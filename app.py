import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0f1419 0%, #1a4d5c 50%, #0d2d3d 100%);
        background-attachment: fixed;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00d4ff;
        color: white;
        text-align: center;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-1 { border-left-color: #ff6b6b; }
    .metric-2 { border-left-color: #4ecdc4; }
    .metric-3 { border-left-color: #95e1d3; }
    .metric-4 { border-left-color: #ffd93d; }
    .metric-5 { border-left-color: #6bcf7f; }
    .metric-6 { border-left-color: #ff8c42; }
    .weather-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(15, 139, 180, 0.2), rgba(26, 77, 92, 0.3));
        border-radius: 15px;
        margin-bottom: 20px;
        border: 2px solid rgba(0, 212, 255, 0.3);
    }
    .input-section {
        background: linear-gradient(135deg, rgba(15, 139, 180, 0.15), rgba(26, 77, 92, 0.25));
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.2);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-top: 20px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 3px solid #00d4ff;
    }
    hr { border: none; height: 2px; background: rgba(255, 255, 255, 0.2); margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Title and Header
st.markdown("<div class='weather-header'><h1>🌊 Weather Dashboard</h1><p>Real-time weather forecasts & advanced analytics</p></div>", unsafe_allow_html=True)

# Input Section
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col1:
    city = st.text_input("🔍 Enter City Name", placeholder="e.g., London, Tokyo, Karachi", label_visibility="collapsed")
with col2:
    show_hourly = st.checkbox("📅 Hourly", value=True)
with col3:
    show_data = st.checkbox("📊 Raw Data", value=False)
with col4:
    show_advanced = st.checkbox("⚙️ Advanced", value=False)
st.markdown("</div>", unsafe_allow_html=True)

if city.strip() == "":
    st.info("� Enter a city name above to get started!", icon="ℹ️")
    st.stop()

# Fetch Data
with st.spinner(f"✨ Fetching weather for {city}..."):
    # Geo API
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    try:
        geo = requests.get(geo_url).json()
        if not geo:
            st.error(f"❌ City '{city}' not found. Please check the spelling and try again.")
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Error fetching location data: {str(e)}")
        st.stop()

    lat, lon = geo[0]["lat"], geo[0]["lon"]
    city_name, country = geo[0]["name"], geo[0]["country"]

    # Current Weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather = requests.get(weather_url).json()

    # Forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    forecast = requests.get(forecast_url).json()

# Display Current Weather
st.markdown(f"<h3 style='color: white; text-align: center;'>📍 {city_name}, {country}</h3>", unsafe_allow_html=True)

# Current Conditions
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    icon = weather["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
    st.image(icon_url, width=100)

with col2:
    st.markdown(f"<h2 style='color: #00d4ff; margin: 0;'>{weather['main']['temp']:.1f}°C</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: white; margin: 5px 0;'>{weather['weather'][0]['description'].title()}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #ccc; font-size: 14px;'>Feels like {weather['main']['feels_like']:.1f}°C</p>", unsafe_allow_html=True)

with col3:
    sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(weather["sys"]["sunset"]).strftime("%H:%M")
    st.markdown(f"""
    <div style='color: white; text-align: right;'>
        <p style='margin: 5px 0;'>🌅 Sunrise: <b>{sunrise}</b></p>
        <p style='margin: 5px 0;'>🌇 Sunset: <b>{sunset}</b></p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Weather Metrics Grid
st.markdown("<div class='section-title'>📈 Current Conditions</div>", unsafe_allow_html=True)
m1, m2, m3, m4, m5, m6 = st.columns(6)

metrics_data = [
    (m1, "🌡", "Temperature", f"{weather['main']['temp']:.1f}°C", "metric-1"),
    (m2, "🌡", "Feels Like", f"{weather['main']['feels_like']:.1f}°C", "metric-2"),
    (m3, "💧", "Humidity", f"{weather['main']['humidity']}%", "metric-3"),
    (m4, "🌬", "Wind Speed", f"{weather['wind']['speed']:.1f} m/s", "metric-4"),
    (m5, "🔽", "Pressure", f"{weather['main']['pressure']} hPa", "metric-5"),
    (m6, "👁", "Visibility", f"{weather['visibility']/1000:.1f} km", "metric-6"),
]

for col, emoji, label, value, color_class in metrics_data:
    col.markdown(f"""
    <div class='metric-card {color_class}'>
        <p style='margin: 0; font-size: 12px;'>{label}</p>
        <p style='margin: 10px 0; font-size: 20px; font-weight: bold;'>{value}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📅 5-Day Forecast", "⏰ Hourly Forecast", "💡 Insights", "📊 Comparison"])

with tab1:
    st.markdown("<div class='section-title'>5-Day Weather Trend</div>", unsafe_allow_html=True)
    
    df = pd.DataFrame(forecast["list"])
    df["datetime"] = pd.to_datetime(df["dt_txt"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    df["temp"] = df["main"].apply(lambda x: x["temp"])
    df["humidity"] = df["main"].apply(lambda x: x["humidity"])
    df["wind"] = df["wind"].apply(lambda x: x["speed"])
    df["feels_like"] = df["main"].apply(lambda x: x["feels_like"])
    df["pressure"] = df["main"].apply(lambda x: x["pressure"])
    df["clouds"] = df["clouds"].apply(lambda x: x["all"])
    
    daily = df.groupby("date").agg({
        "temp": ["min", "max", "mean"],
        "humidity": "mean",
        "wind": "mean",
        "pressure": "mean",
        "clouds": "mean"
    }).reset_index()
    daily.columns = ["date", "temp_min", "temp_max", "temp_mean", "humidity_mean", "wind_mean", "pressure_mean", "clouds_mean"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=daily["date"], y=daily["temp_max"], name="Max Temp", 
                                       mode='lines+markers', line=dict(color='#ff6b6b', width=2)))
        fig_temp.add_trace(go.Scatter(x=daily["date"], y=daily["temp_min"], name="Min Temp",
                                       mode='lines+markers', line=dict(color='#4ecdc4', width=2),
                                       fill='tonexty', fillcolor='rgba(78, 205, 196, 0.2)'))
        fig_temp.update_layout(title="🌡 Temperature Range", hovermode='x unified', 
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='white'))
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_hum = px.bar(daily, x="date", y="humidity_mean", title="💧 Humidity Levels",
                        color_discrete_sequence=["#4facfe"])
        fig_hum.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             font=dict(color='white'))
        st.plotly_chart(fig_hum, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig_wind = px.area(daily, x="date", y="wind_mean", title="🌬 Wind Speed Trend",
                           color_discrete_sequence=["#43e97b"])
        fig_wind.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='white'))
        st.plotly_chart(fig_wind, use_container_width=True)
    
    with col4:
        fig_pressure = px.line(daily, x="date", y="pressure_mean", title="🔽 Atmospheric Pressure",
                              color_discrete_sequence=["#ffd93d"], markers=True)
        fig_pressure.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(color='white'))
        st.plotly_chart(fig_pressure, use_container_width=True)
    
    fig_clouds = px.area(daily, x="date", y="clouds_mean", title="☁️ Cloud Coverage",
                        color_discrete_sequence=["#a8b3ff"])
    fig_clouds.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'))
    st.plotly_chart(fig_clouds, use_container_width=True)

with tab2:
    st.markdown("<div class='section-title'>Hourly Forecast (Next 48 Hours)</div>", unsafe_allow_html=True)
    
    hourly = df.head(24).copy()
    hourly["time"] = hourly["datetime"].dt.strftime("%H:%M")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hourly = go.Figure()
        fig_hourly.add_trace(go.Scatter(x=hourly["time"], y=hourly["temp"], name="Temperature",
                                        mode='lines+markers', line=dict(color='#ff6b6b', width=3),
                                        fill='tozeroy'))
        fig_hourly.update_layout(title="⏰ Temperature in Next 24 Hours", hovermode='x unified',
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'), xaxis_tickangle=-45)
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        fig_hourly_hum = px.bar(hourly, x="time", y="humidity", title="💧 Hourly Humidity",
                               color_discrete_sequence=["#4facfe"])
        fig_hourly_hum.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='white'), xaxis_tickangle=-45)
        st.plotly_chart(fig_hourly_hum, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig_hourly_wind = go.Figure()
        fig_hourly_wind.add_trace(go.Scatter(x=hourly["time"], y=hourly["wind"], name="Wind Speed",
                                            mode='lines+markers', line=dict(color='#43e97b', width=2)))
        fig_hourly_wind.update_layout(title="🌬 Hourly Wind Speed", hovermode='x unified',
                                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                     font=dict(color='white'), xaxis_tickangle=-45)
        st.plotly_chart(fig_hourly_wind, use_container_width=True)
    
    with col4:
        fig_hourly_feels = go.Figure()
        fig_hourly_feels.add_trace(go.Scatter(x=hourly["time"], y=hourly["feels_like"], name="Feels Like",
                                             mode='lines+markers', line=dict(color='#ffd93d', width=2)))
        fig_hourly_feels.update_layout(title="🌡️ Feels Like Temperature", hovermode='x unified',
                                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      font=dict(color='white'), xaxis_tickangle=-45)
        st.plotly_chart(fig_hourly_feels, use_container_width=True)
    
    st.markdown("**Hourly Details:**")
    hourly_display = hourly[["time", "temp", "feels_like", "humidity", "wind"]].copy()
    hourly_display.columns = ["Time", "Temp (°C)", "Feels Like (°C)", "Humidity (%)", "Wind (m/s)"]
    st.dataframe(hourly_display, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("<div class='section-title'>📊 Weather Insights</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🔥 Temperature Trend", f"{daily['temp_max'].iloc[-1]:.1f}°C", 
                 f"{daily['temp_max'].iloc[-1] - daily['temp_max'].iloc[0]:.1f}°C")
        st.metric("💨 Wind Intensity", f"{daily['wind_mean'].mean():.1f} m/s", 
                 "Moderate" if daily['wind_mean'].mean() < 5 else "Strong")
    
    with col2:
        st.metric("💧 Humidity Level", f"{daily['humidity_mean'].mean():.0f}%",
                 "Comfortable" if 40 <= daily['humidity_mean'].mean() <= 60 else "Adjust expectations")
        st.metric("🌅 Daytime Duration", f"{(datetime.fromtimestamp(weather['sys']['sunset']) - datetime.fromtimestamp(weather['sys']['sunrise'])).seconds//3600} hours")
    
    st.info("💡 **Recommendations:** " + ("☂️ Take an umbrella - High humidity expected" if daily['humidity_mean'].mean() > 70 else "🕶️ Enjoy the weather!"))
    
    # Advanced Graphs
    st.divider()
    st.markdown("<h3 style='color: #00d4ff;'>Advanced Weather Analytics</h3>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        fig_temp_variation = go.Figure()
        fig_temp_variation.add_trace(go.Box(y=df["temp"], name="Temperature Distribution", marker=dict(color='#ff6b6b')))
        fig_temp_variation.update_layout(title="🌡 Temperature Distribution", plot_bgcolor='rgba(0,0,0,0)', 
                                        paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_temp_variation, use_container_width=True)
    
    with col_a2:
        fig_scatter = px.scatter(df, x="humidity", y="temp", color="wind", 
                                title="🔗 Temperature vs Humidity vs Wind",
                                color_continuous_scale="Viridis")
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 font=dict(color='white'))
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.markdown("<div class='section-title'>🔄 Weather Comparison</div>", unsafe_allow_html=True)
    
    comparison_data = {
        "Metric": ["Max Temp", "Min Temp", "Avg Humidity", "Avg Wind"],
        "Day 1": [f"{daily['temp_max'].iloc[0]:.1f}°C", f"{daily['temp_min'].iloc[0]:.1f}°C", 
                 f"{daily['humidity_mean'].iloc[0]:.0f}%", f"{daily['wind_mean'].iloc[0]:.1f}m/s"],
        "Day 5": [f"{daily['temp_max'].iloc[-1]:.1f}°C", f"{daily['temp_min'].iloc[-1]:.1f}°C",
                 f"{daily['humidity_mean'].iloc[-1]:.0f}%", f"{daily['wind_mean'].iloc[-1]:.1f}m/s"]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.divider()

# Raw Data Option
if show_data:
    with st.expander("📄 View Raw Forecast Data"):
        st.subheader("5-Day Forecast Details")
        display_df = df[["datetime", "temp", "feels_like", "humidity", "wind"]].copy()
        display_df.columns = ["DateTime", "Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Wind (m/s)"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #aaa; font-size: 12px;'>
    <p>🎨 Built with Streamlit + Plotly | 📍 OpenWeather API | 💾 Data updated in real-time</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
