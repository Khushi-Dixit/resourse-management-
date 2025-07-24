# resourse-management-
# 🔧 Resource Management API

A lightweight Python Flask API to log, manage, and retrieve user-specific resource access data with automatic TTL-based expiration.

---

## 📌 Features

- ✅ Log a resource access by a specific user ID
- ⏳ Automatically expire logs after a given time-to-live (TTL)
- 🔍 Retrieve all non-expired logs for a user
- 🕒 Retrieve all resources logged at a specific timestamp
- 🧹 Manually trigger cleanup of expired logs
- 📦 Easily extendable for database or scheduler support

---

## 🚀 Tech Stack

- **Language:** Python 3.x  
- **Framework:** Flask  
- **Data Store:** In-memory (list)  
- **Tools:** `time` module for TTL, `curl`/Postman for API testing

---

## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resource-management-api.git
   cd resource-management-api
2.Install dependencies:
pip install flask

3.Run the application:
python resource_logger.py


🌱 Future Enhancements
🗃️ Integrate SQLite / MongoDB as persistent backend

🔐 Add JWT authentication and API key management

📅 Schedule auto-cleanup using APScheduler

📊 Add admin dashboard to visualize logs

📦 Dockerize the project for deployment


