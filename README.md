### Lucid Back-end Developer Task : MVC Design Pattern Implementation ➜

### Prerequisites

- Python 3.11 or higher
- MySQL database
- Install dependencies: `pip install -r requirements.txt`

* **Models**: SQLAlchemy models in models/ directory define database tables
* **Views**: Represented by Pydantic schemas in schemas/ directory for validation and serialization
* **Controllers**: API endpoints in controllers/ directory handle HTTP requests
* **Services**: Business logic in services/ directory

### Directory Structure

```
├── app
│   ├── controllers # API endpoints
│   ├── middlewares # OAuth2 authentication
│   ├── models      # SQLAlchemy models
│   ├── schemas     # Pydantic schemas
│   ├── services    # Business logic
│   ├── utils       # Helper functions, JWT token generation, etc.
│   └── main.py     # Application entry point
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

**Run Server**

- uvicorn app.main:app --reload

### API Endpoints

#### 1. Authentication Endpoints

##### a. Signup (`/signup`)

- **Method:** `POST`
- **Description:** Creates a new user and returns a JWT token.
- **Headers:**
  - `Content-Type: application/json`
- **Request Body:**

  ```json
  {
    "email": "new.email@example.com",
    "password": "Password123"
  }
  ```

- **Example `curl` command:**

  ```bash
  curl -X POST "http://localhost:8000/signup" -H "Content-Type: application/json" -d '{"email": "new.email@example.com", "password": "Password123"}'
  ```

- **Response:** (Example)

  ```json
  {
    "access_token": "your_jwt_token"
  }
  ```

##### b. Login (`/login`)

- **Method:** `POST`
- **Description:** Authenticates a user and returns a JWT token.
- **Headers:**
  - `Content-Type: application/x-www-form-urlencoded`
- **Request Body:** (URL-encoded)

  ```
  username=new.email@example.com&password=Password123
  ```

- **Example `curl` command:**

  ```bash
  curl -X POST "http://localhost:8000/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=new.email@example.com&password=Password123"
  ```

- **Response:** (Example)

  ```json
  {
    "access_token": "your_jwt_token"
  }
  ```

#### 2. Post Management Endpoints

##### a. Create Post (`/posts`)

- **Method:** `POST`
- **Description:** Creates a new post for the authenticated user.
- **Headers:**
  - `Authorization: Bearer [YOUR_ACCESS_TOKEN]` (Replace `[YOUR_ACCESS_TOKEN]` with the actual token)
  - `Content-Type: application/json`
- **Request Body:**

  ```json
  {
    "text": "My new post"
  }
  ```

- **Example `curl` command:**

  ```bash
  curl -X POST "http://localhost:8000/posts" -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]" -H "Content-Type: application/json" -d '{"text": "My new post"}'
  ```

- **Response:** (Example)

  ```json
  {
    "id": 1,
    "text": "My new post",
    "user_id": 1
  }
  ```

##### b. Delete Post (`/posts/{post_id}`)

- **Method:** `DELETE`
- **Description:** Deletes a specific post.
- **Headers:**
  - `Authorization: Bearer [YOUR_ACCESS_TOKEN]` (Replace `[YOUR_ACCESS_TOKEN]` with the actual token)
- **Path Parameters:**
  - `post_id`: The ID of the post to delete.
- **Example `curl` command:**

  ```bash
  curl -X DELETE "http://localhost:8000/posts/1" -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]"
  ```

- **Response:** (Example - could be empty on success, or an error message on failure)

  ```
  (Empty body - success)
  ```

  or

  ```json
  {
    "detail": "Post not found"
  }
  ```

### Key Features:

1.  **Authentication Endpoints**

    - /signup: Creates a new user and returns a JWT token
    - /login: Authenticates a user and returns a JWT token

2.  **Post Management Endpoints**

    - /posts (POST): Creates a new post
    - /posts (GET): Retrieves all posts for the authenticated user
    - /posts/{post_id} (DELETE): Deletes a specific post

3.  **Security Features**

    - Password hashing with bcrypt
    - JWT token-based authentication
    - Dependency injection for protected routes

4.  **Data Validation**

    - Pydantic models with extensive validation for all input data
    - Request body size validation for the AddPost endpoint (1MB limit)

5.  **Caching**

    - In-memory caching for GetPosts endpoint with 5-minute TTL

6.  **Database Integration**

    - SQLAlchemy ORM models with appropriate relationships
    - MySQL database connection
