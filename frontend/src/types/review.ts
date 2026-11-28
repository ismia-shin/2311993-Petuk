import type { RatingCategory } from "../utils/ratings";

export type RatingScores = Record<RatingCategory, number>;

export interface Review extends RatingScores {
    id: number;
    restaurant_id: number;
    user_id: number;
    user_name: string;
    comment: string | null;
    created_at: string;
}

export interface ReviewInput extends RatingScores {
    comment: string | null;
}

export interface RatingSummary extends Record<RatingCategory, number | null> {
    count: number;
    overall: number | null;
}