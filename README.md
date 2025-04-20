
# Movie Analysis Dashboard

An interactive movie analytics dashboard that allows users to explore trends, genres, ratings, and more — all in real-time. This project features a **Streamlit frontend**, powered by a **Django backend** and a **MySQL** database.

---

## About the Project

This dashboard provides:

- Visual breakdowns of movie ratings, genres, and release trends
- Search and filtering capabilities for deep exploration
- Modular and maintainable architecture using services and components
- Live interaction with backend APIs to fetch and display movie data

---

##  Tech Stack

| Layer            | Technology     |
|------------------|----------------|
| Frontend         | Streamlit      |
| Backend          | Django         |
| Database         | MySQL          |
| Adnl. Libraries  | Pandas, Plotly, Requests |

---

##  Frontend Directory Structure

```
dashboard/
├── components/           # Custom UI components and reusable widgets
├── services/             # API communication services
├── utils/                # Utility functions and helpers
├── dashboard_app.py      # Main  FE entry point
└── requirements.txt      # Python dependencies
```

---


## Backend & Database

The frontend connects to a Django backend which exposes REST APIs. The backend fetches and processes movie data from a MySQL database.

- Backend repo/directory:
```
├── api/
│   ├── actors/                      # Actor-related APIs and DB services
│   ├── auth/                        # User authentication and JWT logic
│   ├── directors/                   # Director-related APIs and DB services
│   ├── genres/                      # Genre-related APIs and DB services
│   ├── keywords/                    # Keyword-related APIs and DB services
│   ├── movies/                      # Movie-related APIs and DB services
│   ├── production_companies/        # Production-related APIs and DB services
│   └── user/                        # User CRUD operations and services
│
├── app.py                           # Main Flask app entry point
├── config.py                        # Configuration (DB URI, JWT secrets, etc.)
├── database.py                      # DB initialization and session handling
├── requirements.txt                 # Backend Python dependencies
├── routes.py                        # Global API route registration
```
-  Data source: MySQL (movies, genres, director, production company, etc.)

---
