"""Load each dataset into the common schema used by data.clean():
users: participant_id, label, source[, group]   timelines: participant_id, created_date, anonymised_text
"""
import glob, json, os
import numpy as np, pandas as pd
from .config import *


def load_thai(users_csv, timelines_csv):
    us = pd.read_csv(users_csv).drop(columns=["Unnamed: 0"], errors="ignore")
    tl = pd.read_csv(timelines_csv, usecols=[USER_COL, TIME_COL, TEXT_COL])
    us[LABEL_COL] = us["depression"].astype(int); us["source"] = "thai"; us["group"] = "depression"
    return us[[USER_COL, LABEL_COL, "source", "group"]], tl


def load_stmhd(root):
    """Twitter-STMHD sample: root/<disorder>/<pre|post>covid/<id>/tweets.json and root/neg/<id>/tweets.json.
    Label = 1 for any disorder folder, 0 for neg. Mentions are stripped from the text in this dataset, so they
    are re-inserted as '(user-N)' tokens (the Thai-corpus format) for the mentions feature."""
    urows, rows = [], []
    for f in sorted(glob.glob(os.path.join(os.path.expanduser(root), "**", "tweets.json"), recursive=True)):
        rel = os.path.relpath(f, os.path.expanduser(root)).split(os.sep)
        group, uid = rel[0], "tw_" + rel[-2]
        urows.append((uid, int(group != "neg"), "twitter", group))
        rows += _tweet_rows(f, uid)
    if not urows: raise ValueError(f"No tweets.json files found under {root}")
    return (pd.DataFrame(urows, columns=[USER_COL, LABEL_COL, "source", "group"]),
            pd.DataFrame(rows, columns=[USER_COL, TIME_COL, TEXT_COL]))


def _tweet_rows(path, uid):
    rows = []
    for day in json.load(open(path, encoding="utf-8")).values():
        for t in day:
            ment = "".join(f" (user-{i})" for i in range(len(t.get("mentionedUsers") or [])))
            rows.append((uid, t["timestamp_tweet"], (t.get("text") or "") + ment))
    return rows


def load_stmhd_dump(roots, n_per_class=300, min_posts=MIN_POSTS, max_posts=MAX_POSTS, seed=SEED, progress=print):
    """Full Twitter-STMHD dump: roots = {"depression": ".../cleaned_data_depression", "neg": ".../cleaned_data_neg"},
    each holding <user_id>/tweets.json. Randomly samples n_per_class users per group with >= min_posts tweets and keeps
    each user's earliest max_posts tweets (the same ones the pipeline would use). Label = 0 for "neg", else 1."""
    urows, rows = [], []
    for group, root in roots.items():
        root = os.path.expanduser(root); ids = sorted(os.listdir(root))
        np.random.RandomState(seed).shuffle(ids); kept = skipped = 0
        for u in ids:
            f = os.path.join(root, u, "tweets.json")
            if not os.path.isfile(f): continue
            r = _tweet_rows(f, f"st_{group}_{u}")
            if len(r) < min_posts: skipped += 1; continue
            rows += sorted(r, key=lambda x: x[1])[:max_posts]   # ISO UTC strings sort chronologically
            urows.append((f"st_{group}_{u}", int(group != "neg"), "stmhd", group)); kept += 1
            if kept == n_per_class: break
        progress(f"  STMHD {group}: {kept} users sampled ({skipped} skipped with < {min_posts} tweets)")
        if kept < n_per_class: progress(f"  warning: only {kept} {group} users available")
    return (pd.DataFrame(urows, columns=[USER_COL, LABEL_COL, "source", "group"]),
            pd.DataFrame(rows, columns=[USER_COL, TIME_COL, TEXT_COL]))


def load_reddit_ic(csv, max_users=100, seed=SEED):
    """Reddit identity-claim users (all self-reported, so label = 1; no controls). Timestamps only, no text."""
    d = pd.read_csv(os.path.expanduser(csv), usecols=["user", "created_utc"])
    n = d.groupby("user").size(); ok = n[n >= MIN_POSTS].index.values
    pick = np.random.RandomState(seed).choice(ok, min(max_users, len(ok)), replace=False)
    d = d[d["user"].isin(pick)]
    tl = pd.DataFrame({USER_COL: "rd_" + d["user"].astype(str),
                       TIME_COL: pd.to_datetime(d["created_utc"], unit="s", utc=True), TEXT_COL: ""})
    us = pd.DataFrame({USER_COL: "rd_" + pd.Series(pick).astype(str), LABEL_COL: 1, "source": "reddit", "group": "identity_claim"})
    return us, tl


def combine(*pairs):
    us = pd.concat([p[0] for p in pairs], ignore_index=True)
    tl = pd.concat([p[1].assign(**{TIME_COL: pd.to_datetime(p[1][TIME_COL], errors="coerce", utc=True)}) for p in pairs], ignore_index=True)
    return us, tl
