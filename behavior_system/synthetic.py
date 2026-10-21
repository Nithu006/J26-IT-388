"""SYNTHETIC data in the Thai-corpus schema -- ONLY for testing the software. Never report as real results."""
import numpy as np, pandas as pd


def make_synthetic(n_users=60, seed=0, out_dir=None):
    r = np.random.RandomState(seed); rows, urows = [], []
    for u in range(n_users):
        dep = int(r.rand() < 0.45); pid = f"SYN{u:03d}"
        n = r.randint(22, 90)
        t0 = pd.Timestamp("2021-01-01", tz="UTC") + pd.Timedelta(days=int(r.randint(0, 400)))
        gaps = r.exponential(30 if dep else 22, n) * (r.rand(n) < 0.8) + r.exponential(2, n)
        ts = t0 + pd.to_timedelta(np.cumsum(gaps), unit="h")
        for tt in ts:
            if r.rand() < (0.18 if dep else 0.10):
                tt = tt.normalize() + pd.Timedelta(hours=float(r.uniform(0, 4.9)))
            L = int(r.normal(95 if dep else 110, 40)); L = max(5, L)
            txt = "x" * L + "".join(" (user-%d)" % r.randint(9999) for _ in range(r.poisson(0.5 if dep else 0.9)))
            rows.append((pid, tt.strftime("%Y-%m-%d %H:%M:%S%z"), txt))
        urows.append((pid, dep, int(r.rand() < 0.4)))
    tl = pd.DataFrame(rows, columns=["participant_id", "created_date", "anonymised_text"])
    us = pd.DataFrame(urows, columns=["participant_id", "depression", "anxiety"])
    if out_dir:
        tl.to_csv(f"{out_dir}/timelines_annonym.csv", index=False); us.to_csv(f"{out_dir}/users_annonym.csv", index=False)
    return us, tl
