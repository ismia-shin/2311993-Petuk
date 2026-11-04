import { useEffect, useState } from "react";
import type { SyntheticEvent } from "react";
import {
	createRestaurant,
	deleteRestaurant,
	getRestaurant,
	getRestaurants,
	updateRestaurant,
} from "../services/restaurantApi";
import type { Restaurant } from "../services/restaurantApi";
import "./RestaurantManager.css";

const emptyForm = { name: "", cuisine: "", rating: "" };

export default function RestaurantManager() {
	const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");
	const [form, setForm] = useState(emptyForm);
	const [editingId, setEditingId] = useState<number | null>(null);
	const [selected, setSelected] = useState<Restaurant | null>(null);

	function showError(err: unknown) {
		setError(err instanceof Error ? err.message : "Something went wrong");
	}

	// READ LIST
	async function loadRestaurants() {
		try {
			setRestaurants(await getRestaurants());
		} catch (err) {
			showError(err);
		} finally {
			setLoading(false);
		}
	}

	useEffect(() => {
		loadRestaurants();
	}, []);

	// CREATE or UPDATE 
	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		const data = {
			name: form.name.trim(),
			cuisine: form.cuisine.trim(),
			rating: Number(form.rating),
		};
		try {
			setError("");
			if (editingId === null) {
				await createRestaurant(data);
			} else {
				await updateRestaurant(editingId, data);
			}
			setForm(emptyForm);
			setEditingId(null);
			await loadRestaurants();
		} catch (err) {
			showError(err);
		}
	}

	function handleEdit(restaurant: Restaurant) {
		setEditingId(restaurant.id);
		setForm({
			name: restaurant.name,
			cuisine: restaurant.cuisine,
			rating: String(restaurant.rating),
		});
		window.scrollTo({ top: 0, behavior: "smooth" });
	}

	function handleCancelEdit() {
		setEditingId(null);
		setForm(emptyForm);
	}

	// READ SINGLE
	async function handleView(id: number) {
		try {
			setError("");
			setSelected(await getRestaurant(id));
		} catch (err) {
			showError(err);
		}
	}

	// DELETE
	async function handleDelete(id: number) {
		if (!window.confirm("Delete this restaurant?")) return;
		try {
			setError("");
			await deleteRestaurant(id);
			if (selected?.id === id) setSelected(null);
			if (editingId === id) handleCancelEdit();
			await loadRestaurants();
		} catch (err) {
			showError(err);
		}
	}

	return (
		<div className="rm">
			<section className="rm-hero">
				<h1>Discover &amp; manage dining spots</h1>
				<p>Add, edit and organise your favourite places to eat.</p>
			</section>

			{error && <p className="rm-error">{error}</p>}

			<form className="rm-card rm-form" onSubmit={handleSubmit}>
				<h2>{editingId === null ? "Add a restaurant" : "Edit restaurant"}</h2>
				<div className="rm-fields">
					<label className="rm-field">
						<span>Name</span>
						<input
							placeholder="e.g. Kacchi Bhai"
							value={form.name}
							onChange={(e) => setForm({ ...form, name: e.target.value })}
							required
						/>
					</label>
					<label className="rm-field">
						<span>Cuisine</span>
						<input
							placeholder="e.g. Bangladeshi"
							value={form.cuisine}
							onChange={(e) => setForm({ ...form, cuisine: e.target.value })}
							required
						/>
					</label>
					<label className="rm-field">
						<span>Rating (0 - 5)</span>
						<input
							type="number"
							placeholder="4.5"
							min="0"
							max="5"
							step="0.1"
							value={form.rating}
							onChange={(e) => setForm({ ...form, rating: e.target.value })}
							required
						/>
					</label>
				</div>
				<div className="rm-row">
					<button type="submit" className="btn btn-primary">
						{editingId === null ? "Add restaurant" : "Save changes"}
					</button>
					{editingId !== null && (
						<button
							type="button"
							className="btn btn-ghost"
							onClick={handleCancelEdit}
						>
							Cancel
						</button>
					)}
				</div>
			</form>

			{selected && (
				<div className="rm-card rm-detail">
					<div className="rm-detail-head">
						<h2>{selected.name}</h2>
						<button
							type="button"
							className="rm-close"
							aria-label="Close details"
							onClick={() => setSelected(null)}
						>
							&times;
						</button>
					</div>
					<p>
						<strong>ID:</strong> #{selected.id}
					</p>
					<p>
						<strong>Cuisine:</strong> {selected.cuisine}
					</p>
					<p>
						<strong>Rating:</strong> {selected.rating} / 5
					</p>
				</div>
			)}

			<section>
				<h2 className="rm-section-title">All restaurants</h2>
				{loading && <p className="rm-note">Loading restaurants...</p>}
				{!loading && restaurants.length === 0 && (
					<p className="rm-note">No restaurants yet. Add the first one above.</p>
				)}
				<div className="rm-grid">
					{restaurants.map((r) => (
						<article key={r.id} className="rm-card rm-item">
							<div className="rm-item-top">
								<h3>{r.name}</h3>
								<span className="rm-rating">&#9733; {r.rating}</span>
							</div>
							<span className="rm-cuisine">{r.cuisine}</span>
							<div className="rm-row rm-item-actions">
								<button
									type="button"
									className="btn btn-small btn-ghost"
									onClick={() => handleView(r.id)}
								>
									View
								</button>
								<button
									type="button"
									className="btn btn-small btn-soft"
									onClick={() => handleEdit(r)}
								>
									Edit
								</button>
								<button
									type="button"
									className="btn btn-small btn-danger"
									onClick={() => handleDelete(r.id)}
								>
									Delete
								</button>
							</div>
						</article>
					))}
				</div>
			</section>
		</div>
	);
}
