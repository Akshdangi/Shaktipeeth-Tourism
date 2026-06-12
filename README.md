# 🛕 Shaktipeeth Tourism Web App

A full-stack Flask-based web application for exploring and booking tours to sacred Shaktipeeth temples across India. The platform allows users to browse destinations, register/login, and book pilgrimage tours seamlessly.

---

## 🚀 Features

* 🌐 Interactive homepage with temple slider
* 🧭 Sacred map navigation
* 📝 User registration & login system
* 🧾 Tour booking system with API integration
* 📧 Email confirmation (optional)
* 🗄️ Database integration using SQLAlchemy
* 📱 Responsive UI design

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (local) / PostgreSQL (production)
* **ORM:** Flask-SQLAlchemy
* **Deployment:** Render
* **Other:** Flask-Mail, Flask-CORS

---

## 📁 Project Structure

```
shaktipeeth-tourism/
│
├── app.py
├── config.py
├── models.py
├── utils.py
├── requirements.txt
│
├── templates/
│   ├── shaktipeeth-homepage.html
│   ├── book-tour.html
│   ├── login.html
│   ├── donation-page.html
│   ├── sacred-map.html
│   └── ...
│
├── static/
│   ├── images/
│   ├── css/
│   └── js/
│
└── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```
git clone https://github.com/Akshdangi/Shaktipeeth-Tourism.git
cd Shaktipeeth-Tourism
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the app

```
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## 🌍 Deployment (Render)

* Build Command:

```
pip install -r requirements.txt
```

* Start Command:

```
gunicorn app:app
```

* Add environment variables in Render dashboard:

  * `DATABASE_URL` (for PostgreSQL)
  * `MAIL_USERNAME`, `MAIL_PASSWORD` (optional)

---

## 📡 API Endpoints

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| POST   | /api/book          | Book a tour       |
| GET    | /api/bookings      | Get all bookings  |
| GET    | /api/bookings/<id> | Get booking by ID |

---

## 🧠 Future Enhancements

* 💳 Payment Gateway Integration
* 📊 Admin Dashboard
* 🤖 AI-based temple recommendation system
* 📍 Real-time map integration
* 🔐 JWT Authentication

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Aksh Dangi**
🔗 GitHub: https://github.com/Akshdangi

---

⭐ If you like this project, give it a star!
