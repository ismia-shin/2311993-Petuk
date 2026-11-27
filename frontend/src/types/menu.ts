export interface MenuItem {
    id: number;
    restaurant_id: number;
    name: string;
    price: number;
    description: string | null;
}

export type MenuItemInput = Omit<MenuItem, "id" | "restaurant_id">;