export interface Restaurant {
    id: number;
    name: string;
    cuisine: string;
    rating: number;
}

export type RestaurantInput = Omit<Restaurant, "id">;