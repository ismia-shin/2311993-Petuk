import type { RatingSummary } from "./review";

export interface Restaurant {
    id: number;
    owner_id: number | null;
    name: string;
    area: string;
    cuisine: string;
    address: string | null;
    description: string | null;
    ratings: RatingSummary;
}

export type RestaurantInput = Omit<Restaurant, "id" | "owner_id" | "ratings">;