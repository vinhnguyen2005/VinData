"""
src/ui_builder/data_viz.py
===========================
Các hàm vẽ biểu đồ tái sử dụng được cho Phần 2 (EDA).

Hàm:
- plot_revenue_trend(df, save_path)         : Bar daily + MA30 overlay
- plot_gross_margin_trend(df, save_path)    : Area chart gross margin % + linear trend
- plot_mom_heatmap(df, save_path)           : Heatmap MoM growth theo tháng x năm
- plot_category_breakdown(df, save_path)    : 100% stacked bar doanh thu theo danh mục x năm
- plot_return_rate_by_size(df, save_path)   : Bar chart tỷ lệ trả hàng theo size
- plot_traffic_vs_revenue(df, save_path)    : Scatter web traffic vs revenue
- plot_seasonal_heatmap(df, save_path)      : Heatmap doanh thu TB theo tháng x năm
- plot_rfm_segment_dist(df, save_path)      : Bar chart phân bổ RFM segment
- plot_cohort_retention(df, save_path)      : Heatmap cohort retention

Mỗi hàm nhận DataFrame và đường dẫn lưu ảnh (PNG), trả về fig object.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# ── Style chung ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi"     : 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size"      : 11,
})

PALETTE = {
    "blue"  : "#1f77b4",
    "orange": "#ff7f0e",
    "green" : "#2ca02c",
    "red"   : "#d62728",
    "gray"  : "#7f7f7f",
}


def _save(fig, save_path):
    """Lưu figure nếu có save_path."""
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")


# ── D1: REVENUE & PROFITABILITY ───────────────────────────────────────────────

def plot_revenue_trend(df, save_path=None):
    """
    Viz D1_01 — Bar daily revenue + MA30 overlay.

    df cần có:
        date (datetime), revenue (float), revenue_ma30 (float)
    """
    fig, ax1 = plt.subplots(figsize=(16, 5))

    # Bar = daily revenue
    ax1.bar(df["date"], df["revenue"],
            color=PALETTE["blue"], alpha=0.45, width=1, label="Daily Revenue")
    ax1.axhline(df["revenue"].mean(), color=PALETTE["gray"],
                linewidth=0.8, linestyle="--", label="Average")
    ax1.set_ylabel("Revenue")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))

    # Line = MA30 trên trục phụ
    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["revenue_ma30"],
             color=PALETTE["orange"], linewidth=2, label="MA30")
    ax2.set_ylabel("Revenue MA30")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))

    ax1.set_title("Revenue Trend — Daily + MA30 Overlay", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Date")

    # Legend gộp 2 trục
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_gross_margin_trend(df, save_path=None):
    """
    Viz D1_02 — Area chart Gross Margin % theo tháng + linear trend.

    df cần có: year_month (str), gross_margin_pct (float)
    """
    fig, ax = plt.subplots(figsize=(14, 4))

    x     = np.arange(len(df))
    y     = df["gross_margin_pct"].values
    x_lbl = df["year_month"].values

    ax.fill_between(x, y, alpha=0.35, color=PALETTE["green"])
    ax.plot(x, y, color=PALETTE["green"], linewidth=1.5)
    ax.axhline(0, color=PALETTE["gray"], linewidth=0.8, linestyle="--")

    # Linear trend
    z = np.polyfit(x, y, 1)
    ax.plot(x, np.poly1d(z)(x), "--", color=PALETTE["gray"],
            linewidth=1.5, label=f"Trend ({z[0]:+.2f}%/month)")

    # Tick x: chỉ show mỗi 12 tháng cho dễ đọc
    step = max(1, len(x) // 10)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(x_lbl[::step], rotation=45, ha="right")
    ax.set_ylabel("Gross Margin %")
    ax.set_title("Gross Margin % Trend", fontsize=14, fontweight="bold")
    ax.legend()

    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_mom_heatmap(df, save_path=None):
    """
    Viz D1_03 — Heatmap MoM growth (%) theo tháng × năm.
    Đỏ = giảm, Xanh = tăng.

    df cần có: year_month (str 'YYYY-MM'), mom_growth_pct (float)
    """
    data = df.copy()
    data["year"]  = data["year_month"].str[:4]
    data["month"] = data["year_month"].str[5:7]

    pivot = data.pivot(index="month", columns="year", values="mom_growth_pct")

    fig, ax = plt.subplots(figsize=(16, 5))
    sns.heatmap(
        pivot,
        cmap="RdYlGn", center=0,
        annot=True, fmt=".1f", annot_kws={"size": 9},
        linewidths=0.4, linecolor="#e0e0e0",
        ax=ax,
    )
    ax.set_title("MoM Growth Calendar Heatmap  (red=drop · green=grow)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Month")
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_category_breakdown(df, save_path=None):
    """
    Viz D1_04 — 100% Stacked bar: % doanh thu theo danh mục × năm.

    df cần có: order_year (int), category (str), line_revenue (float)
    """
    grp   = df.groupby(["order_year", "category"])["line_revenue"].sum().reset_index()
    pivot = grp.pivot(index="order_year", columns="category", values="line_revenue").fillna(0)
    pct   = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(14, 6))
    pct.plot(kind="bar", stacked=True, ax=ax, colormap="tab10", edgecolor="white")

    # Label % bên trong cột
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", label_type="center",
                     fontsize=8, color="white")

    ax.set_title("Category Revenue Share by Year", fontsize=14, fontweight="bold")
    ax.set_ylabel("% of Total Revenue")
    ax.set_xlabel("Year")
    ax.set_ylim(0, 105)
    ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ── D2: CUSTOMER ANALYSIS ─────────────────────────────────────────────────────

def plot_rfm_segment_dist(df, save_path=None):
    """
    Viz D2_01 — Bar chart phân bổ số khách theo RFM segment.

    df cần có: rfm_segment (str)
    """
    counts = (df["rfm_segment"]
              .value_counts()
              .sort_values(ascending=True))

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(counts.index, counts.values,
                   color=PALETTE["blue"], alpha=0.8)
    ax.bar_label(bars, padding=4, fmt="%d")
    ax.set_title("RFM Segment Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Số khách hàng")
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_cohort_retention(df, save_path=None):
    """
    Viz D2_02 — Heatmap cohort retention rate (%).

    df cần có: cohort_month (str), period_number (int), retention_rate (float)
    """
    pivot = df.pivot(index="cohort_month",
                     columns="period_number",
                     values="retention_rate")

    fig, ax = plt.subplots(figsize=(18, max(6, len(pivot) * 0.4)))
    sns.heatmap(
        pivot,
        cmap="YlGnBu", vmin=0, vmax=100,
        annot=True, fmt=".1f", annot_kws={"size": 8},
        linewidths=0.3, linecolor="#e0e0e0",
        ax=ax,
    )
    ax.set_title("Cohort Retention Rate (%)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Months Since First Purchase")
    ax.set_ylabel("Cohort (First Purchase Month)")
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ── D3: PRODUCT PERFORMANCE ───────────────────────────────────────────────────

def plot_return_rate_by_size(df, save_path=None):
    """
    Viz D3_01 — Bar chart tỷ lệ trả hàng theo size (S/M/L/XL).

    df cần có: size (str), return_quantity (int), quantity (int)
    hoặc đã tính sẵn return_rate (float)
    """
    grp = (df.groupby("size")
             .agg(total_qty=("quantity", "sum"),
                  total_ret=("return_quantity", "sum"))
             .reset_index())
    grp["return_rate"] = (grp["total_ret"] / grp["total_qty"] * 100).round(2)
    grp = grp.sort_values("return_rate", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(grp["size"], grp["return_rate"],
                  color=PALETTE["red"], alpha=0.75)
    ax.bar_label(bars, fmt="%.2f%%", padding=3)
    ax.set_title("Return Rate by Product Size", fontsize=14, fontweight="bold")
    ax.set_ylabel("Return Rate (%)")
    ax.set_xlabel("Size")
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_traffic_vs_revenue(traffic_df, sales_df, save_path=None):
    """
    Viz D3_02 — Scatter: daily sessions vs daily revenue.

    traffic_df cần có: date (datetime), sessions (int)
    sales_df   cần có: date (datetime), revenue (float)
    """
    merged = pd.merge(
        traffic_df[["date", "sessions"]],
        sales_df[["date", "revenue"]],
        on="date", how="inner"
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(merged["sessions"], merged["revenue"],
               alpha=0.4, s=15, color=PALETTE["blue"])

    # Trend line
    z = np.polyfit(merged["sessions"], merged["revenue"], 1)
    x_line = np.linspace(merged["sessions"].min(), merged["sessions"].max(), 200)
    ax.plot(x_line, np.poly1d(z)(x_line),
            color=PALETTE["orange"], linewidth=2, label="Trend")

    ax.set_title("Web Traffic vs Daily Revenue", fontsize=14, fontweight="bold")
    ax.set_xlabel("Daily Sessions")
    ax.set_ylabel("Daily Revenue")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))
    ax.legend()
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_seasonal_heatmap(df, save_path=None):
    """
    Viz D3_03 — Heatmap doanh thu TB theo tháng × năm.
    Giúp xác định tính mùa vụ — quan trọng cho forecasting.

    df cần có: date (datetime), revenue (float)
    """
    data = df.copy()
    data["year"]  = data["date"].dt.year
    data["month"] = data["date"].dt.month

    pivot = (data.groupby(["month", "year"])["revenue"]
                 .mean()
                 .unstack())

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(
        pivot / 1e6,          # đổi sang triệu cho dễ đọc
        cmap="Blues",
        annot=True, fmt=".1f", annot_kws={"size": 9},
        linewidths=0.3,
        ax=ax,
    )
    ax.set_title("Seasonal Heatmap — Avg Daily Revenue by Month × Year (triệu)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Month")
    plt.tight_layout()
    _save(fig, save_path)
    return fig