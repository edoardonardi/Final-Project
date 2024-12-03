from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure SQLAlchemy for portfolio storage
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# API key loaded from .env file
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# API URLs
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

# Portfolio database model
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    asset_type = db.Column(db.String(10), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    units = db.Column(db.Float, nullable=False)

# Create the database
with app.app_context():
    db.create_all()


def get_historical_stock_price(symbol, date):
    """Fetch historical stock price for a specific date using Alpha Vantage."""
    url = f"{ALPHA_VANTAGE_API_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    try:
        historical_data = response['Time Series (Daily)']
        price_on_date = historical_data[date]['4. close']  # '4. close' is the closing price
        return float(price_on_date)
    except KeyError:
        print(f"Debug: Full API Response: {response}")  # Debugging: Log full response
        return None


def get_current_stock_price(symbol):
    """Fetch current stock price using Alpha Vantage API."""
    url = f"{ALPHA_VANTAGE_API_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    try:
        # Get the most recent price
        latest_time = list(response['Time Series (1min)'].keys())[0]
        current_price = response['Time Series (1min)'][latest_time]['4. close']
        return float(current_price)
    except KeyError:
        print(f"Debug: Full API Response: {response}")  # Debugging: Log full response
        return None


@app.route('/')
def index():
    """Homepage with input form and disclaimer."""
    return render_template('index.html')


@app.route('/add_asset', methods=['POST'])
def add_asset():
    """Add an asset to the portfolio."""
    form_data = request.form.to_dict()
    print("Form Data Received:", form_data)  # Debugging

    # Extract form fields
    symbol = form_data.get('symbol')
    asset_type = form_data.get('asset_type')
    purchase_date = form_data.get('purchase_date')
    units = form_data.get('units')

    # Validate required fields
    if not all([symbol, asset_type, purchase_date, units]):
        return jsonify({"error": "All fields (symbol, asset_type, purchase_date, units) are required."}), 400

    try:
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()
        units = float(units)
    except ValueError:
        return jsonify({"error": "Invalid date or units format."}), 400

    # Fetch historical price
    purchase_price = get_historical_stock_price(symbol, purchase_date.strftime('%Y-%m-%d'))
    if purchase_price is None:
        return jsonify({"error": f"Could not retrieve historical price for {symbol} on {purchase_date}."}), 400

    # Add to database
    asset = Asset(
        symbol=symbol,
        asset_type=asset_type,
        purchase_date=purchase_date,
        purchase_price=purchase_price,
        units=units
    )
    db.session.add(asset)
    db.session.commit()

    return redirect(url_for('view_portfolio'))


@app.route('/portfolio', methods=['GET'])
def view_portfolio():
    """Calculate and display portfolio performance."""
    assets = Asset.query.all()
    total_value = 0
    details = []

    for asset in assets:
        symbol = asset.symbol
        asset_type = asset.asset_type
        purchase_price = asset.purchase_price
        units = asset.units
        current_price = get_current_stock_price(symbol)

        if current_price:
            current_value = units * current_price
            total_value += current_value
            absolute_change = current_value - (units * purchase_price)
            percentage_change = (absolute_change / (units * purchase_price)) * 100
            details.append({
                "id": asset.id,
                "symbol": symbol,
                "asset_type": asset_type,
                "units": units,
                "purchase_price": purchase_price,
                "current_price": current_price,
                "current_value": current_value,
                "absolute_change": absolute_change,
                "percentage_change": percentage_change,
                "is_positive": percentage_change > 0  # For color styling
            })

    return render_template('portfolio.html', details=details, total_value=total_value)


@app.route('/delete_asset/<int:asset_id>', methods=['POST'])
def delete_asset(asset_id):
    """Delete an asset from the portfolio."""
    asset = Asset.query.get(asset_id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return redirect(url_for('view_portfolio'))
    return jsonify({"error": "Asset not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
