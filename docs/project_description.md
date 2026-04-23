# Datathon 2026 — The Gridbreakers: Mô tả Dự án

## Bối cảnh
Cuộc thi do VinTelligence (VinUni DS&AI Club) tổ chức.
Bộ dữ liệu mô phỏng hoạt động của một doanh nghiệp thời trang TMĐT tại Việt Nam
từ 04/07/2012 đến 31/12/2022 (train) và 01/01/2023–01/07/2024 (test).

## Ba phần thi
| Phần | Nội dung | Điểm |
|------|----------|------|
| 1 | 10 câu hỏi Trắc nghiệm (MCQ) | 20đ |
| 2 | Trực quan hoá & Phân tích EDA | 60đ |
| 3 | Mô hình Dự báo Doanh thu (Sales Forecasting) | 20đ |

## Cấu trúc thư mục
```
data/raw/           ← CSV gốc (không commit)
data/processed/     ← Data sau xử lý
notebooks/          ← Jupyter notebooks theo từng bước
src/                ← Module Python dùng chung
  data_loader/      ← Load & merge data
  ui_builder/       ← Dashboard & visualization
  ui_predictor/     ← Giao diện dự báo
  utils/            ← Hàm tiện ích chung
figures/            ← Biểu đồ export ra (PNG/SVG)
submission/         ← File submission.csv nộp Kaggle
docs/               ← Tài liệu dự án
```

## Kaggle
Link: https://www.kaggle.com/competitions/datathon-2026-round-1
