import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [stocks, setStocks] = useState([]);
  const [newSymbol, setNewSymbol] = useState('');

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    const response = await fetch('/stocks');
    const data = await response.json();
    setStocks(data);
  };

  const addStock = async () => {
    if (newSymbol.trim() === '') return;
    await fetch('/stocks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol: newSymbol.trim() })
    });
    setNewSymbol('');
    fetchStocks();
  };

  const removeStock = async (symbol) => {
    await fetch(`/stocks/${symbol}`, { method: 'DELETE' });
    fetchStocks();
  };

  return (
    <div className="App">
      <h1>Aktien Tracker</h1>
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={newSymbol}
          onChange={(e) => setNewSymbol(e.target.value)}
          placeholder="Aktien-Symbol eingeben (z.B. AAPL)"
          style={{ padding: '8px', marginRight: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
        />
        <button 
          onClick={addStock}
          style={{ padding: '8px 16px', borderRadius: '5px', backgroundColor: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}
        >
        Hinzufügen
        </button>
      </div>

      <table style={{ width: '80%', margin: 'auto', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>Symbol</th>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>Preis (USD)</th>
            <th style={{ padding: '12px', border: '1px solid #ddd' }}>Aktion</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map(stock => (
            <tr key={stock.id}>
              <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{stock.symbol}</td>
              <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{stock.price.toFixed(2)} USD</td>
              <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>
                <button 
                  onClick={() => removeStock(stock.symbol)}
                  style={{ padding: '6px 12px', borderRadius: '5px', backgroundColor: '#f44336', color: 'white', border: 'none', cursor: 'pointer' }}
                >
                  Entfernen
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
