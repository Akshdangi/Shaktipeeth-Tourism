# 🛕 Shaktipeeth Tourism Web App

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-ff6b6b?style=for-the-badge&logo=render&logoColor=white)](https://shaktipeeth-tourism-1.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A comprehensive, full-stack **Flask-based web application** designed for exploring, planning, and booking sacred pilgrimages to **Shaktipeeth temples** across India. Featuring an interactive sacred map, multi-language support across 8 languages, an AI-powered spiritual assistant (**ShaktiGPT**), secure user authentication, and automated email confirmations.

---

## 🌐 Live Deployment

Experience the live application deployed on **Render**:  
🔗 **[https://shaktipeeth-tourism-1.onrender.com](https://shaktipeeth-tourism-1.onrender.com)**

---

## 🚀 Key Features

* **🤖 ShaktiGPT AI Spiritual Guide:** Built-in AI assistant powered by Ollama (`shaktigpt`) to answer queries about temple histories, significance, rituals, and travel tips. Supports saving and loading conversation history (`/api/chat`, `/api/save-chat`).
* **🌍 Multi-Language Support (i18n):** Dynamic real-time translation across **8 major languages**: English, Hindi (`हिन्दी`), Bengali (`বাংলা`), Tamil (`தமிழ்`), Telugu (`తెలుగు`), Marathi (`मराठी`), Gujarati (`ગુજરાતી`), and Punjabi (`ਪੰਜਾਬੀ`).
* **🧭 Interactive Sacred Map:** Powered by **Leaflet.js** with custom Google Maps tile layers (Streets, Satellite, and Terrain) to visualize exact temple coordinates across the Indian subcontinent.
* **🔐 Secure Authentication & Sessions:** Complete user registration and login system (`/login`, `/register`) using **Werkzeug password hashing** and secure `HTTPS` + `SameSite` session cookies.
* **🧾 Seamless Tour Booking System:** Guided tour booking workflow (`/book`) with instant backend validation, dynamic pricing tiers (Budget, Standard, Premium), and package options (Eastern, Northern, Complete).
* **📧 Automated Email Notifications:** Integrated with **Flask-Mail** to send personalized welcome emails upon registration and detailed itinerary confirmation emails (`#Booking ID`) upon tour reservation.
* **🙏 Sacred Donations Portal:** Dedicated portal (`/donation`) allowing devotees to support the preservation and ongoing upkeep of divine Shakti Peethas.
* **📱 Responsive & Premium UI:** Crafted with custom CSS gradients, glassmorphism, smooth animations, and curated typography (Cinzel & Inter from Google Fonts).

---

## 🛠️ Tech Stack

### **Backend & Core**
* **Framework:** Python 3.12+ (Flask)
* **Database & ORM:** SQLite (local development) / PostgreSQL (production via Render), `Flask-SQLAlchemy`
* **Authentication:** Werkzeug Security (`generate_password_hash`, `check_password_hash`), Flask Sessions
* **Communication & APIs:** `Flask-Mail` (SMTP email automation), `Flask-CORS`
* **AI / LLM Engine:** Ollama (`shaktigpt` local model) / Configurable REST LLM Endpoint (`OLLAMA_API_URL`)

### **Frontend & UI**
* **Markup & Styling:** HTML5, Vanilla CSS3 (Custom design system, CSS Variables, Glassmorphism)
* **Scripting:** ES6+ JavaScript, `fetch` API with `credentials: include`
* **Mapping:** Leaflet.js, Google Maps Tile API layers
* **Internationalization:** Custom JS-driven multi-language dictionary engine (`static/js/i18n.js`)

---

## 📁 Project Structure

```
shaktipeeth-tourism/
│
├── app.py                     # Main Flask application & route definitions
├── config.py                  # Environment & secure session/mail configurations
├── models.py                  # SQLAlchemy models (User, Booking, ChatMessage)
├── utils.py                   # Server-side validation logic for bookings & registrations
├── requirements.txt           # Python dependencies (psycopg2-binary, gunicorn, etc.)
├── shaktipeeth_data.csv       # Dataset of 51+ sacred Shaktipeeth temples & regional info
│
├── templates/                 # Jinja2 / HTML templates
│   ├── shaktipeeth-homepage.html      # Main landing page with temple slider & quick links
│   ├── about-page.html                # About Shaktipeeth Tourism & history
│   ├── login.html                     # User account login portal
│   ├── logout.html                    # Logout confirmation & session clearing
│   ├── shaktipeeth-registration.html  # New devotee registration form
│   ├── book-tour-complete.html        # Tour reservation & itinerary form
│   ├── donation-page.html             # Temple preservation donation platform
│   └── sacred-map.html                # Interactive Leaflet map of all temples
│
└── static/                    # Static assets & scripts
    ├── js/
    │   └── i18n.js                    # Multi-language translation engine (8 languages)
    └── meenakshi temple.jpeg          # High-resolution UI banners & imagery
```

---

## 📡 API Endpoints Reference

### **Authentication & User APIs**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/register` | Register a new user (`fullname`, `age`, `email`, `password`, `mobile`, `idtype`, `idnumber`) |
| `POST` | `/api/login` | Authenticate credentials and establish secure HTTP-only session |
| `POST` | `/api/logout` | Terminate active user session and clear cookies |
| `GET` | `/api/user-status` | Retrieve active session details (`logged_in: boolean`, `user: {id, email, name}`) |

### **Tour Booking APIs**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/book` | Submit a new tour booking (`package`, `travel_date`, `num_travelers`, `accommodation`, `contact_person`) |
| `GET` | `/api/bookings` | Fetch list of all historical bookings (Admin/API use) |
| `GET` | `/api/bookings/<id>` | Fetch specific booking record by ID |

### **ShaktiGPT AI Chatbot APIs**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/chat` | Send message to Ollama `shaktigpt` model and stream/return spiritual guidance |
| `POST` | `/api/save-chat` | Persist a user prompt and assistant response into `ChatMessage` table |
| `GET` | `/api/chat-history` | Retrieve up to 50 previous chat messages for the authenticated user |

---

## ⚙️ Local Installation & Setup

### **1. Clone the repository**
```bash
git clone https://github.com/Akshdangi/Shaktipeeth-Tourism.git
cd Shaktipeeth-Tourism
```

### **2. Create & activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
```

### **3. Install required dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure environment variables (Optional `.env`)**
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_custom_secret_key
DATABASE_URL=sqlite:///shaktipeeth.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
OLLAMA_API_URL=http://localhost:11434/api/chat
```

### **5. Run the application locally**
```bash
python app.py
```
Open your browser and navigate to **`http://localhost:8001`** (or port specified in `PORT` env var).

---

## 🌍 Production Deployment (Render)

The application is configured for seamless deployment on **Render** (`gunicorn` + `PostgreSQL`):

1. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start Command:**
   ```bash
   gunicorn app:app
   ```
3. **Environment Variables on Render Dashboard:**
   * `RENDER = true` (enables `SESSION_COOKIE_SECURE` for HTTPS persistence)
   * `DATABASE_URL` (PostgreSQL connection string — automatically adapted by `config.py`)
   * `SECRET_KEY` (production secret key for session verification)
   * `MAIL_USERNAME` & `MAIL_PASSWORD` (SMTP credentials for automated email delivery)
   * `OLLAMA_API_URL` (URL pointing to hosted Ollama instance or LLM gateway)

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!  
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author & License

* **Author:** [Aksh Dangi](https://github.com/Akshdangi)
* **License:** Distributed under the **MIT License**. See `LICENSE` for more information.

---
⭐ *If you find this project helpful or insightful for spiritual tourism & full-stack development, please consider giving it a star on GitHub!* ⭐
