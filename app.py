import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Configure the quantitative terminal application window
st.set_page_config(
    page_title="MarketPulse AI Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom UI engine configuration to apply a dark-themed terminal container
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

# Resolve system file directories dynamically for cloud and local deployments
base_workspace_dir = os.path.dirname(os.path.abspath(__file__))

path_lr = os.path.join(base_workspace_dir, "lr_baseline_model.pkl")
path_rf = os.path.join(base_workspace_dir, "rf_sentiment_model.pkl")
path_scaler_tech = os.path.join(base_workspace_dir, "scaler_tech.pkl")
path_scaler_sent = os.path.join(base_workspace_dir, "scaler_sentiment.pkl")

@st.cache_resource
def load_quant_pipeline_assets():
    """Loads and caches serialized pipeline components from the local repo root."""
    assets = {}
    resource_registry = {
        "lr_model": path_lr, "rf_model": path_rf,
        "scaler_tech": path_scaler_tech, "scaler_sent": path_scaler_sent
    }
    
    for feature_key, target_path in resource_registry.items():
        # Adaptive file lookup to handle root directory mapping changes on cloud servers
        resolved_path = target_path if os.path.exists(target_path) else os.path.basename(target_path)
        
        if not os.path.exists(resolved_path):
            st.error(f"Missing core pipeline dependency: {os.path.basename(target_path)}")
            return None
        with open(resolved_path, "rb") as data_stream:
            assets[feature_key] = pickle.load(data_stream)
    return assets

pipeline = load_quant_pipeline_assets()

# Build interactive sidebar profile pane
st.sidebar.title("Asset Configuration")
st.sidebar.markdown("---")

selected_stock = st.sidebar.selectbox(
    "Select Target Stock Ticker:",
    ["NVDA", "AAPL", "MSFT", "TSLA", "JPM", "GS", "XOM", "CVX", "JNJ", "PFE"]
)

# Operational sector pairings matching underlying relational database layouts
sector_map = {
    "NVDA": "Technology", "AAPL": "Technology", "MSFT": "Technology", "TSLA": "Consumer Cyclical",
    "JPM": "Financials", "GS": "Financials", "XOM": "Energy", "CVX": "Energy",
    "JNJ": "Healthcare", "PFE": "Healthcare"
}
selected_sector = sector_map[selected_stock]

st.sidebar.info(f"**Asset Profile:**\n* Ticker: **{selected_stock}**\n* Sector: **{selected_sector}**")
st.sidebar.markdown("---")

selected_strategy = st.sidebar.radio(
    "Select Model Structure:",
    ["Technical-Only Baseline (Logistic Regression)", "Technical + Sentiment (Random Forest)"]
)

st.sidebar.markdown("---")
st.sidebar.caption("MarketPulse Engine v1.1 | Production Terminal")

# Main user canvas headers
st.title("📊 MarketPulse: Market Sentiment & Trading Report")
st.write("Adjust the micro-technical sliders and macro sentiment inputs below to evaluate real-time equity trend direction probabilities.")
st.markdown("---")

if pipeline is not None:
    # Setup interactive scenario boundaries
    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown("### Technical Market Indicators")
        volume = st.slider("Daily Volume Log", min_value=100000, max_value=150000000, value=35000000, step=100000)
        price_range = st.slider("Intraday Volatility Spread (High - Low)", min_value=0.05, max_value=55.0, value=4.20, step=0.05)
        ma_7 = st.slider("7-Day Moving Average Filter", min_value=5.0, max_value=480.0, value=165.0, step=0.5)
        ma_30 = st.slider("30-Day Moving Average Filter", min_value=5.0, max_value=480.0, value=160.0, step=0.5)
        volatility_7 = st.slider("7-Day Rolling Historical Volatility Index", min_value=0.005, max_value=0.150, value=0.028, step=0.001)

    with right_column:
        st.markdown("### Broad Macro Sentiment Parameter")
        st.write("Simulate changing text news headline weights compiled via broad market index data feeds.")
        
        sentiment_score = st.slider("VADER Compound Sentiment Score", min_value=-1.00, max_value=1.00, value=0.03, step=0.01)
        
        if sentiment_score < -0.1:
            st.error("Current Regime: **SYSTEMIC PANIC CRISIS**")
        elif sentiment_score > 0.1:
            st.success("Current Regime: **POSITIVE BULLISH HYPE**")
        else:
            st.info("Current Regime: **NEUTRAL CONSOLIDATION**")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### Allocation Execution")
        predict_button = st.button("RUN QUANT ALGORITHMIC PREDICTION ENGINE")

    # Ingestion tracking and inference execution
    st.markdown("---")
    
    if predict_button:
        if selected_strategy == "Technical-Only Baseline (Logistic Regression)":
            raw_features = np.array([[volume, price_range, ma_7, ma_30, volatility_7]])
            scaled_features = pipeline["scaler_tech"].transform(raw_features)
            prediction = pipeline["lr_model"].predict(scaled_features)[0]
            probabilities = pipeline["lr_model"].predict_proba(scaled_features)[0]
            model_name = "Logistic Regression Baseline"
        else:
            raw_features = np.array([[volume, price_range, ma_7, ma_30, volatility_7, sentiment_score]])
            scaled_features = pipeline["scaler_sent"].transform(raw_features)
            prediction = pipeline["rf_model"].predict(scaled_features)[0]
            probabilities = pipeline["rf_model"].predict_proba(scaled_features)[0]
            model_name = "Random Forest Champion"

        st.markdown("### Tactical Strategy Allocation Signal")
        
        # Deploy clear visual output alert modules
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
                        The <b>{model_name}</b> outlines a negative or flat performance trajectory for <b>{selected_stock}</b>. 
                        Confidence metric profile: <b>{confidence:.2f}%</b>.<br>
                        <b>Tactical Risk Strategy Active: Reallocate portfolio exposure to Cash (0% Capital Preservation Shield).</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
