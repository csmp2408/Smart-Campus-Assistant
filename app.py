import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --- Load Data ---
def load_data():
    return {
        "schedule": pd.read_csv("data/schedule.csv"),
        "library": pd.read_csv("data/library.csv"),
        "dining": pd.read_csv("data/dining.csv"),
        "admin": pd.read_csv("data/admin.csv")
    }

# --- Chatbot Logic ---
def run_ai_model(query):
    query = query.lower()
    data = load_data()

    if "schedule" in query or "class" in query:
        return data["schedule"].to_string(index=False)
    elif "library" in query:
        return data["library"].to_string(index=False)
    elif "dining" in query or "food" in query or "menu" in query:
        return data["dining"].to_string(index=False)
    elif "admin" in query or "id card" in query or "fee" in query:
        return data["admin"].to_string(index=False)
    else:
        return "Sorry, I couldn't find that info. Try asking about schedule, library, dining, or admin."

# --- UI Setup ---
st.set_page_config(page_title="Smart Campus Assistant", layout="wide")
st.sidebar.title("🧭 Navigation")
view = st.sidebar.radio("Choose View", ["Chatbot", "Dashboard"])

st.markdown("<h1 style='text-align:center;'>🎓 Smart Campus Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your intelligent campus companion powered by AI.</p>", unsafe_allow_html=True)

# --- Chatbot View ---
if view == "Chatbot":
    st.success("👋 Welcome! Ask me anything about your campus.")
    query = st.text_input("📥 Type your question:")
    if query:
        response = run_ai_model(query)
        st.markdown("### 📋 Response")
        st.text_area("", response, height=300)

# --- Dashboard View ---
elif view == "Dashboard":
    data = load_data()
    st.subheader("📊 Campus Analytics Dashboard")

    # --- Metrics in Columns ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Classes", len(data["schedule"]))
    col2.metric("Dining Options", len(data["dining"]))
    col3.metric("Admin Services", len(data["admin"]))

    st.markdown("---")

    # --- Charts in Columns ---
    chart_col1, chart_col2 = st.columns([2, 1])

    # Bar Chart: Classes per Day
    chart_col1.markdown("### 📅 Classes per Day")
    fig1, ax1 = plt.subplots(figsize=(5, 3))  # Smaller chart
    ax1.bar(data["schedule"]["Day"].value_counts().index, data["schedule"]["Day"].value_counts().values, color="skyblue")
    chart_col1.pyplot(fig1)

    # Pie Chart: Admin Services
    chart_col2.markdown("### 🗂️ Admin Services")
    fig2, ax2 = plt.subplots(figsize=(3, 3))  # Smaller pie
    ax2.pie([1]*len(data["admin"]), labels=data["admin"]["Task"], autopct="%1.1f%%")
    chart_col2.pyplot(fig2)

    st.markdown("---")

    # Word Cloud
    st.markdown("### 🍽️ Dining Menu Word Cloud")
    items = ", ".join(data["dining"]["Items"].dropna())
    wordcloud = WordCloud(width=600, height=300, background_color="white").generate(items)
    st.image(wordcloud.to_array())

    st.markdown("---")

    # Dining Filter
    st.markdown("### 🔍 Filter Dining Menu by Day")
    selected_day = st.selectbox("Select Day", data["dining"]["Day"].unique())
    filtered = data["dining"][data["dining"]["Day"] == selected_day]
    st.write(filtered)

