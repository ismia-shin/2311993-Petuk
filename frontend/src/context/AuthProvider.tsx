import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import {
    refreshAccessToken,
    setAccessToken,
    setSessionExpiredHandler,
} from "../services/api";
import * as authApi from "../services/authApi";
import type { User } from "../types/user";
import { AuthContext } from "./authContext";

export default function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;
        setSessionExpiredHandler(() => setUser(null));

        async function restoreSession() {
            try {
                if (await refreshAccessToken()) {
                    const me = await authApi.getMe();
                    if (!cancelled) setUser(me);
                }
            } catch {
                // not logged in, stay a guest
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        restoreSession();

        return () => {
            cancelled = true;
            setSessionExpiredHandler(null);
        };
    }, []);

    async function login(email: string, password: string) {
        const { access_token } = await authApi.login({ email, password });
        setAccessToken(access_token);
        setUser(await authApi.getMe());
    }

    async function logout() {
        try {
            await authApi.logout();
        } finally {
            setAccessToken(null);
            setUser(null);
        }
    }

    async function logoutAll() {
        try {
            await authApi.logoutAll();
        } finally {
            setAccessToken(null);
            setUser(null);
        }
    }

    return (
        <AuthContext.Provider
            value={{ user, loading, login, logout, logoutAll, setUser }}
        >
            {children}
        </AuthContext.Provider>
    );
}