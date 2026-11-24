import { useState } from "react";
import type { SyntheticEvent } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getErrorMessage } from "../utils/errors";

export default function LoginPage() {
	const { user, loading, login } = useAuth();
	const location = useLocation();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [submitting, setSubmitting] = useState(false);

	const from = (location.state as { from?: string } | null)?.from ?? "/";

	if (loading) {
		return <p className="rm-note">Loading...</p>;
	}
	if (user) {
		return <Navigate to={from} replace />;
	}

	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setError("");
		setSubmitting(true);
		try {
			await login(email.trim(), password);
		} catch (err) {
			setError(getErrorMessage(err, "Login failed"));
		} finally {
			setSubmitting(false);
		}
	}

	return (
		<section className="auth-card">
			<h1>Log in</h1>
			{error && <p className="rm-error">{error}</p>}
			<form className="auth-form" onSubmit={handleSubmit}>
				<label className="auth-field">
					<span>Email</span>
					<input
						type="email"
						placeholder="you@example.com"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
					/>
				</label>
				<label className="auth-field">
					<span>Password</span>
					<input
						type="password"
						placeholder="Your password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
				</label>
				<button type="submit" className="btn btn-primary" disabled={submitting}>
					{submitting ? "Logging in..." : "Log in"}
				</button>
			</form>
			<p className="auth-switch">
				New here? <Link to="/signup">Create an account</Link>
			</p>
		</section>
	);
}
