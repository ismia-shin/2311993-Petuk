import type { Restaurant } from "../types/restaurant";
import type { Review } from "../types/review";
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

export function canWriteReview(user: User | null): boolean {
    return user !== null && user.role === "customer";
}

export function canEditReview(user: User | null, review: Review): boolean {
    return user !== null && review.user_id === user.id;
}

export function canDeleteReview(user: User | null, review: Review): boolean {
    return user !== null && (user.role === "admin" || review.user_id === user.id);
}