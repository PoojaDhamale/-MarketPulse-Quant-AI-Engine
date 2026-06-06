# MarketPulse: Macro-Sentiment & Equity AI Engine 📊
An end-to-end quantitative financial analytics pipeline and tactical trading simulation.

[Live Web Demo](YOUR_STREAMLIT_LINK) | [Power BI Dashboard](YOUR_GITHUB_LINK_TO_PBIX) | [SQL Database Schema](YOUR_GITHUB_LINK_TO_SQL)

---

## 🏗️ Technical Architecture
* **NLP Feature Mining:** Processed un-structured S&P 500 news headlines via **VADER NLP**, compressing daily scores and forward-filling weekend sentiment to match market rows.
* **Data Hygiene (March 4, 2024 Cutoff):** Truncated timeline mismatch to prevent data stagnation noise, locking dataset onto **10,181 synchronized records**.
* **Database Warehousing:** Hosted features in **PostgreSQL (pgAdmin)** running complex window function analytics (`DENSE_RANK() OVER`) and CTE loops.
* **BI Strategy Backtest:** Built a dark-themed **Power BI Dashboard** using custom DAX time-intelligence (`TOTALYTD`) to track capital curves.
* **Production Deployment:** Deployed a click-to-predict web terminal using **Streamlit** to handle raw inputs and scale feature matrices live.

---

## 🔬 Machine Learning Results Matrix
* Enforced strict chronological splitting (Train: 2020–2023 | Test: 2024 out-of-sample) to eliminate temporal data leakage traps.


| Experiment Layer | Feature Set | Model Architecture | Testing Accuracy |
| :--- | :--- | :--- | :--- |
| **Baseline 1.0** | Technical Indicators Only | **Logistic Regression** | **50.93% (Champion)** |
| **Baseline 1.1** | Technical Indicators Only | Random Forest | 46.97% |
| **Experiment 2.0** | Technical + Macro Sentiment | Logistic Regression | 47.67% |
| **Experiment 2.1** | Technical + Macro Sentiment | Random Forest | 46.04% |

**Key Finding:** During the single-direction linear breakout regime of early 2024, technical price filters captured a dominant **50.93% predictive edge**, while broad market news sentiment vectors acted as statistical noise, triggering signal decay.

---

## 📊 Core Business Intelligence Totals
* **Model Win Rate:** 50.93% directional predictive success rate over a pure 50/50 coin flip.
* **Protected Capital Days:** **3,000 days** where the strategy successfully predicted down market trends and moved portfolio allocations into a 0% change cash shield.
* **Asset Peak Performance:** Isolated a peak individual asset hit-rate of **54.27% on Nvidia (NVDA)**.

---

## 📁 Repository Directory
```text
├── 📁 01_Machine_Learning/        # Jupyter Notebook (NLP + Model Experimentation) & saved .pkl files
├── 📁 02_Database_Warehouse/      # PostgreSQL schemas, CTE queries, and window function scripts
├── 📁 03_Business_Intelligence/   # Saved 2-page interactive Power BI Desktop (.pbix) framework
└── 📁 04_Software_Deployment/     # Python script (app.py) powering the hosted Streamlit interface
```

---

## ⚙️ Quick Start Local Setup
```bash
# 1. Launch the interactive frontend web server
pip install streamlit scikit-learn pandas numpy
streamlit run 04_Software_Deployment/app.py
```
