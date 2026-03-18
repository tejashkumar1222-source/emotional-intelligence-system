#  Emotional Intelligence System

## Overview
This project builds a real-world emotional intelligence system that:
- Understands user emotional state from noisy text
- Handles uncertainty and missing signals
- Recommends meaningful next actions
- Provides timing decisions

## Pipeline
1. Text preprocessing (TF-IDF)
2. Metadata features (sleep, stress, energy)
3. Model:
   - Emotion → Classification (XGBoost)
   - Intensity → Regression (XGBoost)
4. Decision Engine:
   - Uses emotion + stress + energy + time
5. Uncertainty modeling:
   - Confidence threshold
   - Uncertain flag

## Features Used
- Text (journal)
- Sleep hours
- Stress level
- Energy level
- Time of day
- Previous mood

## How to Run

```bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run app/streamlit_app.py