import { ChangeEvent } from 'react';
import type { StrategyConfig } from '../types/backtest';

type Props = {
  value: StrategyConfig;
  errors: Partial<Record<keyof StrategyConfig | 'parameters', string>>;
  onChange: (next: StrategyConfig) => void;
};

function parseNumber(value: string): number {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

export default function StrategyConfigForm({ value, errors, onChange }: Props) {
  const handleField = <K extends keyof StrategyConfig>(field: K, raw: string) => {
    const next =
      field === 'initialCapital' || field === 'feePercent' || field === 'slippagePercent'
        ? parseNumber(raw)
        : raw;

    onChange({ ...value, [field]: next } as StrategyConfig);
  };

  const handleParameterChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const rows = event.target.value
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean);

    const parameters = rows.reduce<Record<string, string | number>>((acc, row) => {
      const [k, v] = row.split('=').map((cell) => cell.trim());
      if (!k || !v) return acc;
      const numeric = Number(v);
      acc[k] = Number.isFinite(numeric) ? numeric : v;
      return acc;
    }, {});

    onChange({ ...value, parameters });
  };

  return (
    <section className="card">
      <h2>Strategy Configuration</h2>
      <div className="grid two-col">
        <label>
          Strategy Name
          <input value={value.strategyName} onChange={(e) => handleField('strategyName', e.target.value)} />
          {errors.strategyName ? <span className="error">{errors.strategyName}</span> : null}
        </label>

        <label>
          Symbol
          <input value={value.symbol} onChange={(e) => handleField('symbol', e.target.value)} />
          {errors.symbol ? <span className="error">{errors.symbol}</span> : null}
        </label>

        <label>
          Timeframe
          <input value={value.timeframe} onChange={(e) => handleField('timeframe', e.target.value)} />
          {errors.timeframe ? <span className="error">{errors.timeframe}</span> : null}
        </label>

        <label>
          Initial Capital
          <input
            type="number"
            value={value.initialCapital}
            onChange={(e) => handleField('initialCapital', e.target.value)}
          />
          {errors.initialCapital ? <span className="error">{errors.initialCapital}</span> : null}
        </label>

        <label>
          Fee (%)
          <input type="number" value={value.feePercent} onChange={(e) => handleField('feePercent', e.target.value)} />
          {errors.feePercent ? <span className="error">{errors.feePercent}</span> : null}
        </label>

        <label>
          Slippage (%)
          <input
            type="number"
            value={value.slippagePercent}
            onChange={(e) => handleField('slippagePercent', e.target.value)}
          />
          {errors.slippagePercent ? <span className="error">{errors.slippagePercent}</span> : null}
        </label>
      </div>

      <label>
        Parameters (one per line, format: key=value)
        <textarea
          rows={5}
          defaultValue={Object.entries(value.parameters)
            .map(([k, v]) => `${k}=${v}`)
            .join('\n')}
          onChange={handleParameterChange}
        />
        {errors.parameters ? <span className="error">{errors.parameters}</span> : null}
      </label>
    </section>
  );
}
