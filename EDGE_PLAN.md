# Edge Deployment Plan

## Goal
Run system locally (mobile/on-device)

## Model Choice
- Lightweight models (XGBoost / small NN)
- Avoid heavy LLMs

## Optimizations
- Quantization
- Reduce TF-IDF size
- Cache embeddings

## Latency
- <100ms per prediction

## Tradeoffs
Accuracy vs speed:
- Smaller model → faster
- Larger model → better accuracy

## Deployment Options
- Mobile (Android/iOS via ONNX)
- Local API (FastAPI)
- Desktop app

## Robustness Handling

### Short Text
Fallback to metadata

### Missing Data
Imputation

### Conflicts
Weighted scoring

### Uncertainty
Confidence threshold

## Final Goal
Real-time emotional assistant