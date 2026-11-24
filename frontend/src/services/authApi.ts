import type {
    LoginInput,
    SignupInput,
    TokenResponse,
    User,
} from "../types/user";
import { request } from "./api";

const AUTH_URL = "/api/v1/auth";
const USERS_URL = "/api/v1/users";

export function signup(data: SignupInput): Promise<User> {
    return request<User>(`${AUTH_URL}/signup`, {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function login(data: LoginInput): Promise<TokenResponse> {
    return request<TokenResponse>(`${AUTH_URL}/login`, {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function logout(): Promise<void> {
    return request<void>(`${AUTH_URL}/logout`, { method: "POST" });
}

export function logoutAll(): Promise<void> {
    return request<void>(`${AUTH_URL}/logout-all`, { method: "POST" });
}

export function getMe(): Promise<User> {
    return request<User>(`${USERS_URL}/me`);
}

export function updateProfile(name: string): Promise<User> {
    return request<User>(`${USERS_URL}/me`, {
        method: "PUT",
        body: JSON.stringify({ name }),
    });
}

export function changePassword(
    currentPassword: string,
    newPassword: string,
): Promise<void> {
    return request<void>(`${USERS_URL}/me/password`, {
        method: "PUT",
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
        }),
    });
}