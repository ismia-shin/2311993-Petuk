import type { Review, ReviewInput } from "../types/review";
import { request } from "./api";

const RESTAURANTS_URL = "/api/v1/restaurants";
const REVIEWS_URL = "/api/v1/reviews";

export function getReviews(restaurantId: number): Promise<Review[]> {
    return request<Review[]>(
        `${RESTAURANTS_URL}/${restaurantId}/reviews?limit=50`,
    );
}

export function createReview(
    restaurantId: number,
    data: ReviewInput,
): Promise<Review> {
    return request<Review>(`${RESTAURANTS_URL}/${restaurantId}/reviews`, {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export function updateReview(id: number, data: ReviewInput): Promise<Review> {
    return request<Review>(`${REVIEWS_URL}/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

export function deleteReview(id: number): Promise<void> {
    return request<void>(`${REVIEWS_URL}/${id}`, { method: "DELETE" });
}