"""J26-IT-388 Component 4 · PP1 demo dashboard.

Run from repository root:
  python -m streamlit run dashboard/app.py

Requires local FastAPI server at http://127.0.0.1:8000 (or API_BASE_URL).
All time series are explicitly invented demonstrations, not per-person timelines.
"""
from __future__ import annotations

import os
import math
from typing import Any
from html import escape

import httpx
import pandas as pd
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
DEMO_TEXT = "I have been feeling overwhelmed with my university assignments and deadlines."

SCENARIOS: dict[str, list[float | None]] = {
    "Gradually increasing": [0.20, 0.28, 0.39, 0.52, 0.66, 0.78, 0.89],
    "Gradually decreasing": [0.89, 0.78, 0.66, 0.52, 0.39, 0.28, 0.20],
    "Oscillating inputs": [0.25, 0.85, 0.30, 0.80, 0.20, 0.90, 0.35],
    "Missing observations": [0.82, None, None, None, 0.40, 0.28, 0.31],
    "Sudden synthetic shock": [0.20, 0.20, 0.20, 0.95, 0.95, 0.20, 0.20],
    "Stable middle score": [0.53] * 7,
}

st.set_page_config(
    page_title="MindLens | Explainable AI Research",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
/* MindLens UI v3. Dark, responsive, and intentionally restrained. */
:root {
  --ml-bg: #090f1b; --ml-surface: #121d30; --ml-surface-2: #17263b;
  --ml-border: #263951; --ml-text: #eef4fd; --ml-muted: #a4b9cc;
  --ml-teal: #55dfcf; --ml-violet: #af9aff;
}
.stApp {
  background: radial-gradient(circle at 94% 6%, rgba(45,212,191,.065), transparent 28%),
              radial-gradient(circle at 7% 42%, rgba(167,139,250,.045), transparent 35%),
              var(--ml-bg);
  color: var(--ml-text);
}
/* Layout: allow the browser to handle wide monitors and narrower laptop screens. */
.main .block-container, [data-testid="stMainBlockContainer"] {
  max-width: 1232px !important;
  padding: 2rem clamp(1rem, 3.5vw, 3rem) 4rem !important;
}
[data-testid="stSidebar"] {
  background: #10192a;
  border-right: 1px solid var(--ml-border);
}
[data-testid="stSidebar"] .block-container { padding-top: 1.2rem !important; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { background: transparent; }
/* Do not style generic h1/h2 globally; Streamlit's own markup changes over versions. */
[data-testid="stMarkdownContainer"] { overflow-wrap: break-word; }
[data-testid="stMarkdownContainer"] p { line-height: 1.55; }
[data-testid="stAlert"] { border-radius: 12px !important; }
/* Hero: flex gap prevents the overlapping 'MindLensAI' treatment. */
.ml-hero {
  display: block;
  padding: 12px 0 22px;
  width: 100%;
}
.ml-eyebrow {
  margin-bottom: 13px;
  color: #77e6d6;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: .73rem;
  line-height: 1.5;
  font-weight: 760;
  letter-spacing: .085em;
  text-transform: uppercase;
  overflow-wrap: anywhere;
}
.ml-hero-title {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: .21em;
  margin: 0 0 13px;
  padding: 0 0 5px;
  color: #f6fbff;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: clamp(2.35rem, 4.5vw, 3.7rem);
  line-height: 1.2;
  letter-spacing: -.045em;
  font-weight: 820;
  overflow: visible;
}
.ml-hero-title .ml-title-accent { color: var(--ml-teal); }
.ml-subtitle {
  max-width: 800px;
  color: #b6c7d9;
  font-size: 1rem;
  line-height: 1.72;
}
.ml-hero-rule {
  height: 1px;
  width: 100%;
  margin-top: 22px;
  background: linear-gradient(90deg, rgba(85,223,207,.40), rgba(85,223,207,0));
}
.ml-section-title {
  font-size: 1.05rem;
  line-height: 1.4;
  font-weight: 730;
  letter-spacing: -.012em;
  color: #eef5ff;
  margin: 0 0 10px;
}
.ml-eyebrow-mini {
  display: block;
  font-size: .70rem;
  color: #75dcca;
  letter-spacing: .08em;
  text-transform: uppercase;
  font-weight: 720;
  margin-bottom: 10px;
}
.ml-panel {
  box-sizing: border-box;
  height: 100%;
  min-height: 175px;
  padding: 22px;
  background: linear-gradient(160deg, #17263a, #111d30);
  border: 1px solid #2b3d54;
  border-radius: 15px;
  box-shadow: 0 8px 22px rgba(0,0,0,.10);
}
.ml-panel h3 {
  font-size: 1.17rem;
  letter-spacing: -.018em;
  line-height: 1.35;
  margin: 0 0 8px;
  font-weight: 730;
  color: #f3f7fe;
}
.ml-muted { color: var(--ml-muted); font-size: .92rem; line-height: 1.65; }
.ml-pill {
  display: inline-block;
  border-radius: 99px;
  background: #113c36;
  border: 1px solid #226b60;
  color: #8cf2db;
  padding: 5px 12px;
  font-size: .76rem;
  font-weight: 740;
  letter-spacing: .045em;
}
.ml-rule { font-family: ui-monospace, Consolas, monospace; color: #86e9f6; }
.ml-footer {
  margin-top: 35px;
  padding: 19px 0;
  border-top: 1px solid var(--ml-border);
  color: #91a9c0;
  font-size: .79rem;
  line-height: 1.7;
}
/* Native metric cards and their responsive text sizes. */
[data-testid="stMetric"] {
  box-sizing: border-box;
  padding: 18px 19px !important;
  background: linear-gradient(145deg, #17243a, #111d30);
  border: 1px solid var(--ml-border);
  border-radius: 14px;
  min-height: 118px;
  overflow: hidden;
}
[data-testid="stMetricLabel"] { color: #afc1d4 !important; font-size: .89rem !important; }
[data-testid="stMetricValue"] {
  color: #f2f7ff !important;
  font-size: clamp(1.2rem, 1.85vw, 1.72rem) !important;
  line-height: 1.3 !important;
  overflow-wrap: anywhere;
}
/* Tab treatment with sufficient contrast and no animated border-width jumps. */
.stTabs [data-baseweb="tab-list"] {
  flex-wrap: wrap;
  gap: 7px;
  background: #121e30;
  border: 1px solid #283b50;
  border-radius: 14px;
  padding: 7px;
}
.stTabs [data-baseweb="tab"] {
  min-height: 43px;
  padding: 10px 15px;
  border-radius: 9px;
  color: #bbcada;
  font-weight: 650;
  white-space: normal;
  text-align: center;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
  background: #1b4a4a;
  color: #a4fff0;
}
.stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }
/* Inputs/buttons: allow easy scanning and consistent focus styles. */
[data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {
  border-radius: 14px;
}
.stButton button, .stFormSubmitButton button, .stDownloadButton button {
  border-radius: 10px !important;
  min-height: 42px;
  font-weight: 650;
  transition: background .15s ease, border-color .15s ease;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
  background: linear-gradient(115deg, #0d9488, #087f99) !important;
  color: #ffffff !important;
  border: 1px solid #27c2bb !important;
}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {
  background: linear-gradient(115deg, #0fafa1, #0c95b1) !important;
}
[data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] [data-baseweb="select"] > div {
  border-radius: 10px !important;
  background: #192438;
  border-color: #34465c;
}
[data-testid="stTextArea"] textarea:focus { border-color: #35c9b8 !important; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
[data-testid="stProgress"] > div { border-radius: 8px; }
/* Smaller screens: avoid squeezing 3 columns of text and large headings. */
@media (max-width: 800px) {
  .main .block-container, [data-testid="stMainBlockContainer"] {
    padding: 1.25rem 1rem 3rem !important;
  }
  .ml-hero-title { font-size: 2.4rem; }
  .ml-panel { min-height: 0; padding: 17px; }
  .stTabs [data-baseweb="tab"] { font-size: .85rem; padding: 9px 11px; }
  [data-testid="stMetric"] { min-height: 95px; padding: 14px !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def api_get(path: str) -> dict[str, Any]:
    with httpx.Client(timeout=8.0, trust_env=False) as client:
        response = client.get(f"{API_BASE_URL}{path}")
        response.raise_for_status()
        return response.json()


def api_post(path: str, payload: dict[str, Any], timeout: float = 30.0) -> dict[str, Any]:
    with httpx.Client(timeout=timeout, trust_env=False) as client:
        response = client.post(f"{API_BASE_URL}{path}", json=payload)
        response.raise_for_status()
        return response.json()


def friendly_error(exc: Exception) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        return f"The API returned HTTP {exc.response.status_code}. Check the backend terminal."
    if isinstance(exc, httpx.TimeoutException):
        return "The request timed out. Try again or inspect the backend terminal."
    if isinstance(exc, httpx.RequestError):
        return "Could not reach the local FastAPI server."
    return "The response could not be processed. Inspect the backend terminal."


def interpretation_note() -> None:
    st.caption("Class 1 means stress-related text according to a provisional Dreaddit classifier — not a mental-health diagnosis or calibrated clinical risk.")


def explanation_bar(entries: list[dict[str, Any]], key: str, unit: str) -> None:
    """Native Altair diverging bar chart with direct direction coloring."""
    if not entries:
        st.info("No non-zero contributions were returned.")
        return
    import altair as alt
    frame = pd.DataFrame([{
        "Feature": x["feature"],
        "Weight": float(x[key]),
        "Direction": "Toward class 1" if x[key] >= 0 else "Toward class 0",
    } for x in entries])
    frame["AbsWeight"] = frame["Weight"].abs()
    frame = frame.sort_values("AbsWeight", ascending=False)
    chart = (alt.Chart(frame).mark_bar(cornerRadiusEnd=3).encode(
        x=alt.X("Weight:Q", title=unit),
        y=alt.Y("Feature:N", sort=alt.SortField(field="AbsWeight", order="descending"), title=None),
        color=alt.Color("Direction:N", scale=alt.Scale(domain=["Toward class 1", "Toward class 0"], range=["#2dd4bf", "#a78bfa"]), legend=alt.Legend(orient="bottom")),
        tooltip=["Feature:N", alt.Tooltip("Weight:Q", format="+.5f"), "Direction:N"],
    ).properties(height=max(290, len(frame)*34)).configure_axis(
        labelColor="#c4d2e3", titleColor="#b1c7dc", gridColor="#2b3950"
    ).configure_legend(labelColor="#c4d2e3", titleColor="#b1c7dc"))
    st.altair_chart(chart, use_container_width=True)
    with st.expander("View feature values"):
        st.dataframe(frame[["Feature", "Weight", "Direction"]], hide_index=True, use_container_width=True)


# Sidebar: single source of truth for health status.
st.sidebar.markdown("### MindLens AI")
st.sidebar.caption("J26-IT-388 · Component 4 · PP1")
st.sidebar.divider()
try:
    health = api_get("/health")
    online = health.get("status") == "ok"
except (httpx.HTTPError, ValueError, KeyError):
    online = False
if online:
    st.sidebar.success("FastAPI connected")
else:
    st.sidebar.error("FastAPI disconnected")
st.sidebar.caption(f"Local API: `{API_BASE_URL}`")
st.sidebar.divider()
st.sidebar.markdown("**Research modules**")
for icon, name in [
    ("◉", "Dreaddit text classifier"),
    ("⟡", "SHAP · Local explanations"),
    ("✦", "LIME · Local surrogate"),
    ("↝", "Adaptive EMA scoring"),
    ("♢", "Rule-based recommendations"),
]:
    st.sidebar.caption(f"{icon}  {name}")
st.sidebar.divider()
st.sidebar.info("All temporal sequences in this dashboard are **fictional demonstrations**, never real person-level histories.")

st.markdown(
    """<section class="ml-hero" aria-label="MindLens introduction">
    <div class="ml-eyebrow">Research showcase &nbsp; / &nbsp; Explainable AI &nbsp; / &nbsp; Adaptive intelligence</div>
    <div class="ml-hero-title"><span>MindLens</span><span class="ml-title-accent">AI</span></div>
    <div class="ml-subtitle">An interactive research laboratory for stress-related text classification,
    transparent model explanations, and experimental temporal decision support.</div>
    <div class="ml-hero-rule"></div>
    </section>""",
    unsafe_allow_html=True,
)
st.warning("**Non-clinical research prototype.** Classifier predictions and artificial score bands are not mental-health diagnoses, risk estimates, or emergency alerts.")

# Predict once per click. Persist the *input* alongside results to avoid stale explanations.
with st.container(border=True):
    st.markdown('<div class="ml-section-title">Analyze a text sample</div>', unsafe_allow_html=True)
    with st.form("classify_text", clear_on_submit=False):
        text = st.text_area(
            "Sample text",
            value=DEMO_TEXT,
            height=120,
            max_chars=10000,
            help="Enter fictional demonstration text. Do not enter private health information.",
        )
        submit = st.form_submit_button(
            "Analyze text",
            type="primary",
            disabled=not online,
            use_container_width=True,
        )
    if submit:
        # Use exactly the visible text; no hidden preset overrides.
        selected = text.strip()
        if not selected:
            st.error("Enter a non-empty text sample.")
            # Never keep showing a previous prediction after a failed submission.
            for key in ("prediction", "current_text", "explanations", "explanation_text", "explanation_top_k"):
                st.session_state.pop(key, None)
        else:
            try:
                with st.spinner("Running the frozen text classifier..."):
                    prediction = api_post("/predict", {"text": selected}, timeout=25)
                model_p = float(prediction["probability_stress"])
                if (not math.isfinite(model_p) or not 0 <= model_p <= 1
                        or prediction["predicted_class"] not in (0, 1)
                        or prediction.get("is_clinical_assessment") is not False):
                    raise ValueError("Unexpected prediction API response")
                st.session_state["current_text"] = selected
                st.session_state["prediction"] = prediction
                st.session_state.pop("explanations", None)
                st.session_state.pop("explanation_text", None)
                st.session_state.pop("explanation_top_k", None)
            except (httpx.HTTPError, ValueError, KeyError) as exc:
                st.error(friendly_error(exc))
                st.session_state.pop("prediction", None)
                st.session_state.pop("current_text", None)
                st.session_state.pop("explanations", None)
                st.session_state.pop("explanation_text", None)
                st.session_state.pop("explanation_top_k", None)

if "prediction" not in st.session_state:
    st.info("Enter text and click **Analyze text**. You can then explore the four dashboard areas below.")
else:
    result = st.session_state["prediction"]
    p = float(result["probability_stress"])
    klass = int(result["predicted_class"])
    c1, c2, c3 = st.columns([1.25, 1, 1])
    with c1:
        st.metric("Predicted text label", "Stress-related" if klass == 1 else "Non-stress-related")
    with c2:
        st.metric("Class-1 probability", f"{p:.2%}")
    with c3:
        st.metric("Prediction model", "TF-IDF + LR")
    st.progress(max(0., min(1., p)))
    st.caption("Result for the last submitted text. Edit the input and click Analyze text to update it.")
    interpretation_note()

st.markdown(" ")
overview, explain_tab, temporal_tab, decision_tab = st.tabs([
    "Overview", "Explainability", "Adaptive scoring", "Decision support"
])

with overview:
    st.markdown("### A transparent research workflow")
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="ml-panel"><span class="ml-eyebrow-mini">01 · inference</span><h3>Understand the text</h3><div class="ml-muted">Use a frozen TF-IDF + Logistic Regression model to classify a stress-related text label.</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="ml-panel"><span class="ml-eyebrow-mini">02 · explanations</span><h3>Inspect the reasoning</h3><div class="ml-muted">Explore SHAP log-odds attributions and LIME local-surrogate feature weights.</div></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="ml-panel"><span class="ml-eyebrow-mini">03 · decision support</span><h3>Explore temporal logic</h3><div class="ml-muted">Test fictional time-series inputs, missing observations, and traceable recommendations.</div></div>', unsafe_allow_html=True)
    if "prediction" in st.session_state:
        st.markdown("#### Latest analyzed sample")
        st.code(st.session_state["current_text"], language=None, wrap_lines=True)
    st.info("Model outputs describe *stress-related text labels*. Adaptive scoring is a separate synthetic experiment; no connection to real individual timelines is claimed.")

with explain_tab:
    st.markdown("### Explain the prediction")
    st.caption("Compare two methods without mixing their units. SHAP uses class-1 log-odds; LIME uses a local probability-scale surrogate.")
    if "prediction" not in st.session_state:
        st.info("Analyze a text first to activate the SHAP and LIME panels.")
    else:
        x1, x2 = st.columns([1, 2])
        with x1:
            top_k = st.slider("Maximum features", 5, 20, 10, step=1)
        with x2:
            st.write("")
            if st.button("Generate SHAP + LIME", type="primary", disabled=not online, use_container_width=True):
                current_text = st.session_state["current_text"]
                bundle: dict[str, Any] = {}
                for name, endpoint, timeout in [("shap", "/explain/shap", 60), ("lime", "/explain/lime", 60)]:
                    try:
                        with st.spinner(f"Computing {name.upper()}..."):
                            bundle[name] = api_post(endpoint, {"text": current_text, "top_k": top_k}, timeout=timeout)
                    except (httpx.HTTPError, ValueError, KeyError) as exc:
                        bundle[name] = {"error": friendly_error(exc)}
                st.session_state["explanations"] = bundle
                st.session_state["explanation_text"] = current_text
                st.session_state["explanation_top_k"] = top_k
        # A changed slider must not display old results as though they used the new limit.
        explanation_ready = (
            st.session_state.get("explanation_text") == st.session_state["current_text"]
            and st.session_state.get("explanation_top_k") == top_k
        )
        if explanation_ready:
            bundle = st.session_state.get("explanations", {})
            shap_data = bundle.get("shap", {})
            lime_data = bundle.get("lime", {})
            left, right = st.columns(2, gap="large")
            with left:
                st.markdown("#### ⟡ SHAP")
                if "error" in shap_data:
                    st.error(shap_data["error"])
                elif shap_data:
                    st.metric("Log-odds additivity error", f"{shap_data['additivity_error']:.2e}")
                    explanation_bar(shap_data["contributions"], "shap_value_log_odds", "SHAP contribution (class-1 log-odds)")
                    st.caption("Baseline and prediction reconstruction are evaluated on the full feature vector, not only displayed top features.")
                    with st.expander("SHAP reconstruction details"):
                        st.json({k: shap_data[k] for k in ["baseline_log_odds", "model_log_odds", "reconstructed_log_odds", "additivity_error", "probability_error", "background_size"]})
                else:
                    st.info("Generate explanations to view SHAP output.")
            with right:
                st.markdown("#### ✦ LIME")
                if "error" in lime_data:
                    st.error(lime_data["error"])
                elif lime_data:
                    v1, v2 = st.columns(2)
                    v1.metric("Local surrogate R²", f"{lime_data['local_fidelity_r2']:.3f}")
                    v2.metric("Approximation error", f"{lime_data['absolute_approximation_error']:.4f}")
                    explanation_bar(lime_data["contributions"], "lime_weight", "LIME local surrogate weight")
                    st.caption(f"Uses {lime_data['num_perturbations']:,} perturbations. R² evaluates local approximation, not clinical correctness.")
                else:
                    st.info("Generate explanations to view LIME output.")
        else:
            if st.session_state.get("explanation_text") == st.session_state["current_text"]:
                st.info("Maximum Features changed. Click **Generate SHAP + LIME** again to refresh the explanations and LIME fidelity metrics.")
            else:
                st.info("Click the explanation button to compute the current sample's local attributions.")

with temporal_tab:
    st.markdown("### Adaptive score laboratory")
    st.markdown('<span class="ml-pill">SYNTHETIC SCENARIOS ONLY</span>', unsafe_allow_html=True)
    st.caption("Artificial inputs illustrate EMA response and missing-data safeguards. They are not observations from one person.")
    a, b = st.columns([2, 1])
    with a:
        chosen = st.selectbox("Choose a fictional input sequence", list(SCENARIOS), key="chosen_scenario")
    with b:
        st.write("")
        run_scenario = st.button("Run scenario", type="primary", disabled=not online, use_container_width=True)
    if run_scenario:
        try:
            sequence = SCENARIOS[chosen]
            with st.spinner("Evaluating adaptive scoring and missing-data rules..."):
                scenario_result = api_post("/decision-support", {"probabilities": sequence}, timeout=25)
            if (not isinstance(scenario_result.get("results"), list)
                    or len(scenario_result["results"]) != len(sequence)
                    or scenario_result.get("sequence_length") != len(sequence)):
                raise ValueError("Unexpected decision-support API response")
            st.session_state["scenario_result"] = scenario_result
            st.session_state["scenario_name"] = chosen
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            st.error(friendly_error(exc))
            st.session_state.pop("scenario_result", None)
            st.session_state.pop("scenario_name", None)
    if "scenario_result" in st.session_state and st.session_state.get("scenario_name") != chosen:
        st.info("A different scenario is selected. Click **Run scenario** to replace the previously computed results.")
    if "scenario_result" in st.session_state and st.session_state.get("scenario_name") == chosen:
        scenario_name = st.session_state["scenario_name"]
        rows = st.session_state["scenario_result"]["results"]
        chart_df = pd.DataFrame([{
            "Step": i + 1,
            "Static probability": row["model_probability"],
            "Adaptive EMA score": row["adaptive_score"],
        } for i, row in enumerate(rows)])
        st.markdown(f"#### Scenario: {scenario_name}")
        import altair as alt
        melted = chart_df.melt(id_vars="Step", var_name="Series", value_name="Score")
        chart = (alt.Chart(melted).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X("Step:Q", axis=alt.Axis(tickMinStep=1), title="Invented observation step"),
            y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 1]), title="Illustrative score"),
            color=alt.Color("Series:N", scale=alt.Scale(domain=["Static probability", "Adaptive EMA score"], range=["#a78bfa", "#2dd4bf"])),
            tooltip=["Step", "Series", alt.Tooltip("Score:Q", format=".3f")],
        ).properties(height=330).configure_axis(
            labelColor="#c4d2e3", titleColor="#b1c7dc", gridColor="#2b3950"
        ).configure_legend(labelColor="#c4d2e3", titleColor="#b1c7dc"))
        st.altair_chart(chart, use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Sequence steps", len(rows))
        m2.metric("Missing observations", sum(row["model_probability"] is None for row in rows))
        m3.metric("Informational flags", sum(row["attention_flag"] for row in rows))
        with st.expander("Inspect scoring steps and data-freshness states", expanded=True):
            detail = pd.DataFrame([{
                "Step": i + 1,
                "Input probability": row["model_probability"],
                "EMA score": row["adaptive_score"],
                "Data state": row["data_state"],
                "Rule": row["rule_id"],
                "Indicator": row["attention_flag"],
            } for i, row in enumerate(rows)])
            st.dataframe(detail, hide_index=True, use_container_width=True)
        st.caption("EMA α = 0.35 · Missing gap limit = 2 · Initial score is the first available observation. The backend owns this logic.")
    else:
        st.info("Choose a scenario and click **Run scenario** to view temporal charts and safeguards.")

with decision_tab:
    st.markdown("### Transparent decision support")
    st.caption("Rule-based supportive information only; no clinical triage, intervention, or automatic third-party notification.")
    if "scenario_result" not in st.session_state:
        st.info("Run a synthetic sequence in the Adaptive scoring tab to inspect decisions here.")
    else:
        results = st.session_state["scenario_result"]["results"]
        st.caption(f"Decision trace for last executed fictional scenario: {st.session_state.get('scenario_name', 'Unknown')}")
        latest = results[-1]
        a, b, c = st.columns(3)
        a.metric("Final rule", latest["rule_id"])
        b.metric("Input freshness", latest["data_state"].replace("_", " ").title())
        c.metric("Prototype indicator", "On" if latest["attention_flag"] else "Off")
        st.markdown(
            '<div class="ml-panel">'
            '<span class="ml-eyebrow-mini">Selected decision · '
            f'<span class="ml-rule">{escape(str(latest["rule_id"]))}</span></span>'
            f'<h3>{escape(str(latest["recommendation"]))}</h3>'
            f'<div class="ml-muted">{escape(str(latest["explanation"]))}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("#### Decision trace")
        trace = pd.DataFrame([{
            "Step": i + 1,
            "Rule ID": row["rule_id"],
            "Display band": row["display_band"],
            "Freshness": row["data_state"],
            "Eligible": row["alert_eligible"],
            "Indicator": row["attention_flag"],
            "Message": row["recommendation"],
        } for i, row in enumerate(results)])
        st.dataframe(trace, hide_index=True, use_container_width=True)
        st.download_button("Export fictional decision trace (CSV)", trace.to_csv(index=False).encode("utf-8"),
                           file_name="synthetic_decision_trace.csv", mime="text/csv")
    st.info("Safeguards: stale observations suppress new indicators; near-boundary classifier outputs use an illustrative uncertainty rule; all informational score bands are experimental.")

st.markdown('<div class="ml-footer">MindLens AI · SLIIT PP1 Research Demo · J26-IT-388 Component 4 · Model: Dreaddit stress-related text classifier · No clinical validation · No real longitudinal histories</div>', unsafe_allow_html=True)
