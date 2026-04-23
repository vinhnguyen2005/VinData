"""
src/ui_predictor/prediction.py
===============================
Module load mô hình đã train và thực hiện dự báo doanh thu.

Hàm:
- load_model(model_path)               : Load mô hình từ file .pkl / .joblib
- predict_revenue(model, features_df)  : Trả về Series dự báo Revenue

Cách dùng trong dashboard:
    model = load_model("models/best_model.pkl")
    preds = predict_revenue(model, test_features)

⚠️  Không dùng Revenue/COGS từ test làm feature đầu vào — vi phạm ràng buộc đề thi.
"""

import joblib
import pandas as pd
from pathlib import Path


def load_model(model_path: str | Path):
    """Load mô hình sklearn/XGBoost/LightGBM từ file .pkl hoặc .joblib."""
    return joblib.load(model_path)


def predict_revenue(model, features_df: pd.DataFrame) -> pd.Series:
    """
    Chạy mô hình trên features_df và trả về Series dự báo Revenue.
    Index của output khớp với index của features_df (DatetimeIndex).
    """
    preds = model.predict(features_df)
    return pd.Series(preds, index=features_df.index, name="Revenue")
