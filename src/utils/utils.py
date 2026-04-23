"""
src/utils/utils.py
==================
Hàm tiện ích tổng hợp.

Hàm:
- compute_metrics(y_true, y_pred) : Tính MAE, RMSE, R² — dùng để đánh giá model
- save_submission(dates, revenue, cogs, path) : Tạo submission.csv đúng định dạng đề thi
- set_global_seed(seed)           : Đặt random seed cho numpy, random, torch (nếu có)

Định dạng submission.csv theo đề thi:
    Date,Revenue,COGS
    2023-01-01,26607.2,2585.15
    ...
"""

import numpy as np
import pandas as pd
import random
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true, y_pred) -> dict:
    """
    Tính ba chỉ số đánh giá theo đề thi:
    - MAE  (thấp hơn tốt hơn)
    - RMSE (thấp hơn tốt hơn)
    - R²   (cao hơn tốt hơn, lý tưởng gần 1)
    """
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)
    metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
    print(f"MAE={mae:.2f} | RMSE={rmse:.2f} | R²={r2:.4f}")
    return metrics


def save_submission(dates, revenue_preds, cogs_preds, path: str | Path = "submission/submission.csv"):
    """
    Xuất file submission.csv đúng định dạng đề thi.
    - dates        : list hoặc pd.DatetimeIndex các ngày test
    - revenue_preds: array dự báo Revenue
    - cogs_preds   : array dự báo COGS (nếu không dự báo thì dùng giá trị sample)
    - path         : đường dẫn lưu file
    """
    df = pd.DataFrame({
        "Date": pd.to_datetime(dates).strftime("%Y-%m-%d"),
        "Revenue": revenue_preds,
        "COGS": cogs_preds,
    })
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅  Đã lưu submission: {path} ({len(df)} dòng)")


def set_global_seed(seed: int = 42):
    """Đặt seed toàn cục để đảm bảo tái lập kết quả (reproducibility)."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except ImportError:
        pass
