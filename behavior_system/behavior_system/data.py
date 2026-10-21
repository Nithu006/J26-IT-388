import re
import numpy as np
import pandas as pd
from .config import *

_MENTION = re.compile(r"\(user-\d+\)|@\w+")


def load_thai(users_path, timelines_path):
    users = pd.read_csv(users_path)
    tl = pd.read_csv(timelines_path)
    return clean(users, tl)


def clean(users, tl):
    users = users.drop(columns=["Unnamed: 0"], errors="ignore")
    tl = tl.drop(columns=["Unnamed: 0"], errors="ignore")
    tl = tl.drop_duplicates().dropna(subset=[USER_COL, TIME_COL])
    tl[TIME_COL] = pd.to_datetime(tl[TIME_COL], errors="coerce", utc=True)
    tl = tl.dropna(subset=[TIME_COL]).sort_values([USER_COL, TIME_COL]).reset_index(drop=True)
    if LABEL_COL not in users.columns and "depression" in users.columns:   # raw Thai / synthetic schema
        users = users.assign(**{LABEL_COL: users["depression"]})
    if "source" not in users.columns: users = users.assign(source="thai")
    cols = [USER_COL] + [c for c in (LABEL_COL, "anxiety", "source", "group") if c in users.columns]
    return tl.merge(users[cols], on=USER_COL, how="inner")


def post_table(df, min_posts=MIN_POSTS, max_posts=MAX_POSTS, text_col=TEXT_COL):
    """Per-post columns used for windowing (no label needed)."""
    df = df.sort_values([USER_COL, TIME_COL]).copy()
    n = df.groupby(USER_COL)[TIME_COL].transform("size")
    df = df[n >= min_posts].groupby(USER_COL, group_keys=False).head(max_posts).copy()
    df["hour"] = df[TIME_COL].dt.hour
    df["night"] = df["hour"].between(0, 4).astype(float)
    txt = df[text_col].fillna("").astype(str) if text_col in df else pd.Series("", index=df.index)
    df["text_len"] = txt.str.len()
    df["mentions"] = txt.apply(lambda s: len(_MENTION.findall(s)))
    df["gap_h"] = df.groupby(USER_COL)[TIME_COL].diff().dt.total_seconds().div(3600).fillna(0)
    df["idx"] = df.groupby(USER_COL).cumcount()
    df["win"] = df["idx"] // W
    return df


def windows(df, **kw):
    p = post_table(df, **kw)
    w = p.groupby([USER_COL, "win"]).agg(
        gap_mean=("gap_h", "mean"), gap_std=("gap_h", "std"), night_ratio=("night", "mean"),
        text_len=("text_len", "mean"), mentions=("mentions", "mean"), n=("idx", "size")).reset_index()
    w = w[w["n"] == W].copy()
    w["gap_std"] = w["gap_std"].fillna(0)
    w["gap_mean"] = np.log1p(w["gap_mean"]); w["gap_std"] = np.log1p(w["gap_std"])
    return p, w


def build_arrays(df, label_col=LABEL_COL, **kw):
    """Returns users, X_base (n,10), X_seq (n,T,5) raw (unscaled, zero padded), mask (n,T), y."""
    _, w = windows(df, **kw)
    lab = df.drop_duplicates(USER_COL).set_index(USER_COL)[label_col] if label_col in df else None
    users, seqs, base = [], [], []
    for u, g in w.groupby(USER_COL):
        g = g.sort_values("win")[FEATS].values[:T]
        if len(g) == 0:
            continue
        users.append(u); seqs.append(g)
        base.append(np.concatenate([g.mean(0), g.std(0)]))
    X_seq = np.zeros((len(users), T, len(FEATS))); mask = np.zeros((len(users), T), bool)
    for i, g in enumerate(seqs):
        X_seq[i, :len(g)] = g; mask[i, :len(g)] = True
    y = lab.loc[users].astype(int).values if lab is not None else None
    return users, np.array(base), X_seq, mask, y


def fit_scaler_seq(X_seq, mask):
    real = X_seq[mask]
    return real.mean(0), real.std(0) + 1e-8


def scale_seq(X_seq, mask, mu, sd):
    out = (X_seq - mu) / sd
    out[~mask] = 0.0
    return out
