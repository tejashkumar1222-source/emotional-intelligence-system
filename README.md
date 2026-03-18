# Emotional Intelligence System

## Overview
A real-world AI system that:
- Understands emotional state from messy human text
- Handles noisy and conflicting signals
- Recommends meaningful next actions
- Models uncertainty explicitly

---

## System Design

### 1. Emotional Understanding
- Text + metadata fusion
- XGBoost classifier

### 2. Decision Engine
- Action: breathing, rest, deep work, etc.
- Timing: now, later, tonight, etc.

### 3. Uncertainty Modeling
- Confidence scores
- Uncertain flag

---

## Dashboard Features
- Multi-tab analytics
- 3D emotional space visualization
- Decision flow visualization
- Real-time prediction

---

## How to Run

```bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run app/streamlit_app.py
