import type { BacktestResult } from '../types/backtest';

type Props = {
  result: BacktestResult | null;
};

export default function ResultsSummary({ result }: Props) {
  if (!result) {
    return (
      <section className="card">
        <h2>Results Summary</h2>
        <p>No run selected yet.</p>
      </section>
    );
  }

  if (result.status !== 'completed' || !result.metrics) {
    return (
      <section className="card">
        <h2>Results Summary</h2>
        <p>Status: {result.status}</p>
        {result.error ? <p className="error">{result.error}</p> : null}
      </section>
    );
  }

  const { metrics } = result;

  return (
    <section className="card">
      <h2>Results Summary</h2>
      <div className="grid three-col">
        <Metric label="Total Return" value={`${metrics.totalReturnPercent.toFixed(2)}%`} />
        <Metric label="Sharpe Ratio" value={metrics.sharpeRatio.toFixed(2)} />
        <Metric label="Max Drawdown" value={`${metrics.maxDrawdownPercent.toFixed(2)}%`} />
        <Metric label="Win Rate" value={`${metrics.winRatePercent.toFixed(2)}%`} />
        <Metric label="Trades" value={String(metrics.totalTrades)} />
        <Metric label="Net Profit" value={metrics.netProfit.toFixed(2)} />
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}
