export default function AboutPage() {
	return (
		<section className="about-card">
			<h2>About Petuk</h2>
			<p>
				<strong>Petuk</strong> (পেটুক) is a simple platform for keeping a
				catalog of restaurants you love, with the ability to add, view, edit
				and delete each one.
			</p>
			<p>
				It is built with a <strong>FastAPI</strong> backend and a{" "}
				<strong>React + TypeScript</strong> frontend, and stores its data in a
				database.
			</p>
			<div className="tech-pills">
				<span>React</span>
				<span>TypeScript</span>
				<span>FastAPI</span>
				<span>Supabase</span>
				<span>Vite</span>
			</div>
		</section>
	);
}