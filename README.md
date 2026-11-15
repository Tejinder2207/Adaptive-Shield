# Adaptive Shield — SMS Spam Classification Pipeline

An end-to-end Machine Learning pipeline and FastAPI web service designed to classify SMS messages as either **Ham** (legitimate) or **Spam**, complete with Exploratory Data Analysis (EDA), MLflow experiment tracking, ONNX model optimization, and an interactive web backend.

---

## 🚀 Features

* **Automated Data Pipeline:** Automatically fetches, loads, and cleans the SMS Spam Collection dataset.
* **Exploratory Data Analysis (EDA):** Generates distribution statistics, text length insights, and visualization charts saved automatically to the `plots/` directory.
* **Machine Learning & Tracking:** Trains robust text classification models using `scikit-learn` with class balancing, tracked via `MLflow`.
* **Model Optimization:** Exports trained models to `ONNX` format for high-performance inference.
* **FastAPI Backend:** Serves the model via a high-performance web API endpoint for real-time predictions.

---

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **Framework:** FastAPI, Uvicorn
* **ML Libraries:** Scikit-Learn, Pandas, NumPy, ONNX Runtime, SKL2ONNX
* **Tracking:** MLflow
* **Visualization:** Matplotlib

---

## 📁 Project Structure

```text
Adaptive Shield/
├── data/               # Raw and processed datasets
├── models/             # Saved model artifacts and ONNX exports
├── plots/              # EDA charts and performance visualizations
├── static/             # Frontend assets (if applicable)
├── .venv/              # Virtual environment
├── pyproject.toml      # Project configuration and dependencies
└── run_all.py          # Master pipeline execution script
## 📊 Project Preview 


![alt text](<Screenshot 2026-11-15 171613.png>)