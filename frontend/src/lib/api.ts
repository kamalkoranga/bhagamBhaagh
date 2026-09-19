const BASE_URL = '/api/v1';

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token =
    typeof window !== 'undefined'
      ? localStorage.getItem('token')
      : null;

  const headers = {
    'Content-Type': 'application/json',
    ...(token && {
      Authorization: `Bearer ${token}`
    }),
    ...options.headers
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let message = `HTTP Error ${response.status}`;

    try {
      const data = await response.json();
      if (data.detail) {
        message =
          typeof data.detail === 'string'
            ? data.detail
            : JSON.stringify(data.detail);
      }
    } catch {
      message = 'Network or parsing error occured.'
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}
