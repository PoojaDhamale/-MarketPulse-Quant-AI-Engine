# -MarketPulse-Quant-AI-Engine
# MarketPulse: Macro-Sentiment & Equity AI Engine 📊📈
> **An End-to-End Quantitative Analytics Platform & Tactical Trading Simulation**  
> Deployed via: **Python (VADER NLP, Scikit-Learn) | PostgreSQL | Power BI (DAX) | Streamlit**

[![Live Web App](https://shields.io)](YOUR_STREAMLIT_LINK_HERE)
[![Power BI](https://shields.io)](YOUR_GITHUB_LINK_TO_PBIX)
[![Database](https://shields.io)](YOUR_GITHUB_LINK_TO_SQL)

---

## 📌 Executive Summary
Most academic machine learning projects look for a clean dataset, achieve an overfitted 99% accuracy, and break down under real-world conditions. **MarketPulse** is an enterprise-grade full-stack quantitative framework engineered to test a core macroeconomic hypothesis: *Does top-down broad market headline sentiment possess predictive power over bottom-up individual equity trends?*

By mapping **16 years of broad S&P 500 news headline text sentiment vectors** against **10 diversified multi-sector stocks across 10,181 synchronized daily trading rows (2020–2024)**, this platform builds a live, interactive data-warehoused strategy backtest.

---

## 🏗️ Core Pipeline Architecture & Engineering Solutions

```mermaid
graph TD
    A[Raw S&P 500 News Headlines] -->|VADER NLP Feature Extraction| B(Daily Mean Sentiment Vector)
    C[10 Multi-Sector Equity Logs] -->|Chronological Left-Join & ffill| D(Clean Feature Store: 10,181 rows)
    D -->|Strict March 4 2024 Cutoff| E[Mathematical Data Hygiene]
    E -->|Train 2020-2023 | Test 2024| F[Out-of-Sample Validation]
    F -->|Linear Baseline Model| G[50.93% Win-Rate Target Model]
    F -->|PostgreSQL Relational Storage| H[5 Advanced CTE/Window Queries]
    F -->|Custom DAX Code TOTALYTD| I[Interactive Power BI Dashboard]
    F -->|Pre-Trained Pipeline Export .pkl| J[Live Click-to-Predict Streamlit App]
```

### 🛠️ Overcoming Critical Production Data Traps
* **The Time-Travel Trap Solved:** Standard randomized data splits (`train_test_split`) cause severe temporal leakage by mixing future information into past training blocks. This pipeline applies a strict chronological boundary cut-off (Training: 2020–2023 | Testing: True Future 2024) to maintain absolute mathematical honesty.
* **The Stock-Blindness Trap Solved:** Sorting rows purely asset-by-asset causes group boundary splits to entirely eliminate specific sectors from the training partition. The data framework explicitly enforces a joint multi-asset sorting structure (`sort_values(by=["Date", "Stock"])`), guaranteeing a uniform sector distribution across train and test windows.
* **The Market Calendar Gap Solved:** Financial news is generated 365 days a year, but the stock exchange closes on weekends. A standard inner join completely erases weekend headlines. I engineered a left-join framework paired with a grouping **Forward-Fill (`.ffill()`)** loop, rolling weekend news sentiment vectors directly into Monday’s opening trading sessions to prevent critical signal loss.
* **The Timeline Mismatch Bug Fixed:** Identified a structural cutoff mismatch where stock rows extended to December 2024, but the text archive truncated on March 4, 2024. To prevent severe data stagnation (model reading old data), I enforced a strict database boundary cap at the minimum shared date of **March 4, 2024**, scaling the final matrix to a clean, synchronized **10,181 records**.

---

## 🔬 Machine Learning Experiments & Regime Diagnostics

We evaluated linear estimators against non-linear decision tree structures to isolate how different algorithms process abstract public market mood.


| Experiment Layer | Feature Set | ML Algorithm | Testing Accuracy |
| :--- | :--- | :--- | :--- |
| **Baseline 1.0** | Technical Indicators Only | **Logistic Regression** | **50.93% (Champion)** |
| **Baseline 1.1** | Technical Indicators Only | Random Forest | 46.97% |
| **Experiment 2.0** | Technical + Macro Sentiment | Logistic Regression | 47.67% |
| **Experiment 2.1** | Technical + Macro Sentiment | Random Forest | 46.04% |

### 💡 Core Machine Learning Takeaways
* **The Linear Breakthrough:** During the out-of-sample window of early 2024, the market was in an aggressive, single-direction linear bull breakout. The simpler **Logistic Regression baseline captured a dominant 50.93% predictive edge** over a pure 50/50 coin flip.
* **The Feature Noise Discovery:** Injecting broad macro-sentiment into the models caused accuracy to decay. This proved an authentic financial insight: *During strong momentum-driven linear market regimes, broad macro news headlines act as a statistical noise pollutant rather than a helpful signal, and relying on pure micro-technical price trends is mathematically superior.*

---

## 🗄️ PostgreSQL Relational Warehouse Layer
All cleansed, synchronized dataset layers were hosted in a **PostgreSQL relational database via pgAdmin**. The analytical layer features explicit query schemas deployed to audit market transmission patterns before data ingestion:

* **Sector Sensitivity Aggregations:** Evaluated how identical system-wide news headlines trigger wildly different volatility signatures across high-beta technology (NVDA, TSLA) vs. defensive healthcare (JNJ) sectors.
* **Divergence & Trend-Trap Identification:** Isolated specific trading sessions where short-term prices expanded (`MA_7 > MA_30`) but macro headlines turned heavily negative (sentiment score < -0.20), successfully flagging high-risk fake market rallies.
* **Advanced Window Partitioning:** Deployed `DENSE_RANK() OVER (PARTITION BY "Stock" ORDER BY "Price_Range" DESC)` inside an explicit Common Table Expression (CTE) to instantly isolate and audit the top 3 extreme price-swing shock days for each of the 10 assets individually.

---

## 📊 Power BI BI Dashboarding (Tactical Backtest)
The finalized dataset was integrated into an interactive, dual-page dark-themed visual terminal driven by custom **DAX time-intelligence formulas**:

1. **Model Win Rate (50.93%):** Displays the validated directional accuracy edge of our champion baseline system.
2. **Strategy Alpha [(\$149.85)]:** Attributes the portfolio variance between our active strategy and a passive buy-and-hold market index.
3. **Protected Capital Days (3K):** Counts the exact instances where our model successfully anticipated market downside and triggered our risk shield—automatically moving portfolio allocations into cash (**0% return change**) to completely bypass devastating drawdown loops.
4. **Granular Asset Matrix:** Aggregates individual stock hit ratios, cleanly highlighting our model's peak predictive win-rate on high-beta tech assets like **Nvidia (NVDA) at 54.27%**.

---

## 🚀 Interactive Streamlit Application
To turn this project into a working software product, I packaged the pre-trained notebook classifiers and feature scales (`StandardScaler`) using `pickle` into a live click-to-predict web application. 

* **The Scenario Arena:** Users can use interactive sliders to input a stock ticker, alter trading volumes, adjust trend lines (`MA_7` vs. `MA_30`), and change the VADER text sentiment index score.
* **The Execution Core:** The app scales inputs live and executes a forward-pass calculation, flashing a **Vibrant Green UP SIGNAL (1)** for bullish breakouts, or a **Deep Red DOWN SIGNAL (0)** risk box instructing the user to immediately shift capital into a cash shield.

---

## 📁 Repository Structure
```text
├── 📁 01_Machine_Learning/
│   ├── macro_sentiment_model.ipynb     # Jupyter Notebook (Data cleaning, VADER NLP, Train/Test)
│   ├── lr_baseline_model.pkl           # Serialized 50.93% Champion Logistic Regression model
│   └── scaler_tech.pkl                 # Saved technical data feature scaling transformation
├── 📁 02_Database_Warehouse/
│   └── analytics_queries.sql           # Complete PostgreSQL schemas, CTEs, and Window Queries
├── 📁 03_Business_Intelligence/
│   └── MarketPulse_Dashboard.pbix      # Completed 2-page Power BI dashboard template
├── 📁 04_Software_Deployment/
│   └── app.py                          # Python script powering the live Streamlit terminal
└── README.md                           # Core project portfolio documentation
```

---

## ⚙️ How to Run Locally

### 1. Run the ML Pipeline & Export Assets
```bash
jupyter notebook 01_Machine_Learning/macro_sentiment_model.ipynb
```
### 2. Launch the Streamlit Web Application
```bash
pip install streamlit scikit-learn pandas numpy
cd 04_Software_Deployment/
streamlit run app.py
```
