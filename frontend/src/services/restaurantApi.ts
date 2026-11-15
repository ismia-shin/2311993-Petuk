import type { Restaurant, RestaurantInput } from "../types/restaurant";
import { request } from "./api";

const BASE_URL = "/api/v1/restaurants";

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