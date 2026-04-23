"""
src/ui_builder/data_viz.py
===========================
Các hàm vẽ biểu đồ tái sử dụng được cho Phần 2 (EDA).

Hàm:
- plot_revenue_trend(df, save_path)      : Line chart doanh thu theo thời gian
- plot_category_breakdown(df, save_path) : Bar chart doanh thu theo danh mục
- plot_return_rate_by_size(df, save_path): Bar chart tỷ lệ trả hàng theo size
- plot_traffic_vs_revenue(df, save_path) : Scatter web traffic vs revenue
- plot_seasonal_heatmap(df, save_path)   : Heatmap doanh thu theo tháng x năm

Mỗi hàm nhận DataFrame và đường dẫn lưu ảnh (PNG), trả về fig object.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_revenue_trend(df, save_path=None):
    """
    Vẽ line chart doanh thu (Revenue) theo ngày.
    df: DataFrame với DatetimeIndex và cột 'Revenue'.
    """
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(df.index, df["Revenue"], linewidth=0.8)
    ax.set_title("Xu hướng Doanh thu theo Ngày (2012–2022)")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Doanh thu (VNĐ)")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def plot_category_breakdown(df, save_path=None):
    """
    Vẽ bar chart tổng doanh thu theo danh mục sản phẩm.
    df: DataFrame có cột 'category' và 'Revenue'.
    """
    # TODO: implement
    raise NotImplementedError


def plot_return_rate_by_size(df, save_path=None):
    """
    Vẽ bar chart tỷ lệ trả hàng (returns/order_items) theo kích cỡ S/M/L/XL.
    Liên quan đến Q9 trong MCQ.
    """
    # TODO: implement
    raise NotImplementedError


def plot_traffic_vs_revenue(traffic_df, sales_df, save_path=None):
    """
    Scatter plot: số sessions hàng ngày vs doanh thu cùng ngày.
    Dùng để phân tích mối quan hệ web traffic → doanh số.
    """
    # TODO: implement
    raise NotImplementedError


def plot_seasonal_heatmap(df, save_path=None):
    """
    Heatmap doanh thu trung bình theo tháng (trục Y) và năm (trục X).
    Giúp identify tính mùa vụ — quan trọng cho Predictive analysis.
    """
    # TODO: implement
    raise NotImplementedError
