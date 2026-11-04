import { useState } from "react";
import RestaurantManager from "./components/RestaurantManager";
import "./App.css";

export default function App() {
	const [activeTab, setActiveTab] = useState<"home" | "about">("home");

	return (
		<div className="app-container">
			<header className="navbar">
				<div className="navbar-content">
					<div className="brand" onClick={() => setActiveTab("home")}>
						<span className="brand-icon">🍽️</span>
						<span className="brand-title">Petuk</span>
					</div>
					<nav className="nav-links">
						<button
							type="button"
							className={`nav-btn ${activeTab === "home" ? "active" : ""}`}
							onClick={() => setActiveTab("home")}
						>
							Explore
						</button>
						<button
							type="button"
							className={`nav-btn ${activeTab === "about" ? "active" : ""}`}
							onClick={() => setActiveTab("about")}
						>
							About
						</button>
					</nav>
				</div>
			</header>

			<main className="main-content">
				{activeTab === "home" ? (
					<RestaurantManager />
				) : (
					<section className="about-card">
						<h2>About Petuk</h2>
						<p>
							<strong>Petuk</strong> (পেটুক) is a simple platform for keeping a
							catalog of restaurants you love, with the ability to add, view,
							edit and delete each one.
						</p>
						<p>
							It is built with a <strong>FastAPI</strong> backend and a{" "}
							<strong>React + TypeScript</strong> frontend, and stores its data
							in a database.
						</p>
						<div className="tech-pills">
							<span>React</span>
							<span>TypeScript</span>
							<span>FastAPI</span>
							<span>Supabase</span>
							<span>Vite</span>
						</div>
					</section>
				)}
			</main>

			<footer className="footer">
				<p>&copy; {new Date().getFullYear()} Petuk MVP</p>
			</footer>
		</div>
	);
}
