type Props = {
  disabled: boolean;
  loading: boolean;
  onClick: () => void;
};

export default function RunBacktestButton({ disabled, loading, onClick }: Props) {
  return (
    <button className="run-button" onClick={onClick} disabled={disabled || loading}>
      {loading ? 'Running backtest...' : 'Run Backtest'}
    </button>
  );
}
