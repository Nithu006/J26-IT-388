import json, os, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from .config import *
from .data import build_arrays, fit_scaler_seq, scale_seq
from .models import baseline
from .nplstm import NumpyLSTM

EPOCHS = 150


def _metrics(y, p, thr=0.5):
    pr = (p >= thr).astype(int)
    return dict(accuracy=accuracy_score(y, pr), precision=precision_score(y, pr, zero_division=0),
                recall=recall_score(y, pr, zero_division=0), f1=f1_score(y, pr, zero_division=0),
                roc_auc=roc_auc_score(y, p) if len(set(y)) > 1 else float("nan"))   # undefined for a one-class source


def _fit_predict(name, tr, te, Xb, Xs, M, y, epochs=EPOCHS, Xsrc=None):
    if name == "source":   # confound check: predicts from which dataset the user came from, nothing else
        return LogisticRegression(class_weight="balanced").fit(Xsrc[tr], y[tr]).predict_proba(Xsrc[te])[:, 1]
    if name in ("logreg", "rf"):
        sc = StandardScaler().fit(Xb[tr]); m = baseline(name).fit(sc.transform(Xb[tr]), y[tr])
        return m.predict_proba(sc.transform(Xb[te]))[:, 1]
    mu, sd = fit_scaler_seq(Xs[tr], M[tr])
    lstm = NumpyLSTM(len(FEATS)).fit(scale_seq(Xs[tr], M[tr], mu, sd), M[tr], y[tr], epochs=epochs)
    return lstm.predict_proba(scale_seq(Xs[te], M[te], mu, sd), M[te])


def _summ(ms):
    v = {m: np.array([d[m] for d in ms], float) for m in ms[0]}
    ok = lambda a: not np.isnan(a).all()
    return {**{m: float(np.nanmean(a)) if ok(a) else float("nan") for m, a in v.items()},
            **{m + "_std": float(np.nanstd(a)) if ok(a) else float("nan") for m, a in v.items()}}


def repeated_cv(Xb, Xs, M, y, src=None, n_splits=5, n_repeats=5, epochs=EPOCHS, progress=print):
    """Folds are stratified by source x label so every fold contains every dataset. Overall metrics are per fold;
    per-source metrics use each repeat's pooled out-of-fold predictions (some sources are too small per fold)."""
    src = np.array(["all"] * len(y)) if src is None else np.asarray(src)
    names = {"logreg": "Logistic Regression (non-temporal)", "rf": "Random Forest (non-temporal)", "lstm": "LSTM (temporal)"}
    srcs = sorted(set(src)); Xsrc = (src[:, None] == np.array(srcs)[None]).astype(float)
    if len(srcs) > 1: names["source"] = "Source-only (confound check)"
    strata = np.char.add(src.astype(str), y.astype(str))
    acc = {k: [] for k in names}; oof = {k: np.zeros(len(y)) for k in names}; by_src = {k: [] for k in names}
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The least populated class")
        for fi, (tr, te) in enumerate(rskf.split(Xb, strata)):
            for k in names:
                p = _fit_predict(k, tr, te, Xb, Xs, M, y, epochs, Xsrc)
                acc[k].append((y[te], p)); oof[k][te] = p
            if (fi + 1) % n_splits == 0:
                for k in names: by_src[k].append({s: _metrics(y[src == s], oof[k][src == s]) for s in srcs})
                if progress: progress(f"  repeat {(fi + 1) // n_splits}/{n_repeats} done")
    rows = [{"model": names[k], **_summ([_metrics(a, b) for a, b in lst])} for k, lst in acc.items()]
    src_rows = [{"source": s, "model": names[k], "n_users": int((src == s).sum()), "n_pos": int(y[src == s].sum()),
                 **_summ([r[s] for r in by_src[k]])} for s in srcs for k in names] if len(srcs) > 1 else []
    return pd.DataFrame(rows), pd.DataFrame(src_rows)


def oof_scores(Xb, Xs, M, y, epochs=EPOCHS, strata=None):
    """Out-of-fold LSTM risk per user (so the demo never shows a score from a model trained on that user)."""
    oof = np.zeros(len(y))
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="The least populated class")
        for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(Xb, y if strata is None else strata):
            oof[te] = _fit_predict("lstm", tr, te, Xb, Xs, M, y, epochs)
    return oof


def _records(df):   # NaN -> None so meta.json stays valid JSON for the browser
    return [{k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()} for r in df.to_dict("records")]


def run(users_df, timelines_df, out_dir="artifacts", n_repeats=5, epochs=EPOCHS, dataset_name="Thai corpus", synthetic=False, progress=print):
    from .data import clean
    os.makedirs(out_dir, exist_ok=True)
    df = clean(users_df, timelines_df)
    users, Xb, Xs, M, y = build_arrays(df)
    info = df.drop_duplicates(USER_COL).set_index(USER_COL).loc[users]
    src = info["source"].astype(str).values
    sources = {s: {"n_users": int((src == s).sum()), "n_pos": int(y[src == s].sum()), "n_neg": int((y[src == s] == 0).sum())}
               for s in sorted(set(src))}
    progress(f"Users used: {len(users)}  (positive={int(y.sum())}, negative={int((y == 0).sum())})")
    for s, c in sources.items(): progress(f"  {s}: {c['n_users']} users (positive={c['n_pos']}, negative={c['n_neg']})")
    if len(set(y)) < 2 or y.sum() < 5 or (y == 0).sum() < 5:
        raise ValueError("Not enough users in each class for cross-validation.")
    table, src_table = repeated_cv(Xb, Xs, M, y, src, n_repeats=n_repeats, epochs=epochs, progress=progress)
    oof = oof_scores(Xb, Xs, M, y, epochs, strata=np.char.add(src.astype(str), y.astype(str)))
    mu, sd = fit_scaler_seq(Xs, M)
    lstm = NumpyLSTM(len(FEATS)).fit(scale_seq(Xs, M, mu, sd), M, y, epochs=epochs)
    vec = lstm.embed(scale_seq(Xs, M, mu, sd), M)
    st = lstm.state()
    np.savez(f"{out_dir}/behavior_lstm.npz", mu=mu, sd=sd, **st)
    vdf = pd.DataFrame(vec, columns=[f"bvec_{i}" for i in range(vec.shape[1])]); vdf.insert(0, "participant_id", users)
    vdf.insert(1, "source", src)
    vdf["risk_oof"] = oof; vdf["label"] = y
    vdf.to_csv(f"{out_dir}/behavior_vectors.csv", index=False)
    table.to_csv(f"{out_dir}/results_table_repeated.csv", index=False)
    if len(src_table): src_table.to_csv(f"{out_dir}/results_by_source.csv", index=False)
    flat = pd.DataFrame(Xs[M], columns=FEATS)
    cohort = {f: {"mean": float(flat[f].mean()), "std": float(flat[f].std() + 1e-9),
                  "mean_pos": float(Xs[M & (y == 1)[:, None]][:, i].mean()),
                  "mean_neg": float(Xs[M & (y == 0)[:, None]][:, i].mean())} for i, f in enumerate(FEATS)}
    Zs = scale_seq(Xs, M, mu, sd)
    grp = info["group"].astype(str).values if "group" in info else src
    per_user = {u: {"label": int(l), "risk_oof": float(r), "n_windows": int(M[i].sum()), "source": src[i], "group": grp[i],
                    "series": Zs[i][M[i]].tolist()} for i, (u, l, r) in enumerate(zip(users, y, oof))}
    meta = {"dataset": dataset_name, "synthetic": synthetic, "n_users": len(users), "n_pos": int(y.sum()),
            "n_neg": int((y == 0).sum()), "W": W, "T": T, "min_posts": MIN_POSTS, "max_posts": MAX_POSTS,
            "feats": FEATS, "cohort": cohort, "results": _records(table), "users": per_user,
            "sources": sources, "results_by_source": _records(src_table),
            "thresholds": {"moderate": THRESH_MODERATE, "high": THRESH_HIGH}}
    json.dump(meta, open(f"{out_dir}/meta.json", "w"))
    progress(table.round(3).to_string(index=False))
    if len(src_table): progress("\nPer source:\n" + src_table[["source", "model", "accuracy", "f1", "roc_auc"]].round(3).to_string(index=False))
    return meta
