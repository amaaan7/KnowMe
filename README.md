# KnowMe

A full stack social blogging platform built with Django and Django REST Framework. Users can register, create posts, like, comment, view announcements, and browse upcoming events — all with a clean, responsive UI.

**Live Demo:** [know-me-xi.vercel.app](https://know-me-xi.vercel.app) &nbsp;|&nbsp; **Backend:** [Railway](https://knowme-production-58be.up.railway.app/)

---

## Features

- **Authentication** — Register, login, logout, password reset via email
- **User Profiles** — Custom profile with avatar upload
- **Posts** — Create, read, update, delete blog posts with pagination
- **Likes** — Real-time like/unlike with instant UI feedback (no page reload)
- **Comments** — Add and delete comments via AJAX
- **Announcements** — Staff-only announcements with importance flags
- **Events / Calendar** — Upcoming event listings
- **REST API** — JSON endpoints for posts and likes via Django REST Framework
- **Deployed** — Railway (backend + PostgreSQL) 

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 4.2 |
| REST API | Django REST Framework 3.16 |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Frontend | Django Templates, Bootstrap 5, Vanilla JS |
| Auth | Django built-in auth + crispy forms |
| Storage | Whitenoise (static), Pillow (images) |
| Deployment | Railway |

---

## Project Structure

```
KnowMe/
├── blog/                   # Main app — posts, likes, comments, announcements, events
│   ├── models.py           # Post, Like, Comment, Announcement, Event
│   ├── views.py            # Class-based + function views, AJAX endpoints
│   ├── urls.py             # All blog routes
│   ├── forms.py            # CommentForm
│   ├── serializers.py      # Post serializer for API
│   └── templates/blog/     # All HTML templates
│       ├── base.html       # Base layout with navbar + like system JS
│       ├── home.html       # Post feed with like/comment interaction bar
│       ├── post_detail.html# Single post + comments
│       └── ...
├── api/                    # REST API app
│   ├── views.py            # post_list_api, toggle_like_api
│   └── urls.py             # /api/posts/, /api/posts/<id>/like/
├── users/                  # User registration + profile
│   ├── views.py
│   └── templates/users/
├── django_project/         # Project settings + root urls
│   ├── settings.py
│   └── urls.py
├── media/                  # User uploaded files
├── requirements.txt
├── manage.py
└── vercel.json
```

---

## Getting Started (Local Setup)

### 1. Clone the repo

```bash
git clone https://github.com/amaaan7/KnowMe.git
cd KnowMe
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/posts/` | List all posts |
| POST | `/api/posts/<id>/like/` | Toggle like on a post (auth required) |

### Example response — toggle like

```json
{
  "liked": true,
  "like_count": 5
}
```

Returns `401` with a redirect URL if the user is not authenticated.

---

## Key Implementation Details

### Like System
Likes are handled entirely via AJAX with optimistic UI — the count updates instantly on click without waiting for the server response. A `unique_together` constraint on the `Like` model (`user` + `post`) prevents duplicate likes at the database level. The toggle logic lives in `api/views.py → toggle_like_api`.

### Real-time Comments
Comments are posted and deleted via `fetch()` without page reload. New comments are injected into the DOM immediately after the server confirms success.

### Annotations
The `PostListView` uses Django ORM annotations (`Count`, `Exists`, `OuterRef`) to calculate `like_count`, `comment_count`, and `is_liked` per user in a single query — avoiding N+1 queries.

```python
qs = qs.annotate(
    like_count=Count("like", distinct=True),
    comment_count=Count("comments", distinct=True),
    is_liked=Exists(Like.objects.filter(post=OuterRef("pk"), user=user))
)
```

---

## Deployment (Railway)

1. Push code to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Add a PostgreSQL database service
4. Set environment variables:
   ```
   SECRET_KEY=...
   DEBUG=False
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=your-railway-domain.up.railway.app
   ```
5. Railway auto-deploys on every push to `main`

---

## Screenshots

> Add screenshots here after deployment  
> Tip: Use `![Home Page](screenshots/home.png)` syntax

---

## Future Improvements

- [ ] Search posts by keyword
- [ ] Follow/unfollow users
- [ ] Notifications for likes and comments
- [ ] React frontend consuming the REST API
- [ ] Image uploads for posts

---

## Author

**Amaan Mulla**  
B.Tech Data Science, Dr. D.Y. Patil Pratishthan's College of Engineering  
[LinkedIn](https://www.linkedin.com/in/amaanmulla231/) · [GitHub](https://github.com/amaaan7)
