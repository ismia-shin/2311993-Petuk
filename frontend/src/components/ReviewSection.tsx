import { useEffect, useState } from "react";
import type { SyntheticEvent } from "react";
import { useAuth } from "../hooks/useAuth";
import {
	createReview,
	deleteReview,
	getReviews,
	updateReview,
} from "../services/reviewApi";
import type { Restaurant } from "../types/restaurant";
import type { Review, ReviewInput } from "../types/review";
import { getErrorMessage } from "../utils/errors";
import {
	canDeleteReview,
	canEditReview,
	canWriteReview,
} from "../utils/permissions";
import {
	RATING_CATEGORIES,
	RATING_LABELS,
	formatRating,
} from "../utils/ratings";
import type { RatingCategory } from "../utils/ratings";
import "./ReviewSection.css";

interface Props {
	restaurant: Restaurant;
	onChanged: () => void;
}

const emptyForm = {
	taste: 5,
	atmosphere: 5,
	cleanliness: 5,
	price: 5,
	service: 5,
	comment: "",
};
const SCORES = [5, 4, 3, 2, 1];

export default function ReviewSection({ restaurant, onChanged }: Props) {
	const { user, loading: authLoading } = useAuth();
	const [reviews, setReviews] = useState<Review[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");
	const [form, setForm] = useState(emptyForm);
	const [editingId, setEditingId] = useState<number | null>(null);

	const ratings = restaurant.ratings;
	const myReview = reviews.find((r) => user !== null && r.user_id === user.id);
	const showForm =
		canWriteReview(user) && (editingId !== null || myReview === undefined);

	useEffect(() => {
		let cancelled = false;
		getReviews(restaurant.id)
			.then((data) => {
				if (!cancelled) setReviews(data);
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

	async function refresh() {
		setReviews(await getReviews(restaurant.id));
		onChanged();
	}

	function setScore(category: RatingCategory, value: number) {
		setForm((current) => ({ ...current, [category]: value }));
	}

	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setError("");
		const { comment, ...scores } = form;
		const data: ReviewInput = { ...scores, comment: comment.trim() || null };
		try {
			if (editingId === null) {
				await createReview(restaurant.id, data);
			} else {
				await updateReview(editingId, data);
			}
			setForm(emptyForm);
			setEditingId(null);
			await refresh();
		} catch (err) {
			setError(getErrorMessage(err));
		}
	}

	function handleEdit(review: Review) {
		setEditingId(review.id);
		setForm({
			taste: review.taste,
			atmosphere: review.atmosphere,
			cleanliness: review.cleanliness,
			price: review.price,
			service: review.service,
			comment: review.comment ?? "",
		});
	}

	function handleCancelEdit() {
		setEditingId(null);
		setForm(emptyForm);
	}

	async function handleDelete(id: number) {
		if (!window.confirm("Delete this review?")) return;
		try {
			setError("");
			await deleteReview(id);
			if (editingId === id) handleCancelEdit();
			await refresh();
		} catch (err) {
			setError(getErrorMessage(err));
		}
	}

	return (
		<div className="rv">
			<h3>Reviews</h3>

			{ratings.count > 0 && (
				<div className="rv-summary">
					<div className="rv-overall">
						<span className="rv-big">&#9733; {formatRating(ratings.overall)}</span>
						<span>
							{ratings.count} {ratings.count === 1 ? "review" : "reviews"}
						</span>
					</div>
					<ul className="rv-breakdown">
						{RATING_CATEGORIES.map((category) => (
							<li key={category}>
								<span>{RATING_LABELS[category]}</span>
								<strong>{formatRating(ratings[category])}</strong>
							</li>
						))}
					</ul>
				</div>
			)}

			{error && <p className="rm-error">{error}</p>}
			{loading && <p className="rm-note">Loading reviews...</p>}
			{!loading && reviews.length === 0 && (
				<p className="rm-note">No reviews yet.</p>
			)}

			<ul className="rv-list">
				{reviews.map((review) => (
					<li key={review.id} className="rv-item">
						<div className="rv-head">
							<strong>
								{review.user_name}
								{user !== null && review.user_id === user.id ? " (you)" : ""}
							</strong>
							<span className="rv-date">
								{new Date(review.created_at).toLocaleDateString()}
							</span>
						</div>
						<div className="rv-scores">
							{RATING_CATEGORIES.map((category) => (
								<span key={category}>
									{RATING_LABELS[category]} {review[category]}
								</span>
							))}
						</div>
						{review.comment && <p className="rv-comment">{review.comment}</p>}
						{(canEditReview(user, review) || canDeleteReview(user, review)) && (
							<div className="rm-row">
								{canEditReview(user, review) && (
									<button
										type="button"
										className="btn btn-small btn-soft"
										onClick={() => handleEdit(review)}
									>
										Edit
									</button>
								)}
								{canDeleteReview(user, review) && (
									<button
										type="button"
										className="btn btn-small btn-danger"
										onClick={() => handleDelete(review.id)}
									>
										Delete
									</button>
								)}
							</div>
						)}
					</li>
				))}
			</ul>

			{showForm && (
				<form className="rv-form" onSubmit={handleSubmit}>
					<h4>{editingId === null ? "Write a review" : "Edit your review"}</h4>
					<div className="rv-form-grid">
						{RATING_CATEGORIES.map((category) => (
							<label key={category} className="rv-field">
								<span>{RATING_LABELS[category]}</span>
								<select
									value={form[category]}
									onChange={(e) => setScore(category, Number(e.target.value))}
								>
									{SCORES.map((score) => (
										<option key={score} value={score}>
											{score}
										</option>
									))}
								</select>
							</label>
						))}
					</div>
					<textarea
						aria-label="Comment"
						placeholder="Comment (optional)"
						rows={3}
						maxLength={500}
						value={form.comment}
						onChange={(e) => setForm({ ...form, comment: e.target.value })}
					/>
					<div className="rm-row">
						<button type="submit" className="btn btn-primary btn-small">
							{editingId === null ? "Submit review" : "Save review"}
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

			{!authLoading && !canWriteReview(user) && (
				<p className="rm-note">
					{user
						? "Only customers can write reviews."
						: "Log in as a customer to write a review."}
				</p>
			)}
		</div>
	);
}
