# FilmFusion

FilmFusion is a comprehensive web application that offers a wide range of features related to movies, including reviews, ratings, recommendations, and user interactions.

## Installation and Setup

### OS-Based Dependencies

1. **Provide executable permission to the script:**
    ```bash
    chmod +x dependencies.sh
    ```

2. **Run the dependencies script:**
    ```bash
    ./dependencies.sh
    ```

### Project Setup

1. **Clone the repository:**
    ```bash
    git clone <repo link>
    ```

2. **Navigate to the project directory:**
    ```bash
    cd FilmFusion/filmfusion
    ```

3. **Copy content from `example.env` to `.env`:**
    ```bash
    cp example.env .env
    ```
   Update the `.env` file with the correct values.

4. **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Open and run the Jupyter notebook:**
   - To open `movie_recommendation.ipynb` in VS Code, select the correct kernel.
   - Alternatively, you can access the notebook through the Jupyter Notebook UI:
    ```bash
    jupyter-notebook
    ```
   Run the notebook to preprocess the data and build recommendation models, which will be used in the APIs.

6. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Run Celery beat and worker:**
    ```bash
    celery -A filmfusion beat -l info
    celery -A filmfusion worker -l info
    ```

8. **Start the Django server:**
    ```bash
    python manage.py runserver
    ```

### Project Setup Completion
Your project setup is now complete.

## API Documentation

### Onboarding

- **Register**
  - **URL:** `http://127.0.0.1:8000/api/users/register/`
  - **Description:** Create a new user with unique email constraints and an encrypted password. The user remains `is_active=False` until email verification. An OTP is sent to the provided email for verification.

- **Verify OTP**
  - **URL:** `http://127.0.0.1:8000/api/users/verify-otp/`
  - **Description:** Verifies the email through OTP, activates the user (`is_active=True`), and returns access and refresh tokens.

- **Resend OTP**
  - **URL:** `http://127.0.0.1:8000/api/users/resend_otp/`
  - **Description:** The OTP has a 2-minute lifespan. This API can be used to resend the OTP if it expires.

- **Login**
  - **URL:** `http://127.0.0.1:8000/api/users/login/`
  - **Description:** Login for existing users, returns access and refresh tokens.

- **Logout**
  - **URL:** `http://127.0.0.1:8000/api/users/logout/`
  - **Description:** Logs out the user and blacklists the refresh token.

- **Access Token**
  - **URL:** `http://127.0.0.1:8000/auth/token/refresh/`
  - **Description:** Recreates and returns a new access token.

### Users

- **Create (Admin Only)**
  - **URL:** `http://127.0.0.1:8000/api/users/`
  - **Description:** Create a user with an encrypted password without email verification.

- **List Users (Admin Only)**
  - **URL:** `http://127.0.0.1:8000/api/users/`
  - **Description:** Returns a paginated list of users.

- **Get/Update/Delete User**
  - **URL:** `http://127.0.0.1:8000/api/users/retrieve_update_destroy/`
  - **Description:** Users can get, update, or delete their profiles.

### Movies

- **Movies Recommendations**
  - **URL:** `http://127.0.0.1:8000/api/movies/recommendations/`
  - **Description:** A hybrid recommendation model works in the backend. It recommends 10 movies by default if `num_recommendations` isn't provided in query params. If `user_id` and `movie_id` aren't provided, a popularity-based model is used. If only `movie_id` is provided, a content-based model is used. If both are provided, a collaborative filtering model is applied.

- **Fetch Movies**
  - **URL:** `http://127.0.0.1:8000/api/movies/fetch/`
  - **Description:** Fetch movie details from the database (if they exist) or from TMDB. The movie details are stored in the database for each `tmdb_id` in the provided list.

- **Get Movie**
  - **URL:** `http://127.0.0.1:8000/api/movies/<uuid:pk>/`
  - **Description:** Returns movie details along with all reviews and comments in a paginated format for the specified movie UUID.

- **Movie by Genre**
  - **URL:** `http://127.0.0.1:8000/api/movies/genres/<uuid:pk>/`
  - **Description:** Returns a paginated list of movies for the specified genre UUID.

- **Movies List**
  - **URL:** `http://127.0.0.1:8000/api/movies/`
  - **Description:** Returns a paginated list of all movies in the database.

### Reviews

- **Reviews List/Create**
  - **URL:** `http://127.0.0.1:8000/api/movie/reviews/?movie_id=<uuid>`
  - **Description:** Returns a paginated list of reviews along with comments for the specified movie UUID, or creates a review for a movie.

- **Reviews Get/Update/Delete**
  - **URL:** `http://127.0.0.1:8000/api/movie/reviews/<uuid:pk>/`
  - **Description:** Users can get, update, or delete their review for the provided review UUID.

- **Comments List/Create**
  - **URL:** `http://127.0.0.1:8000/api/movie/comments/?review_id=<uuid>`
  - **Description:** Returns a paginated list of comments for the specified review UUID, or creates comments for a review.

- **Comments Get/Update/Delete**
  - **URL:** `http://127.0.0.1:8000/api/movie/comments/<uuid>`
  - **Description:** Users can get, update, or delete their comments for the specified comment UUID.

### Search API

There is a search API for movies and reviews that uses Elasticsearch. However, the search API code is currently commented out because Elasticsearch could not be tested due to system limitations.

## Key Features

- **JWT Authentication**
- **Swagger Documentation**
- **Admin Integration**
- **Shared Tasks:**
  - `send_otp_email`
  - `fetch_and_store_movies`: A cron job to fetch movies from TMDB periodically and save them in the database if they don't already exist.
- **Logs**
- **Recommendation System:**
  - Popularity-based recommendations
  - Content-based recommendations
  - Collaborative filtering-based recommendations
  - Hybrid recommendations that combine the above three models
- **Elasticsearch** for text-based search

## Pending Work

- Fine-tuning the recommendation model for upcoming data (currently in progress).

## Notes

There may be unhandled scenarios in this project. Please report any issues, and I'll make the necessary fixes and updates.
