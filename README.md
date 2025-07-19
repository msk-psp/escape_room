# Escape Everything

Escape Everything is a web service that provides integrated information on escape room cafes and themes across South Korea, helping users easily and quickly find themes that suit their tastes.

## Project Overview

This project aims to build a web service that helps users find escape room cafes and themes. It provides search and filtering functions to help users find the themes they want.

## Tech Stack

- **Frontend:** React (with Bun), TypeScript, Tailwind CSS
- **Backend:** Python (FastAPI), SQLAlchemy
- **Database:** PostgreSQL (with PostGIS)
- **Crawling:** Python (Selenium, BeautifulSoup)
- **Deployment:** Docker

## Features

### Frontend

- **Main Page:** Displays popular themes, new themes, and recommended cafes by region.
- **Search and Filtering:**
    - Search by cafe or theme name.
    - Filter by region, genre, difficulty, number of players, and rating.
    - View results in a list or on a map.
- **Cafe/Theme Details:**
    - View detailed information about cafes and themes.
    - Read and write reviews.
- **Map View:**
    - View search results on a map.
    - Click on a pin to view summary information.

### Backend

- **RESTful API:** Provides APIs for searching, viewing, and reviewing cafes and themes.
- **Data Crawling:**
    - Periodically crawls data from Naver Map, Kakao Map, and official cafe websites.
    - Collects cafe and theme information.
- **Data Management:**
    - Cleans and removes duplicate data.
    - Provides an admin page for managing cafe and theme information.

## Database Schema

- **`cafes`:** Stores cafe information.
- **`themes`:** Stores theme information.
- **`reviews`:** Stores user reviews.
- **`users`:** Stores user information.

## Getting Started

### Prerequisites

- Bun
- Python 3.11+
- Docker

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/escape-everything.git
   ```
2. **Frontend:**
   ```bash
   cd app
   bun install
   bun run dev
   ```
3. **Backend:**
   ```bash
   cd backend
   uv pip install -r requirements.txt
   uvicorn main:app --reload
   ```

### Docker

You can also run the project using Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

- `GET /api/cafes`: Get a list of cafes.
- `GET /api/cafes/{id}`: Get detailed information about a specific cafe.
- `GET /api/themes`: Get a list of themes.
- `GET /api/themes/{id}`: Get detailed information about a specific theme.
- `POST /api/themes/{id}/reviews`: Add a review for a specific theme.
- `GET /api/themes/{id}/reviews`: Get a list of reviews for a specific theme.
