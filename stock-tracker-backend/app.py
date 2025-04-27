import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# hier deine Config für die Datenbank setzen
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@db:5432/stocksdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Datenbankverbindung
DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://postgres:mysecretpassword@localhost:5432/stocksdb"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Tabelle definieren
class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)

Base.metadata.create_all(engine)

# API-Endpunkte

@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    stock_list = []
    for stock in stocks:
        price = get_stock_price(stock.symbol)
        stock_list.append({
            'id': stock.id,
            'symbol': stock.symbol,
            'price': price
        })
    return jsonify(stock_list)

@app.route('/stocks', methods=['POST'])
def add_stock():
    data = request.get_json()
    symbol = data.get('symbol')
    if symbol:
        new_stock = Stock(symbol=symbol)
        db.session.add(new_stock)
        db.session.commit()
        return jsonify({'message': 'Stock added', 'symbol': symbol}), 201
    else:
        return jsonify({'error': 'No symbol provided'}), 400

@app.route('/stocks/<string:symbol>', methods=['DELETE'])
def delete_stock(symbol):
    stock = session.query(Stock).filter_by(symbol=symbol).first()
    if stock:
        db.session.delete(stock)
        db.session.commit()
        return jsonify({'message': 'Stock removed', 'symbol': symbol})
    else:
        return jsonify({'error': 'Stock not found'}), 404

# Methoden
def get_stock_price(symbol):
    api_key = "d06li9pr01qg26s8nl50d06li9pr01qg26s8nl5g"
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Fehler werfen bei HTTP-Error
        data = response.json()
        return data.get('c', 0)  # 'c' ist der aktuelle Preis bei Finnhub
    except Exception as e:
        print(f"Fehler beim Abrufen von {symbol}: {e}")
        return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

with app.app_context():
    db.create_all()