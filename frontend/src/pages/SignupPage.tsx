import { useState } from "react";
import type { SyntheticEvent } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { signup } from "../services/authApi";
import type { SignupInput } from "../types/user";
import { getErrorMessage } from "../utils/errors";

export default function SignupPage() {
	const { user, loading, login } = useAuth();
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [role, setRole] = useState<SignupInput["role"]>("customer");
	const [error, setError] = useState("");
	const [submitting, setSubmitting] = useState(false);

	if (loading) {
		return <p className="rm-note">Loading...</p>;
	}
	if (user) {
		return <Navigate to="/" replace />;
	}

	async function handleSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setError("");
		setSubmitting(true);
		try {
			const cleanEmail = email.trim();
			await signup({ name: name.trim(), email: cleanEmail, password, role });
			await login(cleanEmail, password);
		} catch (err) {
			setError(getErrorMessage(err, "Signup failed"));
		} finally {
			setSubmitting(false);
		}
	}

	return (
		<section className="auth-card">
			<h1>Create your account</h1>
			{error && <p className="rm-error">{error}</p>}
			<form className="auth-form" onSubmit={handleSubmit}>
				<label className="auth-field">
					<span>Name</span>
					<input
						placeholder="Your name"
						value={name}
						maxLength={100}
						onChange={(e) => setName(e.target.value)}
						required
					/>
				</label>
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
					<span>Password (at least 8 characters)</span>
					<input
						type="password"
						placeholder="Choose a password"
						value={password}
						minLength={8}
						maxLength={128}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
				</label>
				<label className="auth-field">
					<span>I am a</span>
					<select
						value={role}
						onChange={(e) => setRole(e.target.value as SignupInput["role"])}
					>
						<option value="customer">Customer (I want to review restaurants)</option>
						<option value="owner">Restaurant owner (I want to manage my restaurant)</option>
					</select>
				</label>
				<button type="submit" className="btn btn-primary" disabled={submitting}>
					{submitting ? "Creating account..." : "Sign up"}
				</button>
			</form>
			<p className="auth-switch">
				Already have an account? <Link to="/login">Log in</Link>
			</p>
		</section>
	);
}