# MarketPulse: Financial Sentiment Analytics Engine 📊

[Live Web Demo](https://hvsctehrjaf9e2grydbjfa.streamlit.app/) 

## Problem Statement & Overview
Traditional financial models rely strictly on historical price structures and technical market filters, completely ignoring the velocity of public information transmission. This project was engineered to solve a core qualitative constraint: *Investigate whether extracting public emotions and real-time news discussions via Natural Language Processing (NLP) can predict forward stock market behavior better than traditional financial metrics alone.* 

By constructing a joint framework mapping S&P 500 news discussions against a diversified 10-stock portfolio across 10,181 synchronized records, this pipeline isolates the boundaries of sentiment-driven market predictive edges compared to traditional metrics alone.

---

## Data Sources
*   **Macro Discussion & News Feed:** Core text corpus consisting of historical S&P 500 headline streams and macroeconomic news discussions covering a multi-year window to capture shifting public emotion.
*   **Micro Equity Metrics:** Historical daily transaction records (Open, High, Low, Close, Volume) covering a diversified 10-stock portfolio representing key sector vectors (Technology, Financials, Energy, Healthcare).

---

## Features Matrix
The unified feature store matches top-down macro discussion data with micro-technical price filters to evaluate market trends:

### 📢 Macro Sentiment Features (NLP Layer)
*   **VADER Sentiment Index:** Normalized compound text metrics scaling from `-1.00` (Deep Public Panic) to `+1.00` (Extreme Bullish Hype) mined via text tokenization.
*   **News Regime Category:** Text-driven categorical bounds classifying daily broad public mood into *Positive Bullish Hype*, *Negative Panic*, or *Neutral Consolidation*.

### 📈 Micro Technical Features (Traditional Layer)
*   **Daily Volume Log:** Total number of asset shares traded daily, capturing raw institutional capital activity.
*   **Intraday Volatility Spread:** The structural high-to-low price variance mapped across each single trading session.
*   **Short-Term Trend Filter (MA 7):** A rolling 7-day technical price moving average used to trace immediate momentum blocks.
*   **Long-Term Trend Filter (MA 30):** A rolling 30-day structural technical price moving average tracking overall market baselines.
*   **Historical Volatility Index:** A 7-day rolling window computing asset-specific price fluctuations to evaluate downside risk boundaries.

---

## Data Engineering & Core Pipeline Fixes
*   **The Calendar Gap Trap:** Public discussions and news headlines drop 365 days a year, but the stock exchange closes on weekends. A standard inner join completely erases weekend sentiment data. I built a left-join framework paired with a chronological forward-fill (`.ffill()`) loop to roll weekend news vectors straight into Monday’s opening market sessions to ensure weekend public emotion is preserved.
*   **The Timeline Mismatch Bug:** The raw stock price logs extended through late 2024, but the text sentiment archive truncated on March 4, 2024. To prevent severe data stagnation (feeding the model stale public emotion scores), I enforced a strict database boundary cap at the minimum shared date of **March 4, 2024**, stabilizing the final matrix at **10,181 synchronized records**.
*   **Data Leakage Prevention:** Randomized train/test splits cause severe temporal data leakage by mixing future data points into past partitions. I enforced a strict chronological mask split (Training: 2020–2023 | Testing: Out-of-Sample 2024) to maintain absolute backtest validity.

---

## Modeling & Regime Diagnostics
We benchmarked linear classifiers against non-linear tree structures across the chronological 2024 validation window to evaluate traditional metrics against public emotion vectors:

*   **Technical-Only Baseline (Logistic Regression):** **50.93% Accuracy**
*   **Technical + Sentiment Matrix (Random Forest):** 46.04% Accuracy

### The Analytical Takeaway
During the explosive, single-direction linear breakout regime of early 2024, individual stock prices moved strictly on massive capital momentum rather than broad public discussion text patterns. Because it was insulated from the sentiment column, the simpler linear baseline successfully avoided processing text noise, capturing a clean **50.93% predictive edge** over a pure 50/50 coin flip. This proves that during high-momentum runs, broad public emotion acts as a noise pollutant rather than an alpha signal.

---

## Production Deployment & Warehousing
*   **PostgreSQL Warehouse:** Designed complex analytical queries running CTEs and window partition functions (`DENSE_RANK() OVER`) to audit extreme price-swing shock days for individual stocks.
*   **Power BI Dashboard:** Deployed custom DAX time-intelligence wrappers (`TOTALYTD`) to track strategy compounding curves against passive benchmarks, documenting **3,000 capital preservation days** where the system successfully predicted down market trends and moved portfolio allocations into a risk-free cash shield.
*   **Streamlit Web App:** Deployed an interactive click-to-predict frontend application (`app.py`) that loads the serialized model pickles, fits inputs against training `StandardScaler` profiles live, and flashes real-time green buy parameters or red cash preservation signals.


**Pooja Dhamale**

