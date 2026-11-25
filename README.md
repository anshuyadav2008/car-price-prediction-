# AutoValue - Car Price Prediction

A Flask web app that estimates a used car's resale price using a Linear Regression model trained from the included `car data.csv` dataset.

## Features

- Estimates resale prices in lakh.
- Shows the model's R² score and mean absolute error.
- Validates vehicle details before making a prediction.
- Trains the model locally when the app starts; no pre-trained model file is required.

## Requirements

- Python 3.11 or newer
- Windows, macOS, or Linux

## Run locally

### Windows

Double-click `run_windows.bat`, or run these commands from the project directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Keep the terminal open while using the app and press Ctrl+C to stop the server.

## Run tests

With the dependencies installed, run:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests on Python 3.11 and 3.14.

## Project structure

```text
.
├── app.py
├── car data.csv
├── requirements.txt
├── run_windows.bat
├── static/
├── templates/
├── tests/
└── .github/workflows/tests.yml
```

## Model and API

- The CSV has 301 vehicle records. The app maps fuel type, seller type, and transmission to numeric values, then evaluates a 90/10 train/test split with `random_state=2`.
- `GET /api/summary` returns dataset size, feature count, R², and mean absolute error.
- `POST /predict` accepts JSON or form fields named `year`, `present_price`, `kms_driven`, `fuel_type`, `seller_type`, `transmission`, and `owner`.

The estimate is for educational purposes only, is expressed in lakh, and is not a live market quote.

## Data and licensing

The included dataset is needed to run the app. Confirm that you have permission to publish and redistribute the dataset before making this repository public. No license is included; add a license only after confirming you have the rights to license the project and its bundled data.
