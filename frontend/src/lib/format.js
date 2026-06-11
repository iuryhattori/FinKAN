// Rótulo curto de horário para ticks de eixo (recebe timestamp em ms).
export function formatTickTime(value) {
  if (typeof value !== 'number') return value;
  return new Date(value).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

// Data e hora completas para tooltips (recebe timestamp em ms).
export function formatFullTime(value) {
  if (typeof value !== 'number') return value;
  const d = new Date(value);
  const date = d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  const time = d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  return `${date} · ${time}`;
}

// Formata volume de negociação com sufixo adaptativo (K/M/B).
// O tick volume real da B3 fica na casa de milhares; o formato fixo em
// milhões exibiria "0.0M" para dados reais.
export function formatVolume(value) {
  if (value == null || Number.isNaN(value)) return '—';
  const abs = Math.abs(value);
  if (abs >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
  return String(Math.round(value));
}
