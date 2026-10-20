import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from behavior_system.synthetic import make_synthetic
from behavior_system import pipeline
from behavior_system.predict import BehaviorModel

us, tl = make_synthetic(40)
d = tempfile.mkdtemp()
meta = pipeline.run(us, tl, d, n_repeats=1, epochs=30, synthetic=True, progress=lambda *_: None)
bm = BehaviorModel(d)
r = bm.score_posts(tl[tl.participant_id == "SYN001"])
assert 0 <= r["risk"] <= 1 and len(r["vector"]) == 16
try: bm.score_posts(tl[tl.participant_id == "SYN001"].head(3)); raise SystemExit("should fail")
except ValueError: pass
# merged datasets: fake Twitter-STMHD folder + fake Reddit identity-claim CSV
import json, numpy as np, pandas as pd
from behavior_system import loaders
r = np.random.RandomState(1); root = os.path.join(d, "stmhd")
for g, k in (("neg", 6), ("adhd/precovid", 6)):
    for u in range(k):
        os.makedirs(f"{root}/{g}/{u}"); ts = pd.Timestamp("2020-01-01", tz="UTC") + pd.to_timedelta(np.cumsum(r.exponential(20, 30)), unit="h")
        json.dump({str(t.date()): [{"text": "x" * r.randint(5, 140), "timestamp_tweet": str(t), "mentionedUsers": [1] * r.randint(3)}] for t in ts},
                  open(f"{root}/{g}/{u}/tweets.json", "w"))
pd.DataFrame([(f"ic_{u}", 1.6e9 + i * 3600 * r.randint(1, 50)) for u in range(8) for i in range(25)],
             columns=["user", "created_utc"]).to_csv(f"{d}/ic.csv", index=False)
us2, tl2 = loaders.combine((us.assign(label=us.depression, source="thai"), tl), loaders.load_stmhd(root), loaders.load_reddit_ic(f"{d}/ic.csv", 5))
meta = pipeline.run(us2, tl2, d, n_repeats=1, epochs=10, progress=lambda *_: None)
assert set(meta["sources"]) == {"thai", "twitter", "reddit"}, meta["sources"]
assert any(r["model"].startswith("Source-only") for r in meta["results"]) and meta["results_by_source"]
json.loads(open(f"{d}/meta.json").read().replace("NaN", "BAD"))   # must be valid JSON (no NaN)
assert BehaviorModel(d).score_posts(tl[tl.participant_id == "SYN001"])["risk"] >= 0
print("SMOKE TEST PASSED")
