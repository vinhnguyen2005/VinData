"""
src/utils/visualization_code.py
=================================
Đoạn code mẫu / snippet tái sử dụng cho các loại biểu đồ phức tạp.

Nội dung:
- SHAP summary plot wrapper
- Time-series decomposition plot (trend, seasonal, residual)
- Confusion matrix heatmap (nếu có bài phân loại)
- Correlation heatmap (feature selection)

Cách dùng:
    from src.utils.visualization_code import plot_shap_summary
    plot_shap_summary(shap_values, features, save_path="figures/shap_summary.png")
"""

import matplotlib.pyplot as plt
from pathlib import Path


def plot_shap_summary(shap_values, features, save_path=None):
    """
    Vẽ SHAP beeswarm plot — bắt buộc có trong báo cáo Phần 3.
    Cần import shap và đã gọi shap.Explainer trước.
    """
    try:
        import shap
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.summary_plot(shap_values, features, show=False)
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig
    except ImportError:
        raise ImportError("Cần cài: pip install shap")


def plot_ts_decomposition(series, period=7, save_path=None):
    """
    Phân tách chuỗi thời gian thành Trend + Seasonal + Residual.
    series: pd.Series với DatetimeIndex.
    period: chu kỳ mùa vụ (7 = tuần, 365 = năm).
    """
    from statsmodels.tsa.seasonal import seasonal_decompose
    result = seasonal_decompose(series.dropna(), model="additive", period=period)
    fig = result.plot()
    fig.suptitle(f"Decomposition (period={period})", y=1.02)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
