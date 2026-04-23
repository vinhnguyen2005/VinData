# Datathon 2026 — The Gridbreakers

> **VinTelligence × VinUni DS&AI Club** | Cuộc thi Khoa học Dữ liệu đầu tiên tại VinUniversity

## Thành viên nhóm
| Tên | Vai trò |
|-----|---------|
| ... | EDA & Visualization |
| ... | Feature Engineering |
| ... | Modelling & Forecasting |
| ... | Report & Presentation |

## Cấu trúc thư mục

```
datathon2026/
├── data/
│   ├── raw/                  ← CSV gốc từ ban tổ chức (không commit)
│   └── processed/            ← Data sau xử lý (parquet)
├── figures/                  ← Biểu đồ export (PNG)
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modelling.ipynb
│   └── 05_explain_model.ipynb
├── src/
│   ├── data_loader/          ← Load & merge CSV
│   ├── ui_builder/           ← Dashboard & visualizations
│   ├── ui_predictor/         ← Giao diện dự báo
│   └── utils/                ← Hàm tiện ích chung
├── submission/               ← submission.csv nộp Kaggle
├── docs/                     ← Tài liệu dự án
├── app.py                    ← Streamlit dashboard entry point
├── requirements.txt
└── environment.yml
```

## Hướng dẫn cài đặt

```bash
# Clone repo
git clone <repo-url>
cd datathon2026

# Cài môi trường (chọn 1 trong 2)
conda env create -f environment.yml        # Windows / Linux
conda env create -f environment_macm1.yml  # Mac Apple Silicon

conda activate datathon2026

# Hoặc dùng pip
pip install -r requirements.txt
```

## Hướng dẫn chạy

1. **Đặt data** vào `data/raw/` (tải từ Kaggle)
2. **Chạy notebooks theo thứ tự**: 01 → 02 → 03 → 04 → 05
3. **File kết quả** xuất ra `submission/submission.csv`
4. **Nộp lên Kaggle**: https://www.kaggle.com/competitions/datathon-2026-round-1

## Kaggle Leaderboard
Link: https://www.kaggle.com/competitions/datathon-2026-round-1

## Phân công công việc

| Task | Notebook / File | Người phụ trách | Deadline |
|------|----------------|-----------------|----------|
| Tiền xử lý data | 01_preprocessing.ipynb | ... | ... |
| EDA & Visualization | 02_EDA.ipynb | ... | ... |
| Feature Engineering | 03_feature_engineering.ipynb | ... | ... |
| Modelling | 04_modelling.ipynb | ... | ... |
| SHAP & Explain | 05_explain_model.ipynb | ... | ... |
| Báo cáo LaTeX | docs/ | ... | ... |
