# API MovieLens — Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED)

Practical **Machine Learning + API** project split into two stages:

- **Part 1:** train a recommendation system using MovieLens data;
- **Part 2:** expose the trained model through an API (FastAPI), with request validation and Docker execution.

---

## Table of Contents

* [Project Context](#1-project-context)
* [Goals](#2-goals)

  - [Part 1 — MovieLens Recommendation](#part-1--movielens-recommendation)
  - [Part 2 — Inference API](#part-2--inference-api)
    
* [Part 1 Notebook (Detailed Flow)](#3-part-1-notebook-detailed-flow)

* [Repository Structure](#4-repository-structure)

* [Tech Stack](#5-tech-stack)

* [How to Run](#6-how-to-run)

  - [Running Locally](#61-running-locally)
  - [Running with Docker](#62-running-with-docker)
    
* [API Endpoints](#7-api-endpoints)

* [Implemented Validations](#8-implemented-validations)

* [Usage Example](#9-usage-example)

* [References](#10-references)

---

## Project Context

Recommendation systems are among the most valuable data applications across industries, helping companies suggest items with higher potential for conversion, retention, and revenue.

In this project, we use **MovieLens**, one of the most traditional datasets for recommendation problems, widely adopted in academic research and applied projects.

This project was developed inspired by the **7DaysOfCode Data Science challenge by Alura**, with a focus on practical experimentation based on real-world cases.
---

## Goals

### Goals Part 1 — MovieLens Recommendation

Build a recommendation system capable of suggesting **5 movies per user** based on historical behavior (past interactions).

Beyond training, this stage also includes **model serialization** for later production reuse, using libraries such as:

- `joblib` (example: `joblib.dump(model, "file.sav")`)
- `pickle`

> The serialized artifact is essential for the API deployment stage.

### Goals Part 2 — Inference API

Create a simple API that consumes the trained model and responds to recommendation requests in near real-time.

Main requirements:

- provide at least **1 recommendation endpoint**;
- validate requests before prediction;
- check request format and HTTP method;
- validate required fields and input consistency;
- package the app with **Docker**.

---

## Part 1 Notebook (Detailed Flow)

The `movie-lens.ipynb` notebook contains the full recommender-building process in steps:

1. **Data loading and initial EDA**
   - load `ratings` and `movies`;
   - run quality checks (nulls, schema, and cardinality).

2. **Popularity baseline**
   - build an initial movie ranking using average rating and number of ratings;
   - create a simple function to return popular recommendations.

3. **Movie-based recommendation (item-item)**
   - apply **KNN** to find movies similar to a reference movie;
   - create mapping dictionaries (`movieId` ↔ title) for easier retrieval and responses.

4. **User-based recommendation (main goal)**
   - implement logic to recommend movies the user has not watched yet;
   - use KNN similarities to generate scores and final ranking.

5. **Model/artifact serialization**
   - persist all artifacts required for later inference in the API.

> In short: before the final user-based recommender, the notebook also demonstrates movie-to-movie similarity recommendations, which support the next stage.

---

## Repository Structure

```bash
.
├── api.py                # FastAPI application for recommendations
├── movie-lens.ipynb      # Notebook for training/preparation (Part 1)
├── requirements.txt      # Project dependencies
├── Dockerfile            # API containerization
└── README.md
```

> **Important:** for the API to run, the serialized model file (`recomendador_movies_knn.sav`) must be available in the project root.

---

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Pydantic**
- **Scikit-learn**
- **Pandas / NumPy**
- **Joblib**
- **Uvicorn**
- **Docker**

---

## How to Run

### Running Locally

1. Clone the repository:

```bash
git clone <repository-url>
cd API-MovieLens
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure `recomendador_movies_knn.sav` is in the project root.

5. Run the API:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

6. Access:

- API: `http://localhost:8000`
- Interactive docs (Swagger): `http://localhost:8000/docs`

### Running with Docker

1. Build the image:

```bash
docker build -t api-movielens .
```

2. Run the container:

```bash
docker run --rm -p 8000:8000 api-movielens
```

3. Open docs:

- `http://localhost:8000/docs`

---

## API Endpoints

### `POST /predict`

Receives a user id and returns movie recommendations.

**Expected body (JSON):**

```json
{
  "user_id": 1,
  "top_k": 5
}
```

- `user_id` (required): integer >= 1
- `top_k` (optional): integer between 1 and 20 (default = 5)

**Response example:**

```json
{
  "input_user_id": 1,
  "movies_watched_count": 34,
  "recommendations": [
    {
      "movie_id": 50,
      "title": "Star Wars (1977)",
      "relevance_score": 9.8731
    }
  ]
}
```

---

## Implemented Validations

The API already applies important baseline validations:

- type and range validation via **Pydantic**;
- unknown users rejected with `404`;
- internal errors returned as `500`;
- explicit `POST` method usage for prediction.

---

## Usage Example

Using `curl`:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 10, "top_k": 5}'
```

---

## References

- MovieLens dataset: [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/32m/)
- FastAPI: https://fastapi.tiangolo.com/
- Joblib: https://joblib.readthedocs.io/
- Alura #7DaysOfCode: https://7daysofcode.io/#dados

---

## Author 
Barbara Barletta
Data Science Portfolio Project.
