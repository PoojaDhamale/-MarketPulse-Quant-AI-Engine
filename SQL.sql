CREATE TABLE IF NOT EXISTS stock_sentiment (
    "Date" DATE,
    "Open" NUMERIC,
    "High" NUMERIC,
    "Low" NUMERIC,
    "Close" NUMERIC,
    "Volume" NUMERIC,
    "Stock" VARCHAR(10),
    "Sector" VARCHAR(50),
    "Daily_Return" NUMERIC,
    "MA_7" NUMERIC,
    "MA_30" NUMERIC,
    "Price_Range" NUMERIC,
    "Volatility_7" NUMERIC,
    "sentiment_score" NUMERIC,
    "Sentiment_Category" VARCHAR(20),
    "Target" INTEGER
);

SELECT * FROM stock_sentiment

COPY stock_sentiment
FROM 'C:\pgdata\merged_stock_sentiment_with_target.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')

-- 1.Calculate the Total Trading Days,Average Overall Sentiments and Average Historical Volatilty
SELECT 
    "Sector", 
    COUNT(*) as total_trading_days,
    ROUND(AVG(sentiment_score)::numeric, 4) as avg_macro_sentiment,
    ROUND(AVG("Volatility_7")::numeric, 4) as avg_historical_volatility
FROM stock_sentiment
GROUP BY "Sector"
ORDER BY avg_macro_sentiment DESC;

-- 2.Worst Trading Days Analysis (Sentiment_Category is Negative and Daily_Return is less than -0.03)
SELECT 
    "Date", 
    "Stock", 
    "Sector", 
    ROUND(sentiment_score::numeric, 2) as macro_sentiment,
    ROUND(("Daily_Return" * 100)::numeric, 2) as asset_return_pct,
    "Volume"
FROM stock_sentiment
WHERE "Sentiment_Category" = 'Negative' 
  AND "Daily_Return" < -0.03
ORDER BY "Daily_Return" ASC
LIMIT 15;

-- 3.Identifies days where a stock has a temporary 7-day upward bounce (`MA_7 > MA_30`),
--   but is trapped inside a crashing 30-day macro economic news environment (`sentiment_score < -0.2`).
SELECT 
    "Date", 
    "Stock", 
    ROUND("MA_7", 2) as Short_Term_Avg, 
    ROUND("MA_30", 2) as Long_Term_Avg, 
    ROUND(sentiment_score, 2) as Macro_Sentiment
FROM stock_sentiment
WHERE "MA_7" > "MA_30" 
  AND "sentiment_score" < -0.2
ORDER BY "Date" DESC;

-- 4.Model Hit-Ratio Performance Attribution Analysis
SELECT 
    "Stock",
    COUNT(*) as total_observations,
    SUM(CASE WHEN "Target" = 1 THEN 1 ELSE 0 END) as total_predicted_up_days,
    SUM(CASE WHEN "Target" = 1 AND "Daily_Return" > 0 THEN 1 ELSE 0 END) as correct_up_predictions,
    ROUND(
        (SUM(CASE WHEN "Target" = 1 AND "Daily_Return" > 0 THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN "Target" = 1 THEN 1 ELSE 0 END), 0) * 100)::numeric, 2
    ) as model_hit_ratio_percentage
FROM stock_senti
GROUP BY "Stock"
ORDER BY model_hit_ratio_percentage DESC;

-- 5.Most Fluctautaing Price ranges by Stock

WITH RankedVolatility AS (
    SELECT 
        "Date", 
        "Stock", 
        "Price_Range", 
        "Sentiment_Category",
        DENSE_RANK() OVER (PARTITION BY "Stock" ORDER BY "Price_Range" DESC) as volatility_rank
    FROM stock_sentiment
)
SELECT "Date", "Stock", "Price_Range", "Sentiment_Category", volatility_rank
FROM RankedVolatility
WHERE volatility_rank <= 3
ORDER BY "Stock", volatility_rank;




