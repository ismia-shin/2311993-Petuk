import type { MenuItem, MenuItemInput } from "../types/menu";
import { request } from "./api";

const RESTAURANTS_URL = "/api/v1/restaurants";
const MENU_ITEMS_URL = "/api/v1/menu-items";

export function getMenuItems(restaurantId: number): Promise<MenuItem[]> {
    return request<MenuItem[]>(`${RESTAURANTS_URL}/${restaurantId}/menu-items`);
}

export function createMenuItem(
    restaurantId: number,
    data: MenuItemInput,
): Promise<MenuItem> {
    return request<MenuItem>(`${RESTAURANTS_URL}/${restaurantId}/menu-items`, {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function updateMenuItem(
    id: number,
    data: MenuItemInput,
): Promise<MenuItem> {
    return request<MenuItem>(`${MENU_ITEMS_URL}/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

export function deleteMenuItem(id: number): Promise<void> {
    return request<void>(`${MENU_ITEMS_URL}/${id}`, { method: "DELETE" });
}