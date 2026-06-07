const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
  params?: Record<string, string>;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, headers = {}, params } = options;

  let url = `${API_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }

  const token = getStoredToken();

  const config: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
  };

  if (body && method !== "GET") {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const stored = localStorage.getItem("email_insight_tokens");
    if (stored) {
      const tokens = JSON.parse(stored);
      return tokens.access_token;
    }
  } catch {
    return null;
  }
  return null;
}

export function setStoredTokens(tokens: { access_token: string; refresh_token: string }): void {
  localStorage.setItem("email_insight_tokens", JSON.stringify(tokens));
}

export function clearStoredTokens(): void {
  localStorage.removeItem("email_insight_tokens");
  localStorage.removeItem("email_insight_user");
}

export function setStoredUser(user: unknown): void {
  localStorage.setItem("email_insight_user", JSON.stringify(user));
}

export function getStoredUser<T>(): T | null {
  if (typeof window === "undefined") return null;
  try {
    const stored = localStorage.getItem("email_insight_user");
    return stored ? JSON.parse(stored) : null;
  } catch {
    return null;
  }
}

export const api = {
  auth: {
    register: (data: { email: string; username: string; password: string; full_name?: string; company?: string }) =>
      request<import("@/types").AuthTokens>("/api/auth/register", { method: "POST", body: data }),
    login: (data: { email: string; password: string }) =>
      request<import("@/types").AuthTokens>("/api/auth/login", { method: "POST", body: data }),
    me: () => request<import("@/types").User>("/api/auth/me"),
    logout: () => { clearStoredTokens(); },
    refresh: (refreshToken: string) =>
      request<import("@/types").AuthTokens>("/api/auth/refresh", { method: "POST", body: { refresh_token: refreshToken } }),
    changePassword: (data: { current_password: string; new_password: string }) =>
      request<{ message: string }>("/api/auth/change-password", { method: "POST", body: data }),
    forgotPassword: (data: { email: string }) =>
      request<{ message: string; reset_token?: string }>("/api/auth/forgot-password", { method: "POST", body: data }),
    resetPassword: (data: { token: string; new_password: string }) =>
      request<{ message: string }>("/api/auth/reset-password", { method: "POST", body: data }),
  },
  email: {
    lookup: (data: { email: string }) =>
      request<import("@/types").SearchResult>("/api/email/lookup", { method: "POST", body: data }),
    gravatar: (email: string) =>
      request<{ url: string | null; has_gravatar: boolean }>("/api/email/gravatar", { params: { email } }),
  },
  domain: {
    lookup: (domain: string) =>
      request<import("@/types").DomainResult>("/api/domain/lookup", { params: { domain } }),
    dns: (domain: string) =>
      request<{ records: import("@/types").DNSRecord[] }>("/api/domain/dns", { params: { domain } }),
    whois: (domain: string) =>
      request<import("@/types").WhoisInfo>("/api/domain/whois", { params: { domain } }),
    security: (domain: string) =>
      request<{ spf: string | null; dkim: string | null; dmarc: string | null; security_score: number }>(
        "/api/domain/security", { params: { domain } }
      ),
  },
  company: {
    lookup: (domain: string) =>
      request<import("@/types").CompanyInfo>("/api/company/lookup", { params: { domain } }),
    techStack: (domain: string) =>
      request<{ domain: string; technologies: string[] }>("/api/company/tech-stack", { params: { domain } }),
    social: (domain: string) =>
      request<{ domain: string; social_media: Record<string, string> }>("/api/company/social", { params: { domain } }),
  },
  search: {
    history: (params?: { page?: number; per_page?: number; search_type?: string }) =>
      request<import("@/types").SearchHistoryItem[]>("/api/search/history", { params: params as Record<string, string> }),
    analytics: () =>
      request<import("@/types").SearchAnalytics>("/api/search/analytics"),
    detail: (id: string) =>
      request<import("@/types").SearchResult>(`/api/search/${id}`),
    delete: (id: string) =>
      request<{ message: string }>(`/api/search/${id}`, { method: "DELETE" }),
    export: (data: { search_ids: string[]; format_type: string }) =>
      request<Blob>("/api/search/export", { method: "POST", body: data }),
  },
  dashboard: {
    stats: () =>
      request<import("@/types").DashboardStats>("/api/dashboard/stats"),
  },
};
