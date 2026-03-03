import { useEffect, useMemo, useState } from 'react';
import { getBacktestResult, runBacktest } from './api/backtest';
import EquityCurveChart from './components/EquityCurveChart';
import ResultsSummary from './components/ResultsSummary';
import RunBacktestButton from './components/RunBacktestButton';
import StrategyConfigForm from './components/StrategyConfigForm';
import TradeListTable from './components/TradeListTable';
import type { BacktestResult, StrategyConfig } from './types/backtest';

const STORAGE_KEY = 'recent-backtest-runs';
const MAX_RECENT = 10;

const initialConfig: StrategyConfig = {
  strategyName: 'Moving Average Crossover',
  symbol: 'BTCUSDT',
  timeframe: '1h',
  initialCapital: 10000,
  feePercent: 0.1,
  slippagePercent: 0.05,
  parameters: {
    fastPeriod: 20,
    slowPeriod: 50
  }
};

export default function App() {
  const [config, setConfig] = useState<StrategyConfig>(initialConfig);
  const [errors, setErrors] = useState<Partial<Record<keyof StrategyConfig | 'parameters', string>>>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string>('');
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [recentRuns, setRecentRuns] = useState<BacktestResult[]>([]);

  useEffect(() => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    try {
      setRecentRuns(JSON.parse(raw) as BacktestResult[]);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recentRuns));
  }, [recentRuns]);

  const canRun = useMemo(() => !loading, [loading]);

  const validate = (): boolean => {
    const nextErrors: Partial<Record<keyof StrategyConfig | 'parameters', string>> = {};

    if (!config.strategyName.trim()) nextErrors.strategyName = 'Strategy name is required.';
    if (!config.symbol.trim()) nextErrors.symbol = 'Symbol is required.';
    if (!config.timeframe.trim()) nextErrors.timeframe = 'Timeframe is required.';
    if (config.initialCapital <= 0) nextErrors.initialCapital = 'Initial capital must be greater than 0.';
    if (config.feePercent < 0) nextErrors.feePercent = 'Fee cannot be negative.';
    if (config.slippagePercent < 0) nextErrors.slippagePercent = 'Slippage cannot be negative.';
    if (Object.keys(config.parameters).length === 0) nextErrors.parameters = 'Add at least one strategy parameter.';

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const saveRun = (next: BacktestResult) => {
    setRecentRuns((current) => {
      const merged = [next, ...current.filter((item) => item.id !== next.id)];
      return merged.slice(0, MAX_RECENT);
    });
  };

  const pollUntilDone = async (id: string): Promise<BacktestResult> => {
    while (true) {
      const snapshot = await getBacktestResult(id);
      if (snapshot.status === 'completed' || snapshot.status === 'failed') return snapshot;
      await new Promise((resolve) => setTimeout(resolve, 1500));
    }
  };

  const handleRun = async () => {
    if (!validate()) return;

    setLoading(true);
    setMessage('Submitting backtest job...');

    try {
      const run = await runBacktest({ config });
      setMessage(`Job ${run.id} submitted. Waiting for completion...`);
      const completed = await pollUntilDone(run.id);
      setResult(completed);
      saveRun(completed);
      setMessage(completed.status === 'completed' ? 'Backtest finished.' : completed.error ?? 'Backtest failed.');
    } catch (error) {
      const detail = error instanceof Error ? error.message : 'Unknown error';
      setMessage(`Run failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Trading Backtest Runner</h1>
      <StrategyConfigForm value={config} errors={errors} onChange={setConfig} />
      <div className="actions card">
        <RunBacktestButton disabled={!canRun} loading={loading} onClick={handleRun} />
        <p>{message || 'Fill in strategy settings and run a backtest.'}</p>
      </div>

      <section className="card">
        <h2>Recent Runs</h2>
        {recentRuns.length === 0 ? (
          <p>No recent runs yet.</p>
        ) : (
          <ul className="recent-list">
            {recentRuns.map((run) => (
              <li key={run.id}>
                <button className="link-button" onClick={() => setResult(run)}>
                  <strong>{run.id}</strong> — {run.symbol} {run.timeframe} — {run.status}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <ResultsSummary result={result} />
      <EquityCurveChart points={result?.equityCurve ?? []} />
      <TradeListTable trades={result?.trades ?? []} />
    </main>
  );
}
