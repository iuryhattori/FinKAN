// Cliente HTTP central: toda comunicação com o backend passa por aqui.
// Componentes e hooks nunca chamam fetch diretamente.

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

const DEFAULT_TIMEOUT_MS = 10000;

export class ApiError extends Error {
  constructor(message, { status = null, url = null, cause = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.url = url;
    this.cause = cause;
  }
}

/**
 * GET que retorna JSON. Lança ApiError em falha de rede, timeout ou status não-2xx.
 */
export async function getJson(path, { signal, timeoutMs = DEFAULT_TIMEOUT_MS } = {}) {
  const url = `${API_BASE_URL}${path}`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  signal?.addEventListener('abort', () => controller.abort(), { once: true });

  let response;
  try {
    response = await fetch(url, {
      signal: controller.signal,
      headers: { Accept: 'application/json' },
    });
  } catch (cause) {
    throw new ApiError(
      cause.name === 'AbortError'
        ? `Request to ${path} timed out`
        : `Network failure while calling ${path}`,
      { url, cause },
    );
  } finally {
    clearTimeout(timeout);
  }

  if (!response.ok) {
    throw new ApiError(`API responded ${response.status} on ${path}`, {
      status: response.status,
      url,
    });
  }

  try {
    return await response.json();
  } catch (cause) {
    throw new ApiError(`Response from ${path} is not valid JSON`, { url, cause });
  }
}
