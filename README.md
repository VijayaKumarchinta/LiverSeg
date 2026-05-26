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

---

## ⚡ Frontend Setup (Vue 3 / Vite)

The frontend workstation is built using Vue 3, Pinia, Vue Router, TailwindCSS, and Axios.

1. **Install Node modules:**
   ```bash
   npm install
   ```
2. **Start Dev Server:**
   ```bash
   npm run dev
   ```
3. **Production Build Compilation:**
   ```bash
   npm run build
   ```

---

## 🔒 Security Operations

- **Password Reset (`reset_password`):**
  The simplified password reset action is constrained strictly to development mode. It will only execute if `DEBUG = True` is configured in `backend/core/settings.py`. In production, a secure, token-based verification flow via email must be integrated.
