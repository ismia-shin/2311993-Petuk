export type Role = "customer" | "owner" | "admin";

export interface User {
    id: number;
    email: string;
    name: string;
    role: Role;
}

export interface LoginInput {
    email: string;
    password: string;
}

export interface SignupInput {
    email: string;
    name: string;
    password: string;
    role: "customer" | "owner";
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}