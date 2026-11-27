import { useEffect, useState } from "react";
import type { SyntheticEvent } from "react";
import { useAuth } from "../hooks/useAuth";
import {
	createMenuItem,
	deleteMenuItem,
	getMenuItems,
	updateMenuItem,
} from "../services/menuApi";
import type { MenuItem } from "../types/menu";
import type { Restaurant } from "../types/restaurant";
import { getErrorMessage } from "../utils/errors";
import { canManageRestaurant } from "../utils/permissions";
import "./MenuSection.css";

const emptyForm = { name: "", price: "", description: "" };

export default function MenuSection({ restaurant }: { restaurant: Restaurant }) {
	const { user } = useAuth();
	const canManage = canManageRestaurant(user, restaurant);

	const [items, setItems] = useState<MenuItem[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");
	const [form, setForm] = useState(emptyForm);
	const [editingId, setEditingId] = useState<number | null>(null);

	useEffect(() => {
		let cancelled = false;
		getMenuItems(restaurant.id)
			.then((data) => {
				if (!cancelled) setItems(data);
			})
			.catch((err) => {
				if (!cancelled) setError(getErrorMessage(err));
			})
			.finally(() => {
				if (!cancelled) setLoading(false);
			});
		return () => {
			cancelled = true;
		};
	}, [restaurant.id]);

	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setError("");
		const data = {
			name: form.name.trim(),
			price: Number(form.price),
			description: form.description.trim() || null,
		};
		try {
			if (editingId === null) {
				await createMenuItem(restaurant.id, data);
			} else {
				await updateMenuItem(editingId, data);
			}
			setForm(emptyForm);
			setEditingId(null);
			setItems(await getMenuItems(restaurant.id));
		} catch (err) {
			setError(getErrorMessage(err));
		}
	}

	function handleEdit(item: MenuItem) {
		setEditingId(item.id);
		setForm({
			name: item.name,
			price: String(item.price),
			description: item.description ?? "",
		});
	}

	function handleCancelEdit() {
		setEditingId(null);
		setForm(emptyForm);
	}

	async function handleDelete(id: number) {
		if (!window.confirm("Delete this dish?")) return;
		try {
			setError("");
			await deleteMenuItem(id);
			if (editingId === id) handleCancelEdit();
			setItems(await getMenuItems(restaurant.id));
		} catch (err) {
			setError(getErrorMessage(err));
		}
	}

	return (
		<div className="menu">
			<h3>Menu</h3>
			{error && <p className="rm-error">{error}</p>}
			{loading && <p className="rm-note">Loading menu...</p>}
			{!loading && items.length === 0 && (
				<p className="rm-note">No dishes on the menu yet.</p>
			)}

			<ul className="menu-list">
				{items.map((item) => (
					<li key={item.id} className="menu-item">
						<div>
							<strong>{item.name}</strong>
							{item.description && (
								<div className="menu-desc">{item.description}</div>
							)}
						</div>
						<div className="menu-right">
							<span className="menu-price">&#2547; {item.price.toFixed(2)}</span>
							{canManage && (
								<>
									<button
										type="button"
										className="btn btn-small btn-soft"
										onClick={() => handleEdit(item)}
									>
										Edit
									</button>
									<button
										type="button"
										className="btn btn-small btn-danger"
										onClick={() => handleDelete(item.id)}
									>
										Delete
									</button>
								</>
							)}
						</div>
					</li>
				))}
			</ul>

			{canManage && (
				<form className="menu-form" onSubmit={handleSubmit}>
					<input
						aria-label="Dish name"
						placeholder="Dish name"
						value={form.name}
						maxLength={100}
						onChange={(e) => setForm({ ...form, name: e.target.value })}
						required
					/>
					<input
						aria-label="Price in taka"
						type="number"
						placeholder="Price (BDT)"
						min="0"
						step="0.01"
						value={form.price}
						onChange={(e) => setForm({ ...form, price: e.target.value })}
						required
					/>
					<input
						aria-label="Description"
						placeholder="Description (optional)"
						value={form.description}
						maxLength={255}
						onChange={(e) => setForm({ ...form, description: e.target.value })}
					/>
					<div className="menu-form-actions">
						<button type="submit" className="btn btn-primary btn-small">
							{editingId === null ? "Add dish" : "Save dish"}
						</button>
						{editingId !== null && (
							<button
								type="button"
								className="btn btn-ghost btn-small"
								onClick={handleCancelEdit}
							>
								Cancel
							</button>
						)}
					</div>
				</form>
			)}
		</div>
	);
}