<div align="center">

# 🎬 WatchQueue

### *Your intelligent productivity hub — media watchlist, to-do, timetable & attendance.*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)

---

*A to-do list for your digital life — movies, classes, books, and everything in between.*
*Paste a YouTube link, streaming URL, or Instagram post — WatchQueue auto-categorizes it,*
*organizes your education by topic, ranks everything by priority, and tracks your attendance.*

[Features](#-features) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
  - [Database Setup](#database-setup)
  - [Running the App](#running-the-app)
- [API Documentation](#-api-documentation)
  - [Authentication](#authentication)
  - [Media Items](#media-items)
  - [To-Do & Leaderboard](#to-do--leaderboard)
  - [Timetable](#timetable)
  - [Attendance](#attendance)
  - [Tags](#tags)
- [Auto-Categorization Engine](#-auto-categorization-engine)
- [Database Schema](#-database-schema)
- [Frontend Pages](#-frontend-pages)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🎯 Overview

**WatchQueue** is a personal productivity hub that combines a **media watchlist**, **to-do list**, **AI-powered timetable extraction**, and **attendance tracking** — all in one place.

The killer feature? **Paste any URL** — YouTube video, Netflix show, Instagram reel, or a Goodreads book — and WatchQueue **automatically categorizes** it using content-based analysis. Assign a **priority score**, and everything — media AND normal tasks — shows up in a **unified leaderboard** ranked by what matters most.

### The Problem
You find a great YouTube tutorial, a movie recommendation, a course you want to take, an assignment to finish, and your timetable just changed — all in the same day. Where do you track it all? Notes app? Browser bookmarks? A random WhatsApp message to yourself? They all get lost.

### The Solution
WatchQueue is a single, organized home for your entire digital life:
1. **Paste a link** → auto-extracts metadata and categorizes (Movie, Education, Book, etc.)
2. **Assign priority** (1–10) → everything ranks in a unified leaderboard
3. **Add normal to-dos** alongside media items — all tracked together
4. **Upload your timetable** → AI extracts subjects per day automatically
5. **Track attendance** → mark present/absent daily, see per-subject percentages

---

## ✨ Features

### 🔗 Smart Link Analysis
- Paste any URL — YouTube, Netflix, Disney+, Instagram, Hotstar, Prime Video, Goodreads
- Automatic metadata extraction (title, thumbnail, channel, duration, description)
- Zero manual data entry — just paste and go

### 🧠 Content-Based Auto-Categorization
- **Multi-signal analysis** using `yt-dlp` for rich metadata extraction
- YouTube Category ID mapping (Education, Film, Sci & Tech, etc.)
- Keyword scanning across title, description, and tags
- Known channel recognition (3Blue1Brown, freeCodeCamp, MIT OCW, etc.)
- Confidence scoring — low confidence prompts manual confirmation

### 📚 Education Hub
Dedicated view for learning content, organized by topic:

| Topic | Example Content |
|-------|----------------|
| 🤖 AI / Machine Learning | Neural networks, GPT, deep learning courses |
| 💻 Computer Science | Algorithms, data structures, OS, compilers |
| 🌐 Web Development | React tutorials, Node.js courses, CSS tricks |
| ℹ️ Information Science | Data science, analytics, information theory |
| 📐 Mathematics | Linear algebra, calculus, statistics |
| 🔬 Science | Physics, chemistry, biology lectures |
| 🎓 General Education | University lectures, MOOCs, tutorials |

### 🎬 Media Categories
| Category | What it includes |
|----------|-----------------|
| 🎬 Movies | Netflix, Disney+, Prime Video, Hotstar content |
| 📚 Education | YouTube tutorials, courses, lectures |
| 🎮 Entertainment | YouTube entertainment, Instagram reels, shorts |
| 📖 Books | Goodreads links, Amazon book pages |
| 🎙️ Podcasts | Podcast links and audio content |
| 📰 Articles | Blog posts, articles, news links |
| 📦 Other | Anything else — user can reclassify |

### 📝 Unified To-Do + Priority Leaderboard
- **Normal to-dos**: Create tasks with title, description, due date, and **priority score (1–10)**
- **Media items as to-dos**: Every video, movie, and book also gets a priority score
- **Unified leaderboard**: ALL items (tasks + videos + movies + books) ranked by priority score
  - 🥇🥈🥉 badges for top 3 items
  - Type badges: 📝 Task, 🎬 Movie, 📚 Education, 🎮 Entertainment, 📖 Book
  - Color-coded priority: 1-3 green, 4-6 yellow, 7-9 orange, 10 red/fire
- **Filter tabs**: All | Tasks Only | Media Only

### 📅 AI-Powered Timetable
- **Upload a photo** of your timetable (printed or screenshot)
- **Google Gemini Vision** extracts subjects, times, and rooms automatically
- **Weekly view**: Mon–Sat grid with editable slots
- **Today's classes**: highlighted at the top for quick reference
- Re-upload anytime when your schedule changes

### 📊 Attendance Tracker
- **Daily attendance**: mark present/absent for each subject (auto-populated from timetable)
- **Calendar view**: monthly grid color-coded by attendance (green/yellow/red/gray)
- **Working day toggle**: mark holidays and cancelled class days
- **Per-subject stats**: attendance percentage with warnings below 75%
- **Overall dashboard**: total working days, attended, overall percentage

### 📈 Progress Tracking
- **Status management**: Unwatched → Watching → Completed / Dropped / On Hold
- **Dashboard stats**: Visual counters by category, status, and priority
- **Education progress**: Track completion across topics

### 🏷️ Custom Tags
- Create personal tags with custom colors
- Attach multiple tags to any media item
- Filter your queue by tag combinations

### 🔐 User Authentication
- Secure JWT-based authentication
- bcrypt password hashing (12 rounds)
- Per-user isolated media libraries
- Rate-limited auth endpoints (brute force protection)

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | High-performance async Python web framework |
| **PostgreSQL** | Relational database for structured data |
| **SQLAlchemy** | ORM with declarative models and migrations |
| **python-jose** | JWT token creation and validation |
| **bcrypt** | Password hashing (salted, adaptive) |
| **yt-dlp** | YouTube/video metadata extraction (no download) |
| **Google Gemini** | AI vision for timetable image extraction |
| **httpx** | Async HTTP client for external API calls |
| **slowapi** | Rate limiting middleware |
| **Pydantic v2** | Request/response validation and serialization |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **HTML5** | Semantic page structure |
| **Vanilla CSS** | Custom design system with glassmorphism |
| **Vanilla JavaScript** | Client-side logic, API calls, DOM manipulation |
| **Google Fonts** | Modern typography (Inter / Outfit) |

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Static)                          │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ Login  │ │Register│ │Dashboard │ │Education │ │To-Do /    │  │
│  │        │ │        │ │  (Hub)   │ │   Hub    │ │Leaderboard│  │
│  └───┬────┘ └───┬────┘ └────┬─────┘ └────┬─────┘ └─────┬─────┘  │
│      │          │           │            │              │         │
│  ┌───┴──────────┴───────────┴────────────┴──────────────┴──────┐ │
│  │               ┌───────────┐  ┌────────────┐                 │ │
│  │               │ Timetable │  │ Attendance │                 │ │
│  │               └─────┬─────┘  └──────┬─────┘                 │ │
│  └─────────────────────┼───────────────┼───────────────────────┘ │
│                        │ fetch()       │                         │
└────────────────────────┼───────────────┼─────────────────────────┘
                         │ REST API      │
┌────────────────────────┼───────────────┼─────────────────────────┐
│                    BACKEND (FastAPI)                              │
│                        │               │                         │
│  ┌──────────┐ ┌────────┴──┐ ┌─────────┴──┐ ┌──────────────────┐ │
│  │Auth      │ │Media      │ │Todos       │ │Timetable /       │ │
│  │Router    │ │Router     │ │Router +    │ │Attendance Router │ │
│  │          │ │           │ │Leaderboard │ │                  │ │
│  └────┬─────┘ └─────┬─────┘ └──────┬─────┘ └────────┬─────────┘ │
│       │             │              │                 │           │
│  ┌────┴─────────────┴──────────────┴─────────────────┴────────┐  │
│  │                  Dependencies Layer                        │  │
│  │         (JWT decode, get_current_user, get_db)             │  │
│  └──────────────────────┬────────────────────────────┘         │  │
│                         │                                      │  │
│  ┌──────────────────────┴──────────────────────────┐           │  │
│  │           Categorizer Engine     Timetable AI   │           │  │
│  │  ┌─────────┐ ┌──────────┐  ┌────────────────┐  │           │  │
│  │  │ yt-dlp  │ │ Keyword  │  │ Gemini Vision  │  │           │  │
│  │  │Metadata │ │ Matcher  │  │ (Image → JSON) │  │           │  │
│  │  └─────────┘ └──────────┘  └────────────────┘  │           │  │
│  └─────────────────────────────────────────────────┘           │  │
│                         │                                      │  │
└─────────────────────────┼──────────────────────────────────────┘  │
                          │ SQLAlchemy ORM                          │
┌─────────────────────────┼────────────────────────────────────────┐
│                   PostgreSQL Database                             │
│  ┌───────┐ ┌────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│  │ users │ │media_items │ │education_metadata│ │    todos      │ │
│  └───────┘ └────────────┘ └──────────────────┘ └──────────────┘ │
│  ┌──────┐  ┌──────────┐  ┌─────────────────┐ ┌──────────────┐  │
│  │ tags │  │media_tags│  │timetable_entries│ │calendar_days │  │
│  └──────┘  └──────────┘  └─────────────────┘ └──────────────┘  │
│                                          ┌────────────────────┐ │
│                                          │attendance_records  │ │
│                                          └────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
todo/
├── README.md
├── backend/
│   ├── .env                    # Environment variables (git-ignored)
│   ├── .env.example            # Template for environment setup
│   ├── .gitignore
│   ├── requirements.txt        # Python dependencies
│   ├── uploads/                # Timetable images (git-ignored)
│   ├── venv/                   # Virtual environment (git-ignored)
│   └── app/
│       ├── __init__.py
│       ├── main.py             # FastAPI app, middleware, static serving
│       ├── database.py         # SQLAlchemy engine, session, Base
│       ├── auth.py             # JWT creation/decode, bcrypt helpers
│       ├── dependencies.py     # get_current_user, require_admin
│       ├── models.py           # SQLAlchemy ORM models
│       ├── schemas.py          # Pydantic v2 request/response schemas
│       ├── categorizer.py      # URL analysis & auto-categorization
│       ├── timetable_ai.py     # Gemini Vision timetable extractor
│       └── routers/
│           ├── __init__.py
│           ├── auth_router.py      # /api/auth/*
│           ├── media_router.py     # /api/media/*
│           ├── tags_router.py      # /api/tags/*
│           ├── todos_router.py     # /api/todos/* + leaderboard
│           ├── timetable_router.py # /api/timetable/*
│           └── attendance_router.py# /api/attendance/*
└── frontend/
    ├── index.html              # Landing page / Login
    ├── register.html           # Registration page
    ├── dashboard.html          # Main hub
    ├── education.html          # Education hub (topic-based view)
    ├── todos.html              # To-Do List + Priority Leaderboard
    ├── timetable.html          # Timetable Manager
    ├── attendance.html         # Attendance Tracker
    ├── styles.css              # Design system & all styles
    └── app.js                  # Shared JS (API client, auth, utils)
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Check |
|------------|---------|-------|
| Python | 3.11+ | `python3 --version` |
| PostgreSQL | 14+ | `psql --version` |
| pip | Latest | `pip --version` |

### Installation

```bash
# 1. Clone / navigate to the project
cd ~/Documents/funprojects/todo

# 2. Set up the Python virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
# Copy the example env file
cp .env.example .env

# Edit with your values
nano .env   # or use any editor
```

**.env** file:
```env
# ── Database ──────────────────────────────────────────────────
# Format: postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/watchqueue

# ── JWT ───────────────────────────────────────────────────────
# Generate a strong key:  python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ── Gemini AI (for timetable extraction) ──────────────────────
# Get a free key from https://aistudio.google.com
GEMINI_API_KEY=your-google-ai-api-key-here
```

### Database Setup

```bash
# Connect to PostgreSQL and create the database
psql -U postgres

CREATE DATABASE watchqueue;
\q
```

> **Note:** Tables are auto-created on first startup via SQLAlchemy's `create_all`.

### Running the App

```bash
# Make sure you're in the backend/ directory with venv activated
cd backend
source venv/bin/activate

# Start the development server
uvicorn app.main:app --reload --port 8000
```

Open your browser:
| URL | What |
|-----|------|
| `http://localhost:8000` | 🏠 Landing page |
| `http://localhost:8000/dashboard.html` | 📊 Dashboard |
| `http://localhost:8000/todos.html` | 📝 To-Do + Leaderboard |
| `http://localhost:8000/education.html` | 📚 Education Hub |
| `http://localhost:8000/timetable.html` | 📅 Timetable |
| `http://localhost:8000/attendance.html` | 📊 Attendance |
| `http://localhost:8000/api/docs` | 📖 Swagger API docs |
| `http://localhost:8000/api/redoc` | 📄 ReDoc API docs |

---

## 📖 API Documentation

Base URL: `http://localhost:8000/api`

### Authentication

All protected endpoints require the `Authorization: Bearer <token>` header.

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "pranav",
  "email": "pranav@example.com",
  "password": "securepassword123"
}
```
**Response** `201 Created`:
```json
{
  "id": "uuid",
  "username": "pranav",
  "email": "pranav@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2026-07-05T10:00:00Z"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "pranav",
  "password": "securepassword123"
}
```
**Response** `200 OK`:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": { "id": "uuid", "username": "pranav", "..." : "..." }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

---

### Media Items

#### Add Media Item (with auto-categorization + priority)
```http
POST /api/media
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=aircAruvnKk",
  "priority_score": 8
}
```
**Response** `201 Created`:
```json
{
  "id": "uuid",
  "url": "https://www.youtube.com/watch?v=aircAruvnKk",
  "title": "But what is a neural network? | Chapter 1, Deep learning",
  "thumbnail_url": "https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg",
  "category": "education",
  "status": "unwatched",
  "platform": "youtube",
  "channel_name": "3Blue1Brown",
  "duration": 1140,
  "priority_score": 8,
  "education_metadata": {
    "topic": "ai_ml",
    "course_name": null,
    "instructor": "3Blue1Brown"
  },
  "confidence": 0.92,
  "tags": [],
  "created_at": "2026-07-05T10:00:00Z"
}
```

#### Analyze URL (preview without saving)
```http
POST /api/media/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=aircAruvnKk"
}
```
**Response** `200 OK`:
```json
{
  "title": "But what is a neural network? | Chapter 1, Deep learning",
  "channel": "3Blue1Brown",
  "description": "Home page: https://www.3blue1brown.com...",
  "thumbnail": "https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg",
  "duration": 1140,
  "platform": "youtube",
  "category": "education",
  "education_topic": "ai_ml",
  "confidence": 0.92
}
```

#### List Media Items
```http
GET /api/media?category=education&status=unwatched&topic=ai_ml&page=1&limit=20
Authorization: Bearer <token>
```
**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `category` | string | Filter: movie, education, entertainment, book, podcast, article, other |
| `status` | string | Filter: unwatched, watching, completed, dropped, on_hold |
| `platform` | string | Filter: youtube, netflix, instagram, etc. |
| `topic` | string | Filter (education only): ai_ml, computer_science, web_dev, etc. |
| `search` | string | Search in title and notes |
| `page` | int | Page number (default: 1) |
| `limit` | int | Items per page (default: 20, max: 100) |

#### Update Media Item
```http
PUT /api/media/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "watching",
  "notes": "Great series, watching chapter 2 next",
  "category": "education",
  "priority_score": 9
}
```

#### Delete Media Item
```http
DELETE /api/media/{id}
Authorization: Bearer <token>
```

#### Get Dashboard Stats
```http
GET /api/media/stats
Authorization: Bearer <token>
```
**Response** `200 OK`:
```json
{
  "total": 42,
  "by_category": {
    "movie": 12,
    "education": 18,
    "entertainment": 8,
    "book": 4
  },
  "by_status": {
    "unwatched": 20,
    "watching": 8,
    "completed": 12,
    "dropped": 2
  },
  "by_topic": {
    "ai_ml": 6,
    "computer_science": 5,
    "web_dev": 4,
    "mathematics": 3
  }
}
```

---

### Tags

#### Create Tag
```http
POST /api/tags
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Must Watch",
  "color": "#FF6B6B"
}
```

#### List Tags
```http
GET /api/tags
Authorization: Bearer <token>
```

#### Attach Tag to Media Item
```http
POST /api/media/{media_id}/tags/{tag_id}
Authorization: Bearer <token>
```

#### Remove Tag from Media Item
```http
DELETE /api/media/{media_id}/tags/{tag_id}
Authorization: Bearer <token>
```

---

### To-Do & Leaderboard

#### Create To-Do
```http
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Complete graph algorithms assignment",
  "description": "BFS, DFS, Dijkstra's implementations",
  "priority_score": 9,
  "due_date": "2026-07-10"
}
```
**Response** `201 Created`:
```json
{
  "id": "uuid",
  "title": "Complete graph algorithms assignment",
  "description": "BFS, DFS, Dijkstra's implementations",
  "priority_score": 9,
  "status": "pending",
  "due_date": "2026-07-10",
  "created_at": "2026-07-05T10:00:00Z"
}
```

#### Unified Priority Leaderboard
```http
GET /api/todos/leaderboard?type=all
Authorization: Bearer <token>
```
**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `type` | string | `all` (default), `todo`, `media` — filter by item type |

**Response** `200 OK`:
```json
[
  {
    "rank": 1,
    "item_type": "todo",
    "id": "uuid",
    "title": "Complete graph algorithms assignment",
    "priority_score": 9,
    "status": "pending",
    "category": null,
    "platform": null,
    "thumbnail_url": null,
    "due_date": "2026-07-10"
  },
  {
    "rank": 2,
    "item_type": "media",
    "id": "uuid",
    "title": "But what is a neural network?",
    "priority_score": 8,
    "status": "unwatched",
    "category": "education",
    "platform": "youtube",
    "thumbnail_url": "https://i.ytimg.com/vi/...",
    "due_date": null
  }
]
```

---

### Timetable

#### Upload Timetable Image (AI extraction)
```http
POST /api/timetable/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: [timetable.jpg]
```
**Response** `201 Created`:
```json
{
  "message": "Timetable extracted successfully",
  "entries": [
    {"day_of_week": "monday", "subject": "Data Structures", "start_time": "09:00", "end_time": "10:00", "room": "LH-301"},
    {"day_of_week": "monday", "subject": "AI & ML", "start_time": "10:00", "end_time": "11:00", "room": "LH-302"}
  ]
}
```

#### Get Full Timetable
```http
GET /api/timetable
Authorization: Bearer <token>
```

#### Get Timetable for a Day
```http
GET /api/timetable/monday
Authorization: Bearer <token>
```

---

### Attendance

#### Record Daily Attendance
```http
POST /api/attendance
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2026-07-05",
  "records": [
    {"subject": "Data Structures", "was_present": true},
    {"subject": "AI & ML", "was_present": false}
  ]
}
```

#### Toggle Working Day
```http
PUT /api/attendance/calendar/2026-07-05
Authorization: Bearer <token>
Content-Type: application/json

{
  "is_working_day": false,
  "notes": "Independence Day holiday"
}
```

#### Get Attendance Stats
```http
GET /api/attendance/stats
Authorization: Bearer <token>
```
**Response** `200 OK`:
```json
{
  "overall_percentage": 82.5,
  "total_working_days": 40,
  "total_attended": 33,
  "by_subject": [
    {"subject": "Data Structures", "total": 12, "attended": 11, "percentage": 91.7},
    {"subject": "AI & ML", "total": 10, "attended": 7, "percentage": 70.0},
    {"subject": "Web Development", "total": 8, "attended": 8, "percentage": 100.0}
  ]
}
```

---

## 🧠 Auto-Categorization Engine

The categorizer is the heart of WatchQueue. When you paste a URL, here's what happens:

### Step 1: Platform Detection
The URL domain determines the platform:
```
youtube.com / youtu.be       → YouTube    → Deep content analysis
instagram.com                → Instagram  → Entertainment
netflix.com                  → Netflix    → Movie
disneyplus.com / hotstar.com → Disney+    → Movie
primevideo.com               → Prime      → Movie
goodreads.com                → Goodreads  → Book
```

### Step 2: Metadata Extraction (via yt-dlp)
For YouTube and other supported sites, `yt-dlp` extracts metadata **without downloading** the video:

| Field | Usage |
|-------|-------|
| Title | Primary keyword source |
| Description | Deep context (syllabus, timestamps, links) |
| Tags | Creator-defined labels |
| Category ID | YouTube's own classification system |
| Channel | Known channel matching |
| Duration | Short vs. lecture distinction |
| Thumbnail | Display in UI |

### Step 3: Multi-Signal Classification

```
┌─────────────────────────────────────────────────┐
│              Categorization Pipeline             │
│                                                  │
│  URL ──→ Platform ──→ yt-dlp Extract ──→ Score  │
│                          │                       │
│              ┌───────────┼───────────┐           │
│              ▼           ▼           ▼           │
│         YT Category   Keywords    Channel        │
│          ID Match      Scan       Match          │
│          (High)       (High)     (Medium)        │
│              │           │           │           │
│              └───────────┼───────────┘           │
│                          ▼                       │
│                   Weighted Score                  │
│                   + Confidence                   │
│                          │                       │
│              ┌───────────┼───────────┐           │
│              ▼           ▼           ▼           │
│          Category    Edu Topic   Confidence      │
│         (education)   (ai_ml)     (0.92)        │
└─────────────────────────────────────────────────┘
```

### Step 4: Education Topic Sub-Classification

If the content is classified as **education**, a second pass determines the specific topic:

| Topic | Keyword Signals |
|-------|----------------|
| 🤖 AI / ML | machine learning, deep learning, neural network, GPT, LLM, transformer, NLP, computer vision |
| 💻 Computer Science | algorithm, data structure, programming, OS, compiler, DSA, leetcode |
| ℹ️ Information Science | data science, big data, analytics, information retrieval, visualization |
| 🌐 Web Development | react, javascript, frontend, backend, fullstack, node.js, django, CSS |
| 📐 Mathematics | calculus, linear algebra, statistics, probability, discrete math |
| 🔬 Science | physics, chemistry, biology, astronomy, quantum mechanics |
| 🎓 General | lecture, course, tutorial, university, professor, class |

### YouTube Category ID Mapping

| ID | YouTube Category | WatchQueue Category |
|----|-----------------|-------------------|
| 1 | Film & Animation | Movie |
| 2 | Autos & Vehicles | Other |
| 10 | Music | Entertainment |
| 15 | Pets & Animals | Entertainment |
| 17 | Sports | Entertainment |
| 20 | Gaming | Entertainment |
| 22 | People & Blogs | Entertainment |
| 23 | Comedy | Entertainment |
| 24 | Entertainment | Entertainment |
| 25 | News & Politics | Article |
| 26 | Howto & Style | Education |
| 27 | Education | Education |
| 28 | Science & Technology | Education |
| 43 | Shows | Movie |

---

## 🗄️ Database Schema

```
┌──────────────────────┐       ┌──────────────────────────────────┐
│       users           │       │          media_items              │
├──────────────────────┤       ├──────────────────────────────────┤
│ id         UUID  PK  │───┐   │ id              UUID  PK         │
│ username   VARCHAR(50)│   │   │ user_id         UUID  FK ────────┤
│ email      VARCHAR    │   │   │ url             TEXT              │
│ hashed_pw  TEXT       │   └──▶│ title           VARCHAR(500)     │
│ role       ENUM      │       │ description     TEXT              │
│ is_active  BOOLEAN   │       │ thumbnail_url   TEXT              │
│ created_at TIMESTAMP │       │ category        ENUM              │
└──────────────────────┘       │ status          ENUM              │
                                │ platform        ENUM              │
                                │ channel_name    VARCHAR(200)      │
                                │ duration        INTEGER           │
                                │ priority_score  INTEGER (1–10)    │
                                │ notes           TEXT              │
                                │ confidence      FLOAT             │
                                │ created_at      TIMESTAMP         │
                                │ updated_at      TIMESTAMP         │
                                └────────┬──────────┬──────────────┘
                                         │          │
                     ┌───────────────────┘          │
                     ▼                               ▼
    ┌──────────────────────────┐    ┌──────────────────────────┐
    │   education_metadata      │    │       media_tags          │
    ├──────────────────────────┤    ├──────────────────────────┤
    │ id           UUID  PK    │    │ media_item_id UUID FK    │
    │ media_item_id UUID FK    │    │ tag_id        UUID FK    │
    │ topic        ENUM        │    └────────────┬─────────────┘
    │ course_name  VARCHAR     │                  │
    │ instructor   VARCHAR     │                  ▼
    └──────────────────────────┘    ┌──────────────────────────┐
                                    │         tags              │
┌──────────────────────────┐        ├──────────────────────────┤
│         todos             │        │ id        UUID  PK       │
├──────────────────────────┤        │ user_id   UUID  FK       │
│ id           UUID  PK    │        │ name      VARCHAR(50)    │
│ user_id      UUID  FK    │        │ color     VARCHAR(7)     │
│ title        VARCHAR(200)│        └──────────────────────────┘
│ description  TEXT        │
│ priority_score INT (1-10)│  ┌──────────────────────────┐
│ status       ENUM        │  │   timetable_entries       │
│ due_date     DATE        │  ├──────────────────────────┤
│ created_at   TIMESTAMP   │  │ id           UUID  PK    │
└──────────────────────────┘  │ user_id      UUID  FK    │
                               │ day_of_week  ENUM        │
┌──────────────────────────┐  │ subject      VARCHAR     │
│     calendar_days         │  │ start_time   TIME        │
├──────────────────────────┤  │ end_time     TIME        │
│ id           UUID  PK    │  │ room         VARCHAR     │
│ user_id      UUID  FK    │  └──────────────────────────┘
│ date         DATE        │
│ is_working   BOOLEAN     │  ┌──────────────────────────┐
│ notes        VARCHAR     │  │   attendance_records      │
└──────────────────────────┘  ├──────────────────────────┤
                               │ id           UUID  PK    │
                               │ user_id      UUID  FK    │
                               │ date         DATE        │
                               │ subject      VARCHAR     │
                               │ was_present  BOOLEAN     │
                               └──────────────────────────┘
```

### Enum Values

```sql
-- User roles
CREATE TYPE userrole AS ENUM ('user', 'admin');

-- Media categories
CREATE TYPE mediacategory AS ENUM (
  'movie', 'education', 'entertainment',
  'book', 'podcast', 'article', 'other'
);

-- Watch status
CREATE TYPE mediastatus AS ENUM (
  'unwatched', 'watching', 'completed', 'dropped', 'on_hold'
);

-- To-do status
CREATE TYPE todostatus AS ENUM (
  'pending', 'in_progress', 'completed', 'cancelled'
);

-- Platform sources
CREATE TYPE mediaplatform AS ENUM (
  'youtube', 'netflix', 'prime_video', 'disney_plus',
  'instagram', 'hotstar', 'other'
);

-- Education topics
CREATE TYPE educationtopic AS ENUM (
  'ai_ml', 'computer_science', 'information_science',
  'web_dev', 'mathematics', 'science', 'general'
);

-- Days of week
CREATE TYPE dayofweek AS ENUM (
  'monday', 'tuesday', 'wednesday', 'thursday',
  'friday', 'saturday', 'sunday'
);
```

---

## 🎨 Frontend Pages

### 🏠 Landing / Login (`index.html`)
- Sleek login form with animated gradient background
- Glassmorphic card design
- Smooth transitions to registration

### 📝 Register (`register.html`)
- Registration form with real-time validation
- Password strength indicator
- Matching dark theme design

### 📊 Dashboard (`dashboard.html`)
The main hub with navigation to all sections:
- **Quick Add bar** — paste URL → auto-categorize → assign priority → add
- **Stats overview** — animated counters for total, top priority, today's classes, attendance %
- **Category tabs** — All | 🎬 Movies | 📚 Education | 🎮 Entertainment | 📖 Books
- **Media cards** — glassmorphic cards with thumbnails, platform badges, priority score, status dropdowns
- **Navigation** — sidebar links to To-Do, Timetable, Attendance, Education Hub

### 📝 To-Do + Leaderboard (`todos.html`)
Unified view combining normal tasks AND media items:
- **Add to-do form** — title, description, priority score (1–10 slider), due date
- **Add media shortcut** — paste URL → auto-categorize → assign priority
- **Leaderboard** — ALL items ranked by priority with 🥇🥈🥉 badges, type badges (📝 Task, 🎬 Movie, 📚 Education, etc.), color-coded priority
- **Filter tabs** — All | 📝 Tasks Only | 🎬 Media Only

### 📚 Education Hub (`education.html`)
- Topic-based sections (AI, CS, Web Dev, Math, etc.)
- Progress tracking per topic
- Class-like organization with completion percentages
- Instructor/channel grouping

### 📅 Timetable (`timetable.html`)
- **Drag-and-drop upload** — upload timetable photo for AI extraction
- **Preview & confirm** — review extracted subjects before saving
- **Weekly grid view** — Mon–Sat with subject slots, times, rooms
- **Today's classes** — highlighted section showing what's on today
- **Edit mode** — click any slot to manually adjust

### 📊 Attendance (`attendance.html`)
- **Today's attendance** — subject list with present/absent toggle buttons
- **Calendar view** — monthly grid color-coded by attendance
- **Working day toggle** — click any date to mark holidays
- **Subject stats** — per-subject attendance % with progress bars
- **Alerts** — warnings for subjects below 75%

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🗺️ Roadmap

- [x] Core architecture design
- [ ] Backend API with FastAPI
- [ ] JWT authentication
- [ ] Auto-categorization engine with yt-dlp
- [ ] Unified to-do list with priority scoring
- [ ] Priority leaderboard (media + tasks combined)
- [ ] AI timetable extraction with Gemini Vision
- [ ] Attendance tracker with calendar view
- [ ] PostgreSQL models and schemas
- [ ] Frontend dashboard with glassmorphism UI
- [ ] Education hub with topic-based views
- [ ] Custom tag system
- [ ] Drag-and-drop reordering
- [ ] Browser extension for quick-add
- [ ] Mobile responsive PWA
- [ ] Sharing watchlists with friends
- [ ] AI-powered recommendations
- [ ] Import from YouTube Watch Later playlist

---

## 📄 License

This project is for personal use. Feel free to fork and modify.

---

<div align="center">

**Built with ❤️ by [@pranavperingeth](https://github.com/pranavperingeth)**

*Stop losing track of what you want to watch. Start queueing.*

</div>
