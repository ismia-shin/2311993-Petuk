# Product Requirements Document (PRD) — Petuk

| Field | Value |
|---|---|
| Product | Petuk |
| Version | MVP + Beta |
| Releases | MVP — Mid-term, Beta — Final |
| Status | Draft |
| Related docs | [Software Requirements Specification (SRS)](02-srs.md), [Technical Design Document (TDD)](03-tdd.md) |

**Documents in this set**

| Short form | Full form | Purpose | File |
|---|---|---|---|
| PRD | Product Requirements Document | What we build and why (this document) | [01-prd.md](01-prd.md) |
| SRS | Software Requirements Specification | Exact requirements, permissions and acceptance criteria | [02-srs.md](02-srs.md) |
| TDD | Technical Design Document | How we build it: architecture, data model, API | [03-tdd.md](03-tdd.md) |

## 0. Release plan

| Release | When | Focus |
|---|---|---|
| **MVP** | Mid-term | Restaurants and reviews, stored in a database, live online |
| **Beta** | Final | Accounts, roles, menus and basic security |

## 1. Problem statement

Food lovers in Bangladesh find restaurant reviews scattered across social media, and many of them are sponsored, so it is hard to trust them. Local restaurants also lack a simple place to show accurate information. Petuk is a community-driven restaurant discovery and review platform that helps diners find authentic places to eat across Bangladesh.

## 2. Goals

| ID | Goal | Release |
|---|---|---|
| G-1 | Let people add, view, edit and delete restaurants and reviews through an API. | MVP |
| G-2 | Keep all data in a database so it is not lost. | MVP |
| G-3 | Document the API (`/api/docs`) and deploy it automatically to Vercel. | MVP |
| G-4 | Give each customer an account, so reviews belong to their author. | Beta |
| G-5 | Use two roles, `customer` and `admin`, so only the admin manages restaurants and removes unwanted reviews. | Beta |
| G-6 | Show each restaurant's menu and prices. | Beta |
| G-7 | Keep accounts safe (hashed passwords, login limit). | Beta |

## 3. Target users

| User | Need | Release |
|---|---|---|
| Customer | Browse restaurants and write reviews rated on taste, atmosphere, cleanliness, price and service. | MVP |
| Frontend developer | A clear, documented API to build the UI on. | MVP |
| Registered customer | Log in and manage my own reviews. | Beta |
| Admin | Manage restaurants, menus and bad reviews. | Beta |

In the **MVP** there are no accounts: everyone shares the same data. In the **Beta** every review belongs to a customer.

## 4. Scope

### In scope — MVP
- Add, view, list, edit and delete restaurants
- Add, view, edit and delete reviews, rated 1–5 on taste, atmosphere, cleanliness, price and service
- Clear error messages, health check, API docs, deploy to Vercel

### In scope — Beta
- Sign up, log in, log out
- Reviews belong to their author; only the author can edit or delete them
- `customer` and `admin` roles; the admin manages restaurants and menus and can remove any review
- Menu items with prices on each restaurant
- Basic security (hashed passwords, login attempt limit)

### Out of scope
- Search, photos, maps
- Reservations, ordering, delivery
- Likes or replies on reviews
- Admin dashboard, banning users
- Email verification, password reset, social login
- Automated tests and CI/CD

## 5. Features and priority (MoSCoW)

| ID | Feature | Release | Priority |
|---|---|---|---|
| F-1 | Restaurants: add, view, list, edit, delete | MVP | Must |
| F-2 | Reviews: add, view, edit, delete (five ratings and a comment) | MVP | Must |
| F-3 | Validation and error messages | MVP | Should |
| F-4 | Health check | MVP | Should |
| F-5 | Pagination on lists | MVP | Could |
| F-6 | Simple React page that uses the API | MVP | Could |
| F-7 | Sign up, log in, log out | Beta | Must |
| F-8 | Reviews owned by their author | Beta | Must |
| F-9 | Roles: admin manages restaurants and removes any review | Beta | Must |
| F-10 | Menu items with prices | Beta | Should |
| F-11 | Basic security (hashed passwords, login limit) | Beta | Should |
| F-12 | Profile page (view, change name and password) | Beta | Could |
| F-13 | Restaurant owner role to manage own menu | Beta | Could |
| F-14 | React pages for login, restaurants and reviews | Beta | Could |

## 6. User stories

### MVP

| ID | Story | Feature |
|---|---|---|
| US-01 | As a diner, I want to see a list of restaurants and open one, so I can decide where to eat. | F-1 |
| US-02 | As a user, I want to add, edit and delete a restaurant, so listings stay correct. | F-1 |
| US-03 | As a diner, I want to rate a restaurant on taste, atmosphere, cleanliness, price and service, so others know what to expect. | F-2 |
| US-04 | As a diner, I want to edit or delete my review, so I can fix mistakes. | F-2 |

### Beta

| ID | Story | Feature |
|---|---|---|
| US-05 | As a visitor, I want to sign up and log in, so I can write reviews under my name. | F-7 |
| US-06 | As a customer, I want only myself to be able to edit or delete my reviews, so nobody can change what I wrote. | F-8 |
| US-07 | As an admin, I want to manage restaurants and delete bad reviews, so the platform stays trustworthy. | F-9 |
| US-08 | As a diner, I want to see a restaurant's menu and prices, so I know what it costs. | F-10 |

## 7. Success metrics

- Restaurants and reviews can be added, viewed, edited and deleted on the live Vercel URL, and the data is still there after a redeploy.
- `/api/docs` lists every endpoint.
- A customer can never edit or delete another customer's review.
- Only an admin can add, change or delete restaurants and menus.
- Passwords are never stored or shown in plain text.

## 8. Assumptions and constraints

- This is a one-person project, so "Could" items are only built if time remains.
- Hosted on Vercel, with data in an external database (Supabase PostgreSQL).
- Backend: Python (FastAPI). Frontend: React.
- The first admin is set manually in the database.
- MVP data is demo data and does not need to be kept when the Beta adds accounts.





