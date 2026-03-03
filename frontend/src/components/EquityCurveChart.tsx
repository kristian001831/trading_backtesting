import type { EquityPoint } from '../types/backtest';

type Props = {
  points: EquityPoint[];
};

export default function EquityCurveChart({ points }: Props) {
  return (
    <section className="card">
      <h2>Equity Curve</h2>
      {points.length === 0 ? (
        <p>No equity data available.</p>
      ) : (
        <svg viewBox="0 0 600 240" className="equity-chart" role="img" aria-label="Equity curve chart">
          <polyline
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            points={buildPolyline(points)}
          />
        </svg>
      )}
    </section>
  );
}

function buildPolyline(points: EquityPoint[]): string {
  const values = points.map((point) => point.equity);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  return points
    .map((point, index) => {
      const x = (index / Math.max(points.length - 1, 1)) * 600;
      const y = 220 - ((point.equity - min) / range) * 200;
      return `${x},${y}`;
    })
    .join(' ');
}
