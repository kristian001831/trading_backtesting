import type { Trade } from '../types/backtest';

type Props = {
  trades: Trade[];
};

export default function TradeListTable({ trades }: Props) {
  return (
    <section className="card">
      <h2>Trade List</h2>
      {trades.length === 0 ? (
        <p>No trades available.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Side</th>
                <th>Entry</th>
                <th>Exit</th>
                <th>Entry Px</th>
                <th>Exit Px</th>
                <th>PNL</th>
                <th>PNL %</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade) => (
                <tr key={trade.id}>
                  <td>{trade.id}</td>
                  <td>{trade.side}</td>
                  <td>{new Date(trade.entryTime).toLocaleString()}</td>
                  <td>{new Date(trade.exitTime).toLocaleString()}</td>
                  <td>{trade.entryPrice.toFixed(2)}</td>
                  <td>{trade.exitPrice.toFixed(2)}</td>
                  <td>{trade.pnl.toFixed(2)}</td>
                  <td>{trade.pnlPercent.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
