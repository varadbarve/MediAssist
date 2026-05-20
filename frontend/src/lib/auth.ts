/**
 * Layer 9 — Frontend Auth Utility
 * Handles JWT token storage, login, registration, logout, and auth checks.
 */

const API_URL = "https://mediassist-backend-1bom.onrender.com";

// --- Types ---
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface AuthError {
  detail: string;
}

// --- Token Management ---

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("mediassist_token");
}

export function getUser(): User | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("mediassist_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function saveAuth(token: string, user: User): void {
  localStorage.setItem("mediassist_token", token);
  localStorage.setItem("mediassist_user", JSON.stringify(user));
}

export function clearAuth(): void {
  localStorage.removeItem("mediassist_token");
  localStorage.removeItem("mediassist_user");
}

// --- Auth State ---

export function isAuthenticated(): boolean {
  const token = getToken();
  if (!token) return false;

  // Basic JWT expiry check (decode payload without verification)
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    const expiry = payload.exp * 1000; // Convert to ms
    return Date.now() < expiry;
  } catch {
    return false;
  }
}

// --- API Calls ---

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error: AuthError = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  const data: LoginResponse = await response.json();
  saveAuth(data.access_token, data.user);
  return data;
}

export async function register(
  email: string,
  password: string,
  full_name: string,
  role: string = "staff"
): Promise<User> {
  const response = await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name, role }),
  });

  if (!response.ok) {
    const error: AuthError = await response.json();
    throw new Error(error.detail || "Registration failed");
  }

  return response.json();
}

export function logout(): void {
  clearAuth();
  window.location.href = "/login";
}

/**
 * Get Authorization headers for authenticated API requests.
 */
export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}
