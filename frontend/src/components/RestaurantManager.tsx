import { useEffect, useState } from "react";
import type { SyntheticEvent } from "react";
import {
	createRestaurant,
	deleteRestaurant,
	getRestaurant,
	getRestaurants,
	updateRestaurant,
} from "../services/restaurantApi";
import type { Restaurant } from "../types/restaurant";
import "./RestaurantManager.css";

const emptyForm = {
	name: "",
	area: "",
	cuisine: "",
	address: "",
	description: "",
};

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

	// Runs once when the page opens
	useEffect(() => {
		loadRestaurants();
	}, []);

	// CREATE or UPDATE 
	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		const data = {
			name: form.name.trim(),
			area: form.area.trim(),
			cuisine: form.cuisine.trim(),
			address: form.address.trim() || null,
			description: form.description.trim() || null,
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
			area: restaurant.area,
			cuisine: restaurant.cuisine,
			address: restaurant.address ?? "",
			description: restaurant.description ?? "",
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
							maxLength={100}
							onChange={(e) => setForm({ ...form, name: e.target.value })}
							required
						/>
					</label>
					<label className="rm-field">
						<span>Area</span>
						<input
							placeholder="e.g. Mirpur"
							value={form.area}
							maxLength={100}
							onChange={(e) => setForm({ ...form, area: e.target.value })}
							required
						/>
					</label>
					<label className="rm-field">
						<span>Cuisine</span>
						<input
							placeholder="e.g. Bangladeshi"
							value={form.cuisine}
							maxLength={50}
							onChange={(e) => setForm({ ...form, cuisine: e.target.value })}
							required
						/>
					</label>
					<label className="rm-field">
						<span>Address (optional)</span>
						<input
							placeholder="e.g. Road 3, Mirpur 10"
							value={form.address}
							maxLength={255}
							onChange={(e) => setForm({ ...form, address: e.target.value })}
						/>
					</label>
					<label className="rm-field rm-field-wide">
						<span>Description (optional)</span>
						<textarea
							placeholder="What makes this place special?"
							rows={3}
							value={form.description}
							maxLength={500}
							onChange={(e) =>
								setForm({ ...form, description: e.target.value })
							}
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
						<strong>Area:</strong> {selected.area}
					</p>
					<p>
						<strong>Cuisine:</strong> {selected.cuisine}
					</p>
					{selected.address && (
						<p>
							<strong>Address:</strong> {selected.address}
						</p>
					)}
					{selected.description && (
						<p>
							<strong>About:</strong> {selected.description}
						</p>
					)}
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
								<span className="rm-area">&#128205; {r.area}</span>
							</div>
							<span className="rm-cuisine">{r.cuisine}</span>
							{r.description && <p className="rm-desc">{r.description}</p>}
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