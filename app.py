import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load the trained model directly
model = joblib.load("plantation_profit_model.pkl")  # Ensure this file exists

# Company dataset
company_data = {
    "Elpitiya Plantation": {"Revenue": 250, "Profit": 40, "Employees": 500, "Region": "Central"},
    "Hayleys Plantation": {"Revenue": 300, "Profit": 50, "Employees": 600, "Region": "Southern"},
    "Watawala Plantation": {"Revenue": 280, "Profit": 45, "Employees": 550, "Region": "Western"},
    "Browns Plantation": {"Revenue": 270, "Profit": 43, "Employees": 520, "Region": "Northern"},
    "Akbar Tea Company": {"Revenue": 260, "Profit": 42, "Employees": 510, "Region": "Eastern"},
}

company_locations = {
    "Elpitiya Plantation": [6.2880, 80.1596],
    "Hayleys Plantation": [6.9271, 79.8612],
    "Watawala Plantation": [6.9875, 80.5041],
    "Browns Plantation": [6.8214, 80.0409],
    "Akbar Tea Company": [6.9271, 79.8612]
}

# Function to make predictions directly
def get_profit_margin_prediction(features):
    features = np.array(features).reshape(1, -1)  # Reshape input for model
    prediction = model.predict(features)[0]  # Get prediction
    return round(float(prediction), 2)  # Convert to float and round

# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", ["🏠 Home", "📊 Company Analysis", "📈 Profit Prediction", "🎯 Investment Insights"])

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("🌱 Plantation Profit & Investment Analysis")
    st.subheader("Welcome to the Sri Lanka Plantation Investment Analysis Tool")
    st.write("Use this tool to analyze the profitability of plantation companies based on financial and weather data.")
    #if st.button("Start Analysis 🚀"):
     #   st.switch_page("📊 Company Analysis")
  

# --- COMPANY ANALYSIS ---
elif page == "📊 Company Analysis":
    st.title("📊 Plantation Company Details")
    company_name = st.selectbox("Select a Plantation Company:", list(company_data.keys()))

    if company_name:
        st.subheader(f"📊 Company Overview: {company_name}")
        details = company_data[company_name]
        st.write(f"**Revenue (in million LKR):** {details['Revenue']}")
        st.write(f"**Profit (in million LKR):** {details['Profit']}")
        st.write(f"**Employees:** {details['Employees']}")
        st.write(f"**Region:** {details['Region']}")

        # Revenue vs Profit Bar Chart
        st.subheader("📈 Revenue vs Profit Comparison")
        fig, ax = plt.subplots()
        ax.bar(["Revenue", "Profit"], [details["Revenue"], details["Profit"]], color=["blue", "green"])
        ax.set_ylabel("Million LKR")
        ax.set_title(f"{company_name} - Financial Overview")
        st.pyplot(fig)

        # Plantation Map
        st.subheader("🗺️ Plantation Locations in Sri Lanka")
        plantation_map = folium.Map(location=[7.0, 80.5], zoom_start=8)
        for company, coords in company_locations.items():
            folium.Marker(location=coords, popup=company, tooltip=company).add_to(plantation_map)
        folium_static(plantation_map)

# --- PROFIT PREDICTION ---
elif page == "📈 Profit Prediction":
    st.title("📈 Plantation Profit Margin Prediction")

    # User Input Fields
    historical_avg_temp = st.number_input("Historical Avg Temperature (°C)", min_value=10.0, max_value=40.0, value=20.0)
    yield_metric_tons = st.number_input("Yield (Metric Tons)", min_value=0.0, max_value=1000.0, value=100.0)
    temp_3month_avg = st.number_input("3-Month Avg Temperature (°C)", min_value=10.0, max_value=40.0, value=25.0)
    rainfall_3month_avg = st.number_input("3-Month Avg Rainfall (mm)", min_value=0.0, max_value=500.0, value=150.0)
    humidity_3month_avg = st.number_input("3-Month Avg Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
    rainfall_temp_interaction = st.number_input("Rainfall-Temperature Interaction", min_value=-500.0, max_value=500.0, value=0.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
    temperature = st.number_input("Current Temperature (°C)", min_value=10.0, max_value=40.0, value=25.0)
    temperature_anomaly = st.number_input("Temperature Anomaly", min_value=-5.0, max_value=5.0, value=0.0)

    # Predict Button
    if st.button("Predict Profit Margin"):
        input_data = [
            historical_avg_temp, yield_metric_tons, temp_3month_avg,
            rainfall_3month_avg, humidity_3month_avg, rainfall_temp_interaction,
            humidity, temperature, temperature_anomaly
        ]
        prediction = get_profit_margin_prediction(input_data)

        # Investment Risk Indicators
        if prediction < 10:
            st.error(f"📉 Estimated Profit Margin: {prediction:.2f}% ❌ Risky Investment!")
        elif 10 <= prediction < 15:
            st.warning(f"⚠️ Estimated Profit Margin: {prediction:.2f}% (Moderate Risk)")
        else:
            st.success(f"📈 Estimated Profit Margin: {prediction:.2f}% ✅ Good Investment!")

        # Investment Score Calculation
        investment_score = (prediction * 4) + (yield_metric_tons / 20) + (rainfall_3month_avg / 50)
        if investment_score < 30:
            st.error(f"🎯 Investment Score: {investment_score:.1f} ❌ High Risk")
        elif investment_score < 60:
            st.warning(f"🎯 Investment Score: {investment_score:.1f} ⚠️ Moderate Risk")
        else:
            st.success(f"🎯 Investment Score: {investment_score:.1f} ✅ Safe Investment!")

# --- INVESTMENT INSIGHTS ---
elif page == "🎯 Investment Insights":
    st.title("🎯 Investment Decision Insights")
    selected_companies = st.multiselect("Compare Companies", list(company_data.keys()), default=["Elpitiya Plantation", "Hayleys Plantation"])

    if selected_companies:
        comparison_data = {company: company_data[company]["Profit"] for company in selected_companies}
        st.bar_chart(pd.DataFrame.from_dict(comparison_data, orient="index", columns=["Profit"]))

    st.write("This section provides an overview of the best investment opportunities in Sri Lankan plantations.")
