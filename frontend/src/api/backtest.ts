import type { BacktestResult, BacktestRunRequest, RunResponse } from '../types/backtest';

const API_BASE = '/api/backtest';

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const fallback = `Request failed (${response.status})`;
    try {
      const error = (await response.json()) as { message?: string };
      throw new Error(error.message ?? fallback);
    } catch {
      throw new Error(fallback);
    }
  }

  return (await response.json()) as T;
}

export async function runBacktest(payload: BacktestRunRequest): Promise<RunResponse> {
  const response = await fetch(`${API_BASE}/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  return parseJson<RunResponse>(response);
}

export async function getBacktestResult(id: string): Promise<BacktestResult> {
  const response = await fetch(`${API_BASE}/result/${id}`);
  return parseJson<BacktestResult>(response);
}
