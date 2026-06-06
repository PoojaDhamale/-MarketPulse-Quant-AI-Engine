import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="MarketPulse AI Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium fintech dark-terminal CSS injection
st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #ffffff; }
    .stButton>button { background-color: #1c2541; color: white; border: 1px solid #5bc0be; border-radius: 8px; font-weight: bold; width: 100%; height: 50px; font-size: 16px; }
    .stButton>button:hover { background-color: #5bc0be; color: #0b132b; }
    div[data-testid="stSidebarUserContent"] { background-color: #1c2541; }
    .prediction-box-up { background-color: rgba(46, 204, 113, 0.15); border: 2px solid #2ecc71; border-radius: 10px; padding: 20px; text-align: center; }
    .prediction-box-down { background-color: rgba(231, 76, 60, 0.15); border: 2px solid #e74c3c; border-radius: 10px; padding: 20px; text-align: center; }
    .stSlider [data-baseweb="slider"] { color: #5bc0be; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CACHED PRODUCTION FILE ENGINE
# ==========================================
BASE_DIR = r"C:\Users\dhama\Desktop\MarketPulse_NLP"
LR_MODEL_PATH = os.path.join(BASE_DIR, "lr_baseline_model.pkl")
RF_MODEL_PATH = os.path.join(BASE_DIR, "rf_sentiment_model.pkl")
SCALER_TECH_PATH = os.path.join(BASE_DIR, "scaler_tech.pkl")
SCALER_SENT_PATH = os.path.join(BASE_DIR, "scaler_sentiment.pkl")

@st.cache_resource
def load_production_pipeline_assets():
    assets = {}
    paths = {
        "lr_model": LR_MODEL_PATH, "rf_model": RF_MODEL_PATH,
        "scaler_tech": SCALER_TECH_PATH, "scaler_sent": SCALER_SENT_PATH
    }
    for key, path in paths.items():
        if not os.path.exists(path):
            st.error(f"❌ Missing critical file asset: `{path}`")
            return None
        with open(path, "rb") as f:
            assets[key] = pickle.load(f)
    return assets

pipeline = load_production_pipeline_assets()

# ==========================================
# 3. INTERACTIVE SIDEBAR CONFIGURATOR
# ==========================================
st.sidebar.title("🛠️ Asset Selector Panel")
st.sidebar.markdown("---")

selected_stock = st.sidebar.selectbox(
    "Select Target Equity:",
    ["NVDA", "AAPL", "MSFT", "TSLA", "JPM", "GS", "XOM", "CVX", "JNJ", "PFE"]
)

# Automated sector matching to preserve data framework logic
sector_mapping = {
    "NVDA": "Technology", "AAPL": "Technology", "MSFT": "Technology", "TSLA": "Consumer Cyclical",
    "JPM": "Financials", "GS": "Financials", "XOM": "Energy", "CVX": "Energy",
    "JNJ": "Healthcare", "PFE": "Healthcare"
}
selected_sector = sector_mapping[selected_stock]

st.sidebar.info(f"**Asset Profile:**\n* Ticker: **{selected_stock}**\n* Sector: **{selected_sector}**")
st.sidebar.markdown("---")

# Model strategy layer architecture selection toggle
selected_strategy = st.sidebar.radio(
    "Select Pipeline Configuration:",
    ["Technical-Only Baseline (Logistic Regression)", "Technical + Sentiment (Random Forest)"]
)

st.sidebar.markdown("---")
st.sidebar.caption("MarketPulse Engine v1.1 | Out-of-Sample Validation Terminal")

# ==========================================
# 4. EXECUTIVE CANVAS HEADERS
# ==========================================
st.title("📊 MarketPulse: Market Sentiment & Trading Report")
st.subheader("Interactive Machine Learning Scenario Arena")
st.write("Adjust the technical indicators and macro sentiment vectors to stress-test your quantitative strategy boundaries in real time.")
st.markdown("---")

if pipeline is not None:
    # ==========================================
    # 5. DYNAMIC HISTORICAL RANGE CONSTRAINTS
    # ==========================================
    # Enforces feature constraints mapped to the true historical data distributions
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Micro-Technical Performance Metrics")
        
        # Sliders configured to accurately trace true historical price boundaries
        volume = st.slider("Daily Trading Volume", min_value=100000, max_value=150000000, value=35000000, step=100000)
        price_range = st.slider("Intraday Volatility Range (High - Low)", min_value=0.05, max_value=25.0, value=4.20, step=0.05)
        ma_7 = st.slider("Short-Term Trend Filter (7-Day Moving Average)", min_value=5.0, max_value=480.0, value=165.0, step=0.5)
        ma_30 = st.slider("Long-Term Trend Filter (30-Day Moving Average)", min_value=5.0, max_value=480.0, value=160.0, step=0.5)
        volatility_7 = st.slider("7-Day Historical Price Volatility Index", min_value=0.005, max_value=0.120, value=0.028, step=0.001)

    with col2:
        st.markdown("### 📰 Top-Down Macro-Sentiment Vector")
        st.write("Modify the macro component below to analyze directional trajectory flips under changing news environments.")
        
        sentiment_score = st.slider(
            "VADER Text Sentiment Index Score", 
            min_value=-1.00, 
            max_value=1.00, 
            value=0.03, 
            step=0.01
        )
        
        # Real-time dashboard contextual status updates matching your Power BI view
        if sentiment_score < -0.1:
            st.error("⚠️ Prevailing News Regime: **SYSTEMIC PANIC CRISIS**")
        elif sentiment_score > 0.1:
            st.success("✅ Prevailing News Regime: **POSITIVE BULLISH HYPE**")
        else:
            st.info("ℹ️ Prevailing News Regime: **NEUTRAL CONSOLIDATION**")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Execution Core")
        predict_button = st.button("RUN QUANT ALGORITHMIC PREDICTION ENGINE")

    # ==========================================
    # 6. PIPELINE INFERENCE & STATISTICAL OUTPUT DISPLAY
    # ==========================================
    st.markdown("---")
    
    if predict_button:
        # Initialize conditional prediction parameters
        if selected_strategy == "Technical-Only Baseline (Logistic Regression)":
            # Baseline uses technical variables only (5 features)
            raw_inputs = np.array([[volume, price_range, ma_7, ma_30, volatility_7]])
            scaled_inputs = pipeline["scaler_tech"].transform(raw_inputs)
            prediction = pipeline["lr_model"].predict(scaled_inputs)[0]
            probabilities = pipeline["lr_model"].predict_proba(scaled_inputs)[0]
            model_name = "Logistic Regression Baseline"
        else:
            # Champion setup maps all 6 features including sentiment arrays
            raw_inputs = np.array([[volume, price_range, ma_7, ma_30, volatility_7, sentiment_score]])
            scaled_inputs = pipeline["scaler_sent"].transform(raw_inputs)
            prediction = pipeline["rf_model"].predict(scaled_inputs)[0]
            probabilities = pipeline["rf_model"].predict_proba(scaled_inputs)[0]
            model_name = "Random Forest Champion"

        st.markdown("### 🚀 Real-Time Tactical Capital Signal")
        
        # Generate clean visual notification panels matching your layout colors
        if prediction == 1:
            confidence = probabilities[1] * 100
            st.markdown(f"""
                <div class='prediction-box-up'>
                    <h2 style='color:#2ecc71; margin:0;'>🟩 STRATEGY TARGET DIRECTION: UP SIGNAL (1)</h2>
                    <p style='font-size:18px; margin:10px 0 0 0;'>
                        The <b>{model_name}</b> predicts a positive directional move for <b>{selected_stock}</b> 
                        tomorrow with an execution confidence signature of <b>{confidence:.2f}%</b>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            confidence = probabilities[0] * 100
            st.markdown(f"""
                <div class='prediction-box-down'>
                    <h2 style='color:#e74c3c; margin:0;'>🟥 STRATEGY TARGET DIRECTION: DOWN SIGNAL (0)</h2>
                    <p style='font-size:18px; margin:10px 0 0 0;'>
                        The <b>{model_name}</b> predicts a negative or flat session for <b>{selected_stock}</b>. 
                        Confidence metrics signature: <b>{confidence:.2f}%</b>.<br>
                        <b>Tactical Risk Filter Active: Move portfolio allocation to Cash (0% Capital Preservation Shield).</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
