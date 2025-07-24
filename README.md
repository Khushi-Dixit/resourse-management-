# 🚀 Resource Management API

A Flask-based backend application for managing and logging resources by users with features like automatic expiration (TTL), retrieval by user ID or timestamp, and persistent storage using SQLite.

---

## 🔧 Features

- ✅ Log resources with a TTL (Time-to-Live) mechanism
- ✅ Retrieve resources by user ID or timestamp
- ✅ Automatically clean up expired logs
- ✅ Persistent storage using SQLite
- ✅ `.env` support for configurations
- ✅ Docker support (Optional)
- ✅ Basic unit testing

---

## 📦 Installation

### 🔹 Clone the repository

```bash
git clone https://github.com/Khushi-Dixit/resourse-management-.git
cd resourse-management-
```

### 🔹 Create a virtual environment and activate

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 🔹 Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration (.env)

Create a `.env` file in the root directory and include the following:

```env
TTL_SECONDS=600
DATABASE_URI=sqlite:///resources.db
FLASK_ENV=development
```

---

## ▶️ Running the App

```bash
python run.py
```

The app will start at `http://127.0.0.1:5000/`

---

## 🌐 API Endpoints

| Method | Endpoint                  | Description                                |
|--------|---------------------------|--------------------------------------------|
| POST   | `/log_resource`           | Log a new resource with TTL                |
| GET    | `/get_resources/<user_id>`| Get all resources for a specific user ID   |
| GET    | `/get_all_resources`      | Get all currently active resources         |
| GET    | `/get_by_time/<timestamp>`| Get all resources logged at a timestamp    |

---

## 📁 Folder Structure

```
resourse-management-/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   └── test_routes.py
├── .env
├── requirements.txt
├── Dockerfile
├── README.md
└── run.py
```

---

## 🧪 To Run Tests (if added)

```bash
pytest tests/
```

---

## 🐳 Docker (Optional)

To build and run using Docker:

```bash
docker build -t resource-api .
docker run -p 5000:5000 resource-api
```

---

## ✨ Author

Created by **Khushi Dixit** – [GitHub](https://github.com/Khushi-Dixit)
