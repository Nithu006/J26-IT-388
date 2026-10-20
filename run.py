"""Usage:
  python run.py train --users users_annonym.csv --timelines timelines_annonym.csv   # real data
  python run.py train --users users_annonym.csv --timelines timelines_annonym.csv \
                      --stmhd ~/Downloads/data_sample --reddit ~/Desktop/ic_small.csv  # merged datasets
  python run.py train --synthetic                                                  # software test only
  python run.py serve [--port 8000]
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["train", "serve"])
ap.add_argument("--users"); ap.add_argument("--timelines"); ap.add_argument("--synthetic", action="store_true")
ap.add_argument("--stmhd", help="Twitter-STMHD sample folder (disorder folders + neg)")
ap.add_argument("--stmhd-pos", help="full STMHD depression folder (cleaned_data_depression)")
ap.add_argument("--stmhd-neg", help="full STMHD control folder (cleaned_data_neg)")
ap.add_argument("--stmhd-per-class", type=int, default=300)
ap.add_argument("--reddit", help="Reddit identity-claim CSV (ic_small.csv)")
ap.add_argument("--reddit-max-users", type=int, default=100)
ap.add_argument("--art", default="artifacts"); ap.add_argument("--port", type=int, default=8000)
ap.add_argument("--repeats", type=int, default=5); ap.add_argument("--epochs", type=int, default=150)
ap.add_argument("--no-browser", action="store_true")
a = ap.parse_args()
if a.cmd == "train":
    from behavior_system import pipeline
    if a.synthetic:
        from behavior_system.synthetic import make_synthetic
        us, tl = make_synthetic(60); name = "SYNTHETIC test data (not real)"
    else:
        from behavior_system import loaders
        parts, names = [], []
        if a.users and a.timelines: parts.append(loaders.load_thai(a.users, a.timelines)); names.append("Thai depression/anxiety Twitter corpus")
        if a.stmhd: parts.append(loaders.load_stmhd(a.stmhd)); names.append("Twitter-STMHD sample")
        if a.stmhd_pos and a.stmhd_neg:
            parts.append(loaders.load_stmhd_dump({"depression": a.stmhd_pos, "neg": a.stmhd_neg}, a.stmhd_per_class))
            names.append(f"Twitter-STMHD full (depression vs neg, {a.stmhd_per_class}/class)")
        if a.reddit: parts.append(loaders.load_reddit_ic(a.reddit, a.reddit_max_users)); names.append("Reddit identity-claim")
        if not parts: sys.exit("Give --users and --timelines and/or --stmhd / --reddit (or --synthetic).")
        us, tl = loaders.combine(*parts); name = " + ".join(names)
    pipeline.run(us, tl, a.art, n_repeats=a.repeats, epochs=a.epochs, dataset_name=name, synthetic=a.synthetic)
    print("\nDone. Now run:  python run.py serve")
else:
    if not os.path.exists(os.path.join(a.art, 'meta.json')): sys.exit('No trained model found. Run first:  python run.py train --users ... --timelines ...')
    from behavior_system.server import serve
    serve(a.art, a.port, not a.no_browser)
