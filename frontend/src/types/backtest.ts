export type StrategyConfig = {
  strategyName: string;
  symbol: string;
  timeframe: string;
  initialCapital: number;
  feePercent: number;
  slippagePercent: number;
  parameters: Record<string, string | number>;
};

export type BacktestRunRequest = {
  config: StrategyConfig;
};

export type Trade = {
  id: string;
  entryTime: string;
  exitTime: string;
  side: 'long' | 'short';
  entryPrice: number;
  exitPrice: number;
  pnl: number;
  pnlPercent: number;
};

export type EquityPoint = {
  timestamp: string;
  equity: number;
};

export type BacktestResult = {
  id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  createdAt: string;
  symbol: string;
  timeframe: string;
  metrics?: {
    totalReturnPercent: number;
    sharpeRatio: number;
    maxDrawdownPercent: number;
    winRatePercent: number;
    totalTrades: number;
    netProfit: number;
  };
  equityCurve?: EquityPoint[];
  trades?: Trade[];
  error?: string;
};

export type RunResponse = {
  id: string;
  status: 'queued' | 'running';
};
