export interface Restaurant {
    id: number;
    name: string;
    area: string;
    cuisine: string;
    address: string | null;
    description: string | null;
}

export type RestaurantInput = Omit<Restaurant, "id">;