"""
src/data_loader/loader.py
=========================
Module tập trung việc đọc và merge dữ liệu từ các file CSV gốc.

Hàm chính:
- load_all(raw_dir)         : Load tất cả bảng, trả về dict {tên_bảng: DataFrame}
- load_sales(raw_dir)       : Load sales.csv, parse date, set index
- load_orders_full(raw_dir) : Join orders + customers + geography + payments + shipments

Cách dùng:
    from src.data_loader import load_all
    tables = load_all("data/raw")
    orders = tables["orders"]
"""

from pathlib import Path
import pandas as pd


RAW_FILES = [
    "products", "customers", "promotions", "geography",
    "orders", "order_items", "payments", "shipments",
    "returns", "reviews", "sales", "inventory", "web_traffic",
]


def load_all(raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Load tất cả file CSV từ raw_dir, trả về dict tên->DataFrame."""
    raw_dir = Path(raw_dir)
    tables = {}
    for name in RAW_FILES:
        path = raw_dir / f"{name}.csv"
        if path.exists():
            tables[name] = pd.read_csv(path)
        else:
            print(f"⚠️  Không tìm thấy: {path}")
    return tables


def load_sales(raw_dir: str | Path) -> pd.DataFrame:
    """
    Load sales.csv (tập train), parse cột Date, set làm index.
    Trả về DataFrame với DatetimeIndex và 2 cột: Revenue, COGS.
    """
    df = pd.read_csv(Path(raw_dir) / "sales.csv", parse_dates=["Date"])
    df = df.set_index("Date").sort_index()
    return df


def load_orders_full(raw_dir: str | Path) -> pd.DataFrame:
    """
    Join bảng orders với customers, geography, payments, shipments.
    Dùng cho EDA và feature engineering.
    Trả về DataFrame đã merge, cột trùng tên được xử lý bằng suffix.
    """
    raw_dir = Path(raw_dir)
    orders    = pd.read_csv(raw_dir / "orders.csv",    parse_dates=["order_date"])
    customers = pd.read_csv(raw_dir / "customers.csv", parse_dates=["signup_date"])
    geography = pd.read_csv(raw_dir / "geography.csv")
    payments  = pd.read_csv(raw_dir / "payments.csv")
    shipments = pd.read_csv(raw_dir / "shipments.csv",
                            parse_dates=["ship_date", "delivery_date"])

    df = (orders
          .merge(customers, on="customer_id", how="left", suffixes=("", "_cust"))
          .merge(geography, on="zip", how="left", suffixes=("", "_geo"))
          .merge(payments,  on="order_id",  how="left")
          .merge(shipments, on="order_id",  how="left"))
    return df
