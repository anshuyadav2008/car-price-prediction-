from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "car data.csv"
MODEL_PATH = BASE_DIR / "car_price_model.pkl"
FEATURES = ["Year", "Present_Price", "Kms_Driven", "Fuel_Type", "Seller_Type", "Transmission", "Owner"]

app = Flask(__name__)

def load_and_train():
    df = pd.read_csv(DATA_PATH)
    # Same categorical encoding used in the supplied notebook
    df = df.copy()
    df["Fuel_Type"] = df["Fuel_Type"].map({"Petrol": 0, "Diesel": 1, "CNG": 2})
    df["Seller_Type"] = df["Seller_Type"].map({"Dealer": 0, "Individual": 1})
    df["Transmission"] = df["Transmission"].map({"Manual": 0, "Automatic": 1})
    df = df.dropna(subset=FEATURES + ["Selling_Price"])
    X = df[FEATURES]
    y = df["Selling_Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=2)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = {
        "r2": round(float(r2_score(y_test, predictions)), 3),
        "mae": round(float(mean_absolute_error(y_test, predictions)), 3),
        "total_cars": int(len(df)),
        "features": len(FEATURES)
    }
    joblib.dump(model, MODEL_PATH)
    return model, metrics, df

model, model_metrics, car_data = load_and_train()

@app.route("/")
def home():
    return render_template("index.html", metrics=model_metrics)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or request.form
        year = int(data.get("year"))
        present_price = float(data.get("present_price"))
        kms = float(data.get("kms_driven"))
        fuel = data.get("fuel_type")
        seller = data.get("seller_type")
        transmission = data.get("transmission")
        owner = int(data.get("owner"))

        current_year = pd.Timestamp.now().year
        if year < 1990 or year > current_year:
            return jsonify({"error": f"Year must be between 1990 and {current_year}."}), 400
        if present_price <= 0 or kms < 0 or owner not in [0, 1, 2, 3]:
            return jsonify({"error": "Please enter valid car details."}), 400
        mappings = {
            "fuel_type": {"Petrol": 0, "Diesel": 1, "CNG": 2},
            "seller_type": {"Dealer": 0, "Individual": 1},
            "transmission": {"Manual": 0, "Automatic": 1}
        }
        if fuel not in mappings["fuel_type"] or seller not in mappings["seller_type"] or transmission not in mappings["transmission"]:
            return jsonify({"error": "Please select valid options."}), 400

        row = pd.DataFrame([[
            year, present_price, kms, mappings["fuel_type"][fuel],
            mappings["seller_type"][seller], mappings["transmission"][transmission], owner
        ]], columns=FEATURES)
        price = max(0.0, float(model.predict(row)[0]))
        return jsonify({
            "predicted_price": round(price, 2),
            "formatted_price": f"₹ {price:.2f} Lakh",
            "note": "Estimated value based on the supplied dataset; actual market price may differ."
        })
    except (TypeError, ValueError):
        return jsonify({"error": "Please complete all fields with valid values."}), 400

@app.route("/api/summary")
def summary():
    return jsonify(model_metrics)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
