# LiverSegAI — Clinical Liver Segmentation AI Workstation

LiverSegAI is an enterprise-grade medical imaging and computer vision platform designed for radiologists, clinicians, researchers, and administrators. The platform performs AI-based liver and lesion segmentations from abdominal CT scans (DICOM, NIfTI formats) and compiles interactive compliance dashboards.

---

## 🛠️ System Prerequisites & Configuration

### 1. Root Environment Settings (`.env`)
Create a `.env` file at the root of the project. A template is provided in `.env.example`:

```env
# PostgreSQL Database Settings
DB_NAME=liverseg_db
DB_USER=liverseg_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Frontend Environment Variables
VITE_API_URL=http://localhost:8000/api
```

---

## 🐍 Backend Setup (Django)

The backend uses Django, Django REST Framework, and SimpleJWT.

1. **Navigate to backend and active virtual environment:**
   ```powershell
   cd backend
   # For Windows:
   .\venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Verify Settings & Database Connectivity:**
   Ensure your local PostgreSQL database is running and credentials match the `.env` values. Run the system check:
   ```bash
   python manage.py check
   ```
4. **Apply Migrations:**
   ```bash
   python manage.py showmigrations
   python manage.py migrate
   ```
5. **Start Django Development Server:**
   ```bash
   python manage.py runserver
   ```

## ⚡ Frontend Setup (Vue 3 / Vite)

The frontend workstation is built using Vue 3, Pinia, Vue Router, TailwindCSS, and Axios.

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install Node modules:**
   ```bash
   npm install
   ```
3. **Start Dev Server:**
   ```bash
   npm run dev
   ```
4. **Production Build Compilation:**
   ```bash
   npm run build
   ```

---

## 🔒 Security Operations

- **Password Reset (`reset_password`):**
  The simplified password reset action is constrained strictly to development mode. It will only execute if `DEBUG = True` is configured in `backend/core/settings.py`. In production, a secure, token-based verification flow via email must be integrated.

---

## 🚀 Production Deployment (Vercel + Render Hybrid)

This is the recommended deployment method for LiversegAI. It runs the frontend on Vercel's global CDN and hosts the backend services on Render.

### 1. Database & Cache Setup (Render)
1. **Create a PostgreSQL Database** on Render:
   - Name it `liverseg-db`.
   - Take note of the Internal connection credentials (host, name, user, password).
2. **Create a Redis Instance** on Render:
   - Name it `liverseg-redis`.
   - Take note of the Internal Redis URL (for Celery queue).

### 2. Django Backend Setup (Render Web Service)
1. **Create a Web Service** on Render:
   - Connect your Git repository.
   - Set **Environment** to `Docker`.
   - Set **Docker Context Path** to `backend`.
   - Set **Dockerfile Path** to `Dockerfile`.
2. **Add a Persistent Disk**:
   - Mount Path: `/app/media`
   - Size: 10 GB (or more depending on scan volumes).
   - *Note: Gunicorn and Celery run in the same container using `backend/start.sh` so they can seamlessly share this disk for processing scans.*
3. **Configure Environment Variables**:
   - `DB_HOST`: Your Render PostgreSQL Host
   - `DB_NAME`: Your Render PostgreSQL Database Name
   - `DB_USER`: Your Render PostgreSQL User
   - `DB_PASSWORD`: Your Render PostgreSQL Password
   - `DB_PORT`: `5432`
   - `CELERY_BROKER_URL`: Your Render Internal Redis URL
   - `CELERY_RESULT_BACKEND`: Your Render Internal Redis URL
   - `SECRET_KEY`: A secure random string (e.g. `openssl rand -hex 32`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*` (or your Render service domain)
   - `CORS_ALLOWED_ORIGINS`: Your Vercel frontend URL (e.g. `https://liverseg-ai.vercel.app`)

### 3. Frontend Setup (Vercel)
1. **Import your Git repository** to Vercel.
2. In the project settings, configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add the following **Environment Variable**:
   - `VITE_API_URL`: `https://your-render-backend-url.onrender.com/api` (the URL of your deployed Render Web Service).

---

## 🐳 Docker Compose Deployment (Alternative: Cloud VPS)

If you prefer to host everything on a single Linux VPS (DigitalOcean, AWS EC2, Hetzner, etc.):

1. **Package the project** on Windows:
   ```powershell
   .\deploy_prep.ps1
   ```
2. **Copy the zip** to your server:
   ```bash
   scp liverseg_production.zip user@your-server-ip:/app/
   ```
3. **Extract and run**:
   ```bash
   unzip liverseg_production.zip
   docker-compose up -d --build
   ```

