import { Route, Routes } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import RestaurantManager from "./components/RestaurantManager";
import AboutPage from "./pages/AboutPage";
import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import SignupPage from "./pages/SignupPage";

export default function App() {
	return (
		<div className="app-container">
			<Navbar />

			<main className="main-content">
				<Routes>
					<Route path="/" element={<RestaurantManager />} />
					<Route path="/about" element={<AboutPage />} />
					<Route path="/login" element={<LoginPage />} />
					<Route path="/signup" element={<SignupPage />} />
					<Route
						path="/profile"
						element={
							<ProtectedRoute>
								<ProfilePage />
							</ProtectedRoute>
						}
					/>
					<Route
						path="*"
						element={<p className="rm-note">Page not found.</p>}
					/>
				</Routes>
			</main>

			<footer className="footer">
				<p>&copy; {new Date().getFullYear()} Petuk</p>
			</footer>
		</div>
	);
}