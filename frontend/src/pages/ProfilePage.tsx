import { useState } from "react";
import type { SyntheticEvent } from "react";
import { useAuth } from "../hooks/useAuth";
import { changePassword, updateProfile } from "../services/authApi";
import { getErrorMessage } from "../utils/errors";

export default function ProfilePage() {
	const { user, setUser, logout, logoutAll } = useAuth();

	const [name, setName] = useState(user?.name ?? "");
	const [profileMessage, setProfileMessage] = useState("");
	const [profileError, setProfileError] = useState("");

	const [currentPassword, setCurrentPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [passwordError, setPasswordError] = useState("");

	const [sessionError, setSessionError] = useState("");

	if (!user) return null;

	async function handleProfileSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setProfileMessage("");
		setProfileError("");
		try {
			setUser(await updateProfile(name.trim()));
			setProfileMessage("Profile updated.");
		} catch (err) {
			setProfileError(getErrorMessage(err));
		}
	}

	async function handlePasswordSubmit(event: SyntheticEvent) {
		event.preventDefault();
		setPasswordError("");
		if (newPassword !== confirmPassword) {
			setPasswordError("New passwords do not match");
			return;
		}
		try {
			await changePassword(currentPassword, newPassword);
			window.alert("Password changed. Please log in again.");
			await logout();
		} catch (err) {
			setPasswordError(getErrorMessage(err));
		}
	}

	async function handleLogoutAll() {
		setSessionError("");
		try {
			await logoutAll();
		} catch (err) {
			setSessionError(getErrorMessage(err));
		}
	}

	return (
		<div>
			<section className="auth-card">
				<h1>My profile</h1>
				<p className="profile-line">
					<strong>Email:</strong> {user.email}
				</p>
				<p className="profile-line">
					<strong>Role:</strong> <span className="role-badge">{user.role}</span>
				</p>
				{profileMessage && <p className="auth-success">{profileMessage}</p>}
				{profileError && <p className="rm-error">{profileError}</p>}
				<form className="auth-form" onSubmit={handleProfileSubmit}>
					<label className="auth-field">
						<span>Name</span>
						<input
							value={name}
							maxLength={100}
							onChange={(e) => setName(e.target.value)}
							required
						/>
					</label>
					<button type="submit" className="btn btn-primary">
						Save name
					</button>
				</form>
			</section>

			<section className="auth-card">
				<h2>Change password</h2>
				{passwordError && <p className="rm-error">{passwordError}</p>}
				<form className="auth-form" onSubmit={handlePasswordSubmit}>
					<label className="auth-field">
						<span>Current password</span>
						<input
							type="password"
							value={currentPassword}
							onChange={(e) => setCurrentPassword(e.target.value)}
							required
						/>
					</label>
					<label className="auth-field">
						<span>New password (at least 8 characters)</span>
						<input
							type="password"
							value={newPassword}
							minLength={8}
							maxLength={128}
							onChange={(e) => setNewPassword(e.target.value)}
							required
						/>
					</label>
					<label className="auth-field">
						<span>Confirm new password</span>
						<input
							type="password"
							value={confirmPassword}
							minLength={8}
							maxLength={128}
							onChange={(e) => setConfirmPassword(e.target.value)}
							required
						/>
					</label>
					<button type="submit" className="btn btn-primary">
						Change password
					</button>
				</form>
			</section>

			<section className="auth-card">
				<h2>Sessions</h2>
				<p className="profile-line">
					Log out of this browser and every other device where you are logged in.
				</p>
				{sessionError && <p className="rm-error">{sessionError}</p>}
				<button type="button" className="btn btn-danger" onClick={handleLogoutAll}>
					Log out of all devices
				</button>
			</section>
		</div>
	);
}