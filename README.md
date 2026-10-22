
# J26-IT-388 — Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media

**Research Project:** Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media  
**Group ID:** J26-IT-388  
**Institution:** Sri Lanka Institute of Information Technology (SLIIT)  
**Research Stage:** PP1 — Prototype Development

---

## 1. Project Overview

This research aims to develop an AI-based framework for analyzing social media information to support mental-health-related risk prediction, explainable decision-making, and adaptive support.

The proposed system explores natural language processing (NLP), behavioral and temporal analysis, multimodal machine learning, and Explainable Artificial Intelligence (XAI).

The research is divided into four interconnected components, each addressing a specific aspect of the overall problem.

**Note:** The project is currently under research and development. The complete four-component system has not yet been fully integrated or validated.

## 2. Research Problem

Social media platforms contain large amounts of user-generated content that may provide insights into stress and mental wellbeing.

However, existing AI-based approaches can face several challenges:

- Difficulty interpreting complex social media language and patterns.
- Limited consideration of behavioral and temporal changes.
- Challenges in combining information from multiple data sources.
- Limited transparency in AI-generated predictions.
- Difficulty providing understandable and traceable decision-support information.

This research investigates how these challenges can be addressed through an integrated and explainable AI framework.

## 3. Research Objectives

The main objectives of this research are:

1. Analyze social media text using NLP and machine-learning techniques.
2. Investigate behavioral and temporal information related to user activity.
3. Develop a multimodal prediction approach combining relevant information.
4. Apply explainability techniques to improve prediction transparency.
5. Explore adaptive scoring and decision-support mechanisms.
6. Evaluate the proposed approaches using suitable datasets and experimental methods.

## 4. Research Components

| Component | Research Area | Main Purpose |
|---|---|---|
| Component 1 | NLP-Based Text Analysis | Extract relevant information from social media text. |
| Component 2 | Behavioral and Temporal Analysis | Investigate user activity patterns and changes over time. |
| Component 3 | Multimodal Risk Prediction | Combine relevant information to develop a predictive model. |
| Component 4 | Explainable AI & Adaptive Decision Support | Explain predictions, explore adaptive scoring, and provide transparent decision-support information. |

### Component 1 — NLP-Based Text Analysis

Focuses on processing and analyzing social media text using natural language processing and machine-learning techniques.

### Component 2 — Behavioral and Temporal Analysis

Focuses on understanding behavioral patterns and temporal changes in social media activity.

### Component 3 — Multimodal Risk Prediction

Focuses on combining relevant outputs from the other analytical components to support multimodal prediction.

### Component 4 — Explainable AI & Adaptive Decision Support

Focuses on making AI predictions more understandable through explainability techniques and investigating adaptive scoring and rule-based decision support.

A separate provisional Component 4 prototype has been developed for PP1 using a stress-related text classifier, SHAP, LIME, EMA scoring, FastAPI, and Streamlit.

This prototype is not the final integrated multimodal research system.

## 5. Proposed Overall System Workflow

The proposed high-level research workflow is:

```text
Social Media Data
        |
        v
Data Collection and Preprocessing
        |
        +-----------------------------+
        |                             |
        v                             v
NLP-Based Text Analysis      Behavioral and
   (Component 1)             Temporal Analysis
                               (Component 2)
        |                             |
        +-------------+---------------+
                      |
                      v
           Multimodal Prediction
              (Component 3)
                      |
                      v
          Explainable AI Analysis
             (Component 4)
                      |
                      v
       Adaptive Decision Support
                      |
                      v
          Research Dashboard
```

This represents the proposed overall architecture. Full end-to-end integration remains future work.

## 6. Current Development Status

The project is currently in the PP1 prototype-development stage.

Individual research components are being developed and evaluated separately.

The Component 4 provisional prototype currently demonstrates:

- Stress-related text classification using a frozen ML baseline.
- SHAP and LIME model explanations.
- Experimental adaptive scoring using synthetic temporal scenarios.
- Rule-based recommendations and missing-data safeguards.
- FastAPI backend services.
- An interactive Streamlit dashboard.
- Automated software testing.

The development and integration status of the other components should be updated by their respective members.

## 7. Technologies and Research Methods

The overall research investigates technologies and approaches such as:

- Python
- Natural Language Processing (NLP)
- Machine Learning and Deep Learning
- Behavioral and Temporal Data Analysis
- Multimodal Learning
- Explainable AI (SHAP and LIME)
- Adaptive Scoring
- Data Visualization
- Web-Based Research Prototypes

Specific frameworks, algorithms, and model architectures may differ between components and will be documented as their implementations are finalized.

## 8. Project Organization

The repository contains research datasets, experiment notebooks, model artifacts, source code, evaluation results, and prototype interfaces.

The currently available directories include:

```text
J26-IT-388/
├── dashboard/
├── data/
├── docs/
├── experiments/
├── models/
├── notebooks/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

The structure will evolve as additional components are integrated.

## 9. Research Evaluation

The research will be evaluated at both individual-component and integrated-system levels.

Evaluation areas may include:

- Prediction performance and generalization.
- Data quality and preprocessing reliability.
- Explainability quality and consistency.
- Temporal model behavior.
- Robustness and missing-data handling.
- Usability and system transparency.
- Integration and software reliability.

Evaluation results should be reported separately for each component until the complete architecture has been integrated and tested.

## 10. Future Development

Planned future work includes:

1. Completing individual component implementations.
2. Finalizing compatible interfaces between components.
3. Integrating NLP, behavioral, and multimodal prediction outputs.
4. Connecting the final prediction model to explainability and decision-support modules.
5. Evaluating the complete system using appropriate research datasets.
6. Improving robustness, usability, privacy, and system reliability.
7. Preparing the final integrated research demonstration and evaluation.

## 11. Research Limitations and Ethical Considerations

Social media information is complex and may not accurately represent an individual's mental-health condition.

The project must carefully consider:

- Data privacy and responsible data handling.
- Dataset quality and representativeness.
- Bias and limitations in model predictions.
- Uncertainty in AI-generated outputs.
- Responsible interpretation of explainability results.
- Ethical use of sensitive mental-health-related information.

**This project is intended for academic research. It is not a clinically validated diagnostic system, medical advice service, or emergency-response platform.**

---

## 12. Academic Information

**Institution:** Sri Lanka Institute of Information Technology (SLIIT)  
**Research Project ID:** J26-IT-388  
**Group:** G41  
**Research Stage:** PP1

Detailed implementation reports, experimental results, and component-specific documentation will be maintained separately as the project progresses.

---

*This README provides a high-level overview of the overall research project and will be updated as individual components are completed and integrated.*
