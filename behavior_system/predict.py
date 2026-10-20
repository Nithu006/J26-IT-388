import json
import numpy as np, pandas as pd
from .config import *
from .data import windows, scale_seq
from .nplstm import NumpyLSTM


class BehaviorModel:
    def __init__(self, art="artifacts"):
        z = np.load(f"{art}/behavior_lstm.npz")
        self.mu, self.sd = z["mu"], z["sd"]
        self.lstm = NumpyLSTM.from_state({k: z[k] for k in z.files if k not in ("mu", "sd")})
        self.meta = json.load(open(f"{art}/meta.json"))

    @staticmethod
    def level(p):
        return "HIGH" if p >= THRESH_HIGH else "MODERATE" if p >= THRESH_MODERATE else "LOW"

    def score_posts(self, posts: pd.DataFrame, time_col="created_date", text_col="anonymised_text"):
        d = posts[[time_col] + ([text_col] if text_col in posts else [])].copy()
        d = d.rename(columns={time_col: TIME_COL, text_col: TEXT_COL}); d[USER_COL] = "new_user"
        d[TIME_COL] = pd.to_datetime(d[TIME_COL], errors="coerce", utc=True); d = d.dropna(subset=[TIME_COL])
        if TEXT_COL not in d: d[TEXT_COL] = ""
        if len(d) < W: raise ValueError(f"Need at least {W} posts (got {len(d)}).")
        _, w = windows(d, min_posts=W)
        if w.empty: raise ValueError(f"Need at least {W} posts.")
        seq = w.sort_values("win")[FEATS].values[:T]
        X = np.zeros((1, T, len(FEATS))); M = np.zeros((1, T), bool); X[0, :len(seq)] = seq; M[0, :len(seq)] = True
        Xs = scale_seq(X, M, self.mu, self.sd)
        p = float(self.lstm.predict_proba(Xs, M)[0]); vec = self.lstm.embed(Xs, M)[0]
        coh = self.meta["cohort"]; mean = seq.mean(0)
        dev = {f: float((mean[i] - coh[f]["mean"]) / coh[f]["std"]) for i, f in enumerate(FEATS)}
        return {"risk": p, "level": self.level(p), "n_posts": int(len(d)), "n_windows": int(len(seq)),
                "vector": vec.tolist(), "series": Xs[0][M[0]].tolist(),
                "feature_means": {f: float(mean[i]) for i, f in enumerate(FEATS)}, "deviation_z": dev}
