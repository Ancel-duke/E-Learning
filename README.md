# E-Learning Platform Backend

Django REST API backend for the e-learning platform.

## 🚀 Quick Deploy on Render

### Option 1: Using render.yaml (Recommended)
1. Push this directory to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Update the environment variables in `render.yaml` with your actual values
6. Deploy

### Option 2: Manual Configuration
1. Create a new Web Service on Render
2. Set Build Command: `./build.sh`
3. Set Start Command: `gunicorn wsgi:application --bind 0.0.0.0:$PORT`
4. Add environment variables (see below)

## Environment Variables

Set these in Render dashboard:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.netlify.app,http://localhost:3000
```

## API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/courses/` - List courses
- `POST /api/courses/` - Create course (instructors only)
- `GET /api/courses/{id}/` - Get course details
- `POST /api/courses/{id}/enroll/` - Enroll in course

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your values

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## Project Structure

```
├── elearning_backend/    # Django project settings
├── accounts/            # User authentication app
├── courses/             # Course management app
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── build.sh           # Render build script
├── render.yaml        # Render configuration
└── Procfile          # Alternative deployment config
```
