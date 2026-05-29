import os
import django
from django.conf import settings

# ─────────────────────────────────────────────────────────────
# BLOCK SEEDING IN PRODUCTION
# ─────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

if not settings.DEBUG:
    raise RuntimeError(
        "seed.py is disabled in production environments."
    )

# ─────────────────────────────────────────────────────────────
# IMPORT MODELS
# ─────────────────────────────────────────────────────────────
from api.models import User, Patient

# ─────────────────────────────────────────────────────────────
# SAFE DEV PASSWORD
# ─────────────────────────────────────────────────────────────
SEED_PASSWORD = os.getenv(
    'SEED_USER_PASSWORD',
    'DevOnlyPassword123!'
)

# ─────────────────────────────────────────────────────────────
# SEED DATABASE
# ─────────────────────────────────────────────────────────────
def seed_db():
    print("Clearing existing data...")

    Patient.objects.all().delete()
    User.objects.all().delete()

    print("Seeding development clinical users...")

if __name__ == '__main__':
    seed_db()
