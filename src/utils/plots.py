"""
src/utils/plots.py
==================
Hàm tiện ích liên quan đến đồ thị và xuất ảnh.

Hàm:
- save_fig(fig, filename, dpi=150) : Lưu matplotlib figure sang thư mục figures/
- set_plot_style()                 : Áp dụng style chung cho tất cả biểu đồ
- add_value_labels(ax)             : Thêm số lên đầu cột bar chart

Quy tắc đặt tên file ảnh:
    figures/<số thứ tự>_<mô_tả_ngắn>.png
    Ví dụ: figures/01_revenue_trend.png
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

FIGURES_DIR = Path("figures")


def set_plot_style():
    """Áp dụng style thống nhất — gọi một lần ở đầu notebook EDA."""
    plt.rcParams.update({
        "figure.dpi": 120,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    })


def save_fig(fig, filename: str, dpi: int = 150):
    """Lưu figure vào thư mục figures/. Tạo thư mục nếu chưa có."""
    FIGURES_DIR.mkdir(exist_ok=True)
    out = FIGURES_DIR / filename
    fig.savefig(out, dpi=dpi, bbox_inches="tight")
    print(f"💾  Đã lưu: {out}")


def add_value_labels(ax, fmt="{:.0f}", fontsize=9):
    """Thêm nhãn số lên đầu mỗi cột bar chart."""
    for p in ax.patches:
        ax.annotate(
            fmt.format(p.get_height()),
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha="center", va="bottom", fontsize=fontsize,
        )
