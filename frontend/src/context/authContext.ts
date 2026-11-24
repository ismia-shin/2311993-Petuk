import { createContext } from "react";
import type { User } from "../types/user";

export interface AuthContextValue {
    user: User | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    logoutAll: () => Promise<void>;
    setUser: (user: User | null) => void;
}

export const AuthContext = createContext<AuthContextValue | undefined>(
    undefined,
);