import type { TokenResponse } from "../types/user";
import { HttpStatus } from "../utils/httpStatus";

let accessToken: string | null = null;
let onSessionExpired: (() => void) | null = null;
let refreshPromise: Promise<boolean> | null = null;

const NO_REFRESH_URLS = ["/auth/login", "/auth/signup", "/auth/refresh"];

export function setAccessToken(token: string | null): void {
	accessToken = token;
}

export function setSessionExpiredHandler(handler: (() => void) | null): void {
	onSessionExpired = handler;
}

async function doRefresh(): Promise<boolean> {
	try {
		const response = await fetch("/api/v1/auth/refresh", { method: "POST" });
		if (!response.ok) {
			accessToken = null;
			return false;
		}
		const data = (await response.json()) as TokenResponse;
		accessToken = data.access_token;
		return true;
	} catch {
		return false;
	}
}

export function refreshAccessToken(): Promise<boolean> {
	if (refreshPromise === null) {
		refreshPromise = doRefresh().finally(() => {
			refreshPromise = null;
		});
	}
	return refreshPromise;
}

function send(url: string, options?: RequestInit): Promise<Response> {
	const headers = new Headers(options?.headers);
	headers.set("Content-Type", "application/json");
	if (accessToken) {
		headers.set("Authorization", `Bearer ${accessToken}`);
	}
	return fetch(url, { ...options, headers });
}

async function readErrorMessage(response: Response): Promise<string> {
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
	} catch {
	}
	return message;
}

export async function request<T>(
	url: string,
	options?: RequestInit,
): Promise<T> {
	let response = await send(url, options);

	const canRefresh = !NO_REFRESH_URLS.some((part) => url.includes(part));
	if (response.status === HttpStatus.UNAUTHORIZED && canRefresh) {
		if (await refreshAccessToken()) {
			response = await send(url, options);
		}
		if (response.status === HttpStatus.UNAUTHORIZED) {
			onSessionExpired?.();
		}
	}

	if (!response.ok) {
		throw new Error(await readErrorMessage(response));
	}
	if (response.status === HttpStatus.NO_CONTENT) {
		return undefined as T;
	}
	return response.json() as Promise<T>;
}
