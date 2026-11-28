export const RATING_CATEGORIES = [
    "taste",
    "atmosphere",
    "cleanliness",
    "price",
    "service",
] as const;

export type RatingCategory = (typeof RATING_CATEGORIES)[number];

export const RATING_LABELS: Record<RatingCategory, string> = {
    taste: "Taste",
    atmosphere: "Atmosphere",
    cleanliness: "Cleanliness",
    price: "Price (value)",
    service: "Service",
};

export function formatRating(value: number | null): string {
    return value === null ? "-" : value.toFixed(1);
}