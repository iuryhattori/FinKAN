import { Target } from 'lucide-react';

function mae(history) {
  return history.reduce((acc, r) => acc + Math.abs(r.error), 0) / history.length;
}

function accuracyTone(errorPercent) {
  if (errorPercent < 0.5) return { label: 'No alvo', color: 'var(--up)', bg: 'var(--up-bg)' };
  if (errorPercent < 1) return { label: 'Próximo', color: 'var(--warn)', bg: 'var(--warn-bg)' };
  return { label: 'Desviou', color: 'var(--down)', bg: 'var(--down-bg)' };
}

const columns = [
  { label: 'Horário', align: 'left' },
  { label: 'Projetado', align: 'right' },
  { label: 'Realizado', align: 'right' },
  { label: 'Diferença', align: 'right' },
  { label: 'Erro', align: 'right' },
  { label: 'Avaliação', align: 'right' },
];

export function PredictionHistoryTable({ history }) {
  const avgError = mae(history);
  const avgErrorPct = (avgError / history[0].actualClose) * 100;

  return (
    <section className="panel overflow-hidden" aria-label="Precisão das projeções PETR4">
      <div
        className="flex items-center justify-between px-4 py-3 border-b"
        style={{ backgroundColor: 'var(--muted)', borderColor: 'var(--panel-border)' }}
      >
        <div className="flex items-center gap-3">
          <Target className="w-3.5 h-3.5" style={{ color: 'var(--brand)' }} aria-hidden="true" />
          <div className="leading-tight">
            <p className="text-xs" style={{ color: 'var(--foreground)' }}>
              Precisão do modelo
            </p>
            <p className="text-[10px]" style={{ color: 'var(--muted-foreground)' }}>
              Cada projeção comparada com o preço que de fato se realizou
            </p>
          </div>
        </div>
        <dl className="flex items-center gap-5 text-[10px] font-data">
          <div className="flex items-center gap-1.5" title="Erro médio absoluto das projeções">
            <dt style={{ color: 'var(--muted-foreground)' }}>Erro médio:</dt>
            <dd style={{ color: 'var(--foreground)' }}>R$ {avgError.toFixed(3)}</dd>
          </div>
          <div className="flex items-center gap-1.5" title="Erro percentual médio das projeções">
            <dt style={{ color: 'var(--muted-foreground)' }}>Em %:</dt>
            <dd style={{ color: 'var(--foreground)' }}>{avgErrorPct.toFixed(3)}%</dd>
          </div>
          <div className="flex items-center gap-1.5">
            <dt style={{ color: 'var(--muted-foreground)' }}>Projeções:</dt>
            <dd style={{ color: 'var(--foreground)' }}>{history.length}</dd>
          </div>
        </dl>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b" style={{ borderColor: 'var(--panel-border)' }}>
              {columns.map((col) => (
                <th
                  key={col.label}
                  scope="col"
                  className={`py-2.5 px-4 text-[10px] uppercase tracking-widest font-medium text-${col.align}`}
                  style={{ color: 'var(--muted-foreground)' }}
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {history.map((record, index) => {
              const errorPercent = Math.abs((record.error / record.actualClose) * 100);
              const tone = accuracyTone(errorPercent);

              return (
                <tr
                  key={index}
                  className="border-b transition-colors hover:bg-[rgba(255,255,255,0.02)]"
                  style={{ borderColor: 'var(--panel-border)' }}
                >
                  <td className="py-3 px-4">
                    <span className="text-xs font-data" style={{ color: 'var(--foreground)' }}>
                      {new Date(record.timestamp).toLocaleTimeString('pt-BR')}
                    </span>
                    <span className="text-[10px] ml-2 font-data" style={{ color: 'var(--muted-foreground)' }}>
                      {new Date(record.timestamp).toLocaleDateString('pt-BR')}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right text-xs font-data" style={{ color: 'var(--secondary-foreground)' }}>
                    R$ {record.predictedClose.toFixed(2)}
                  </td>
                  <td className="py-3 px-4 text-right text-xs font-data" style={{ color: 'var(--foreground)' }}>
                    R$ {record.actualClose.toFixed(2)}
                  </td>
                  <td
                    className="py-3 px-4 text-right text-xs font-data"
                    style={{ color: record.error >= 0 ? 'var(--down)' : 'var(--up)' }}
                  >
                    {record.error > 0 ? '+' : ''}{record.error.toFixed(3)}
                  </td>
                  <td className="py-3 px-4 text-right text-xs">
                    <span
                      className="px-1.5 py-0.5 rounded-sm text-[10px] font-data"
                      style={{ color: tone.color, backgroundColor: tone.bg }}
                    >
                      {errorPercent.toFixed(3)}%
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <span
                      className="inline-block text-[9px] px-2 py-0.5 rounded-sm uppercase tracking-widest border"
                      style={{ color: tone.color, borderColor: tone.bg, backgroundColor: 'transparent' }}
                    >
                      {tone.label}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
