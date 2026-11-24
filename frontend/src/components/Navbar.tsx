import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const linkClass = ({ isActive }: { isActive: boolean }) =>
	`nav-btn ${isActive ? "active" : ""}`;

export default function Navbar() {
	const { user, loading, logout } = useAuth();
	const navigate = useNavigate();

	async function handleLogout() {
		await logout();
		navigate("/");
	}

	return (
		<header className="navbar">
			<div className="navbar-content">
				<Link to="/" className="brand">
					<span className="brand-icon">&#127869;&#65039;</span>
					<span className="brand-title">Petuk</span>
				</Link>
				<nav className="nav-links">
					<NavLink to="/" end className={linkClass}>
						Explore
					</NavLink>
					<NavLink to="/about" className={linkClass}>
						About
					</NavLink>
					{!loading && user && (
						<>
							<NavLink to="/profile" className={linkClass}>
								Profile
							</NavLink>
							<span className="nav-name">{user.name}</span>
							<span className="role-badge">{user.role}</span>
							<button type="button" className="nav-btn" onClick={handleLogout}>
								Log out
							</button>
						</>
					)}
					{!loading && !user && (
						<>
							<NavLink to="/login" className={linkClass}>
								Log in
							</NavLink>
							<NavLink to="/signup" className={linkClass}>
								Sign up
							</NavLink>
						</>
					)}
				</nav>
			</div>
		</header>
	);
}