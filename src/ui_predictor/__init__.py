"""
src/ui_predictor/__init__.py
============================
Package giao diện dự báo — wrap model đã train để dùng trong dashboard.

    from src.ui_predictor import predict_revenue
"""
from .prediction import predict_revenue, load_model
