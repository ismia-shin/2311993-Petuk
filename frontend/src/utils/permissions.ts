import type { Restaurant } from "../types/restaurant";
import type { User } from "../types/user";

export function canCreateRestaurant(user: User | null): boolean {
    return user !== null && (user.role === "owner" || user.role === "admin");
}

export function canManageRestaurant(
    user: User | null,
    restaurant: Restaurant,
): boolean {
    if (user === null) return false;
    if (user.role === "admin") return true;
    return user.role === "owner" && restaurant.owner_id === user.id;
}