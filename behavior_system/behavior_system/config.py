USER_COL, TIME_COL, TEXT_COL = "participant_id", "created_date", "anonymised_text"
MIN_POSTS, MAX_POSTS, W, T = 20, 60, 5, 12
FEATS = ["gap_mean", "gap_std", "night_ratio", "text_len", "mentions"]
FEAT_LABELS = {
    "gap_mean": "Avg gap between posts (log hours)",
    "gap_std": "Gap variability (log hours)",
    "night_ratio": "Night-time posting ratio (00-04h)",
    "text_len": "Avg post length (chars)",
    "mentions": "Avg @mentions per post (social-interaction proxy)",
}
THRESH_MODERATE, THRESH_HIGH = 0.40, 0.65   # illustrative demo thresholds only
LABEL_COL = "label"   # unified 0/1 target (Thai: depression; Twitter: any disorder; Reddit: identity claim)
SEED = 42
