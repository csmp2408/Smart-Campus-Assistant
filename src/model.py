import pandas as pd

def load_data():
    try:
        data = {
            "schedule": pd.read_csv("data/schedule.csv"),
            "library": pd.read_csv("data/library.csv"),
            "dining": pd.read_csv("data/dining.csv"),
            "admin": pd.read_csv("data/admin.csv")
        }
        print("✅ Data loaded successfully")
        return data
    except Exception as e:
        print("❌ Data loading error:", e)
        return {"error": str(e)}

def run_ai_model(query):
    data = load_data()
    if "error" in data:
        return f"Data loading failed: {data['error']}"

    query = query.lower()

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
