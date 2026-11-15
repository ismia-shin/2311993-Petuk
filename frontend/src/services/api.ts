import { HttpStatus } from "../utils/httpStatus";

export async function request<T>(
    url: string,
    options?: RequestInit,
): Promise<T> {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });

    if (!response.ok) {
        let message = `Request failed (${response.status})`;
        try {
            const body = await response.json();
            if (typeof body.detail === "string") {
                message = body.detail; 
            } else if (Array.isArray(body.detail)) {
                message = body.detail
                .map((item: { msg: string }) => item.msg)
                .join(", ");
            }
        } catch {}
        throw new Error(message);
    }

    if (response.status === HttpStatus.NO_CONTENT) {
        return undefined as T;
    }
    return response.json() as Promise<T>;
}