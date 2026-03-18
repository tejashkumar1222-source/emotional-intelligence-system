import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import pickle

st.set_page_config(page_title="Emotional Intelligence System", layout="wide")

# ======================
# 🎨 ADVANCED THEME
# ======================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #1e293b);
}
.card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.6);
    margin-bottom: 20px;
}
h1 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Emotional Intelligence System")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("⚙️ Control Panel")

if st.sidebar.button("🚀 Run Pipeline"):
    subprocess.run(["python", "run_pipeline.py"])
    st.sidebar.success("Pipeline completed!")

uploaded_file = st.sidebar.file_uploader("Upload predictions.csv", type=["csv"])

# ======================
# MAIN APP
# ======================
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ======================
    # TABS
    # ======================
    tabs = st.tabs([
        "📊 Overview",
        "📋 Predictions",
        "📈 Insights",
        "🧭 Actions",
        "🧊 3D View",
        "🤖 Live Prediction"
    ])

    # ======================
    # 📊 OVERVIEW
    # ======================
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Entries", len(df))
        c2.metric("Avg Confidence", f"{df['confidence'].mean():.2f}")
        c3.metric("Uncertainty %", f"{df['uncertain_flag'].mean()*100:.1f}")

        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        col1.plotly_chart(px.histogram(df, x="predicted_state", color="predicted_state"))
        col2.plotly_chart(px.histogram(df, x="predicted_intensity", color="predicted_intensity"))

    # ======================
    # 📋 TABLE
    # ======================
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        emotion = st.selectbox("Filter Emotion", ["All"] + list(df["predicted_state"].unique()))

        if emotion != "All":
            df_filtered = df[df["predicted_state"] == emotion]
        else:
            df_filtered = df

        st.dataframe(df_filtered, use_container_width=True)

        st.download_button("Download CSV", df_filtered.to_csv(index=False))

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # 📈 INSIGHTS
    # ======================
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        col1.plotly_chart(px.box(df, x="predicted_state", y="predicted_intensity", color="predicted_state"))
        col2.plotly_chart(px.histogram(df, x="confidence"))

        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("⚠️ Uncertain Predictions")
        st.dataframe(df[df["uncertain_flag"] == 1])

    # ======================
    # 🧭 ACTIONS
    # ======================
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        col1.plotly_chart(px.histogram(df, x="what_to_do", color="what_to_do"))
        col2.plotly_chart(px.histogram(df, x="when_to_do", color="when_to_do"))

        st.plotly_chart(px.sunburst(df, path=["what_to_do", "when_to_do"]))

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # 🧊 3D VIEW
    # ======================
    with tabs[4]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig = go.Figure(data=[go.Scatter3d(
            x=df["confidence"],
            y=df["predicted_intensity"],
            z=df["uncertain_flag"],
            mode='markers',
            marker=dict(
                size=6,
                color=df["predicted_intensity"],
                colorscale='Viridis'
            )
        )])

        fig.update_layout(scene=dict(
            xaxis_title="Confidence",
            yaxis_title="Intensity",
            zaxis_title="Uncertainty"
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ======================
    # 🤖 LIVE PREDICTION
    # ======================
    with tabs[5]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Enter User Reflection")

        text = st.text_area("Journal Text")

        sleep = st.slider("Sleep Hours", 0.0, 10.0, 6.0)
        stress = st.slider("Stress Level", 1, 5, 3)
        energy = st.slider("Energy Level", 1, 5, 3)

        if st.button("Predict"):
            # simple rule-based fallback (since model not loaded)
            if stress > 4:
                state = "stressed"
                action = "breathing"
                when = "now"
            elif energy < 2:
                state = "tired"
                action = "rest"
                when = "tonight"
            else:
                state = "calm"
                action = "deep_work"
                when = "within_15_min"

            st.success(f"Predicted State: {state}")
            st.info(f"Recommended Action: {action} ({when})")

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("⬅️ Upload predictions.csv to begin")