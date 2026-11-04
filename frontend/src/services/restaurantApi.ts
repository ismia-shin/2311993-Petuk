export interface Restaurant {
	id: number;
	name: string;
	cuisine: string;
	rating: number;
}

export type RestaurantInput = Omit<Restaurant, "id">;

const BASE_URL = "/api/v1/restaurants";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
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
		} catch {
			// response had no JSON body; keep the default message
		}
		throw new Error(message);
	}

	if (response.status === 204) {
		return undefined as T; 
	}
	return response.json() as Promise<T>;
}

// Read List
export function getRestaurants(): Promise<Restaurant[]> {
	return request<Restaurant[]>(BASE_URL);
}

// Read Single
export function getRestaurant(id: number): Promise<Restaurant> {
	return request<Restaurant>(`${BASE_URL}/${id}`);
}

// Create
export function createRestaurant(data: RestaurantInput): Promise<Restaurant> {
	return request<Restaurant>(BASE_URL, {
		method: "POST",
		body: JSON.stringify(data),
	});
}

// Update
export function updateRestaurant(
	id: number,
	data: RestaurantInput,
): Promise<Restaurant> {
	return request<Restaurant>(`${BASE_URL}/${id}`, {
		method: "PUT",
		body: JSON.stringify(data),
	});
}

// Delete
export function deleteRestaurant(id: number): Promise<void> {
	return request<void>(`${BASE_URL}/${id}`, { method: "DELETE" });
}
