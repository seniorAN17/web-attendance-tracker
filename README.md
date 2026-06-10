# Web Attendance Tracker

🎓 A modern, AI-powered web application for tracking class attendance with real-time analytics and predictive insights.

## 📋 Project Overview

This is an educational practice project built with:
- **Backend:** Python (FastAPI)
- **Microservice:** Go (high-performance data processing)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** PostgreSQL
- **AI/ML:** Attendance prediction & anomaly detection
- **Deployment:** Docker & Docker Compose

**Deadline:** June 18, 2026, 23:59

## ✨ Features

### Core Functionality
- ✅ **Add** attendance records (mark students present/absent)
- ✅ **View** attendance with filtering options
- ✅ **Edit** existing attendance entries
- ✅ **Delete** incorrect records
- ✅ **Search & Filter** by student, class, date, status
- ✅ **Real-time Statistics** (attendance rates, trends)

### AI/ML Features
- 🤖 **Attendance Prediction** - Predict future attendance patterns
- 📊 **Anomaly Detection** - Identify unusual attendance behavior
- 📈 **Analytics Dashboard** - Visual insights into attendance trends
- ⚠️ **Risk Alerts** - Flag students at risk of low attendance

### Technical Features
- 🚀 **High Performance** - Go microservice for heavy computations
- 🔄 **Real-time Sync** - Instant data updates
- 📱 **Responsive Design** - Works on desktop and mobile
- 🐳 **Docker Ready** - Local development + cloud deployment
- 📚 **API Documentation** - Interactive Swagger UI

## 📁 Project Structure

```
web-attendance-tracker/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── routes.py          # API endpoints
│   │   ├── database.py        # Database config
│   │   └── config.py          # App configuration
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile
│   └── .env.example
│
├── go-service/                 # Go microservice
│   ├── main.go                # Entry point
│   ├── handlers/              # Request handlers
│   ├── models/                # Data models
│   ├── go.mod                 # Go dependencies
│   ├── Dockerfile
│   └── README.md
│
├── ai-module/                  # AI/ML predictions
│   ├── predictor.py           # Prediction models
│   ├── anomaly_detector.py    # Anomaly detection
│   ├── requirements.txt        # ML dependencies
│   └── models/                # Trained models (optional)
│
├── frontend/                   # HTML/CSS/JS frontend
│   ├── index.html             # Main page
│   ├── style.css              # Styling
│   ├── script.js              # Frontend logic
│   ├── pages/                 # Additional pages
│   └── assets/                # Images, fonts
│
├── docker-compose.yml         # Multi-container orchestration
├── .env.example               # Environment variables template
├── README.md                  # This file
├── .gitignore                 # Git ignore file
└── TEAM.md                    # Team contributions
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- OR:
  - Python 3.9+
  - Go 1.18+
  - PostgreSQL 12+
  - Node.js (optional, for frontend tooling)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/seniorAN17/web-attendance-tracker.git
cd web-attendance-tracker

# Create .env file
cp .env.example .env

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Go Service: http://localhost:8080
```

### Option 2: Local Development

#### Backend (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

#### Frontend
```bash
cd frontend
# Open index.html in browser or use a simple server:
python -m http.server 3000
```

#### Go Service (Optional)
```bash
cd go-service
go build -o attendance-service
./attendance-service
```

## 🔌 API Endpoints

### Attendance Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/attendance` | Get all records |
| GET | `/api/attendance?student_name=name&date=2025-01-01` | Filter records |
| POST | `/api/attendance` | Create new record |
| GET | `/api/attendance/{id}` | Get specific record |
| PUT | `/api/attendance/{id}` | Update record |
| DELETE | `/api/attendance/{id}` | Delete record |
| GET | `/api/attendance/stats` | Get statistics |

### AI/ML Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Predict attendance |
| GET | `/api/anomalies` | Detect anomalies |
| GET | `/api/analytics` | Get analytics |
| POST | `/api/alerts` | Generate alerts |

### Go Service Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/process` | Process heavy computations |
| GET | `/health` | Health check |

## 📊 Database Schema

### attendance table
```sql
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    class_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('present', 'absent')),
    time_in TIME,
    time_out TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 👥 Team Contributions

See [TEAM.md](TEAM.md) for detailed team member contributions and task assignments.

| Role | Member | Tasks |
|------|--------|-------|
| Backend Developer | Member 1 | Python API, Database, Routes |
| Frontend Developer | Member 2 | HTML/CSS/JS UI, Forms, Tables |
| DevOps/Database | Member 3 | PostgreSQL, Docker, Deployment |
| AI/ML Developer | Member 4 | Predictions, Anomaly Detection, Analytics |

## 🔧 Configuration

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/attendance

# FastAPI
FASTAPI_ENV=development
FASTAPI_DEBUG=True

# Go Service
GO_SERVICE_PORT=8080

# AI/ML
ML_MODEL_PATH=./ai-module/models/
```

## 📦 Dependencies

### Python
- FastAPI (Web framework)
- SQLAlchemy (ORM)
- psycopg2 (PostgreSQL driver)
- Pydantic (Data validation)
- scikit-learn (ML library)
- pandas (Data processing)

### Go
- Gin (Web framework)
- GORM (ORM)
- pq (PostgreSQL driver)

## 🧪 Testing

```bash
# Python tests
cd backend
pytest

# Go tests
cd go-service
go test ./...
```

## 📚 Documentation

- [Backend Documentation](backend/README.md)
- [Go Service Documentation](go-service/README.md)
- [AI/ML Documentation](ai-module/README.md)
- [Frontend Documentation](frontend/README.md)
- [API Documentation](http://localhost:8000/docs) (Swagger UI)

## 🚢 Deployment

### Docker Compose (Production)
```bash
docker-compose -f docker-compose.yml up -d
```

### Heroku
See [DEPLOYMENT.md](DEPLOYMENT.md) for Heroku deployment instructions.

### AWS/GCP
Dockerized services can be deployed to any cloud platform.

## 📝 Submission Requirements

- ✅ GitHub repository link (private, add @bakhtiyar-k as collaborator)
- ✅ Report PDF (6-12 pages)
- ✅ Demo video (3-5 minutes)
- ✅ Contribution table

**Deadline:** June 18, 2026, 23:59

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🆘 Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Contact team leads

---

**Built with ❤️ for Educational Practice 2025-2026 Summer**
