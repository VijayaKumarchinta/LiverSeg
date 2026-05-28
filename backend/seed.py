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

    users_data = [
        {
            'username': 'radiologist',
            'role': 'radiologist',
            'first_name': 'Robert',
            'last_name': 'Chen'
        },
        {
            'username': 'admin',
            'role': 'admin',
            'first_name': 'Sarah',
            'last_name': 'Admin'
        },
        {
            'username': 'researcher',
            'role': 'researcher',
            'first_name': 'Alice',
            'last_name': 'Researcher'
        },
        {
            'username': 'clinician',
            'role': 'clinician',
            'first_name': 'Thomas',
            'last_name': 'Clinician'
        },
        {
            'username': 'technician',
            'role': 'technician',
            'first_name': 'Mark',
            'last_name': 'Technician'
        },
    ]

    for ud in users_data:
        user = User.objects.create_user(
            username=ud['username'],
            password=SEED_PASSWORD,
            first_name=ud['first_name'],
            last_name=ud['last_name'],
            role=ud['role']
        )

        user.activities = [
            {
                'id': 1,
                'type': 'success',
                'action': 'System Init',
                'details': f"Created development user {ud['username']}",
                'time': '10:00 AM'
            }
        ]

        user.save()

        print(
            f"Created user: {user.username} "
            f"with role {user.role}"
        )

    print("Seeding mock patient records...")

    patients_data = [
        {
            'id': 'PT-1001-A',
            'name': 'Eleanor Vance',
            'age': 58,
            'gender': 'Female',
            'dob': '1968-04-12',
            'modality': 'CT',
            'status': 'Completed',
            'has_file': True,
            'has_lesions': True,
            'lesion_volume': '142 cc',
            'findings': (
                'Synthetic development record only. '
                'Not for clinical use.'
            ),
            'signature': 'Dr. Robert Chen, MD',
            'metrics': {
                'dice': '96.4%',
                'volume': '1520 cc',
                'iou': '92.8%',
                'precision': '97.1%',
                'recall': '95.8%',
                'confidence': '98.2%'
            },
            'slices': [
                {
                    'slice_index': idx,
                    'liver_size': (
                        0 if (idx < 3 or idx > 17)
                        else (10 - abs(10 - idx)) * 4 + 30
                    ),
                    'liver_x': idx * 0.2,
                    'liver_y': idx * -0.15,
                    'lesion_size': (
                        0.35 + (idx % 3) * 0.1
                        if (8 <= idx <= 13)
                        else 0
                    ),
                    'lesion_x': (
                        idx * 0.2 + 5
                        if (8 <= idx <= 13)
                        else 0
                    ),
                    'lesion_y': (
                        idx * -0.15 - 8
                        if (8 <= idx <= 13)
                        else 0
                    )
                }
                for idx in range(20)
            ]
        }
    ]

    for pd in patients_data:
        patient = Patient.objects.create(
            id=pd['id'],
            name=pd['name'],
            age=pd['age'],
            gender=pd['gender'],
            dob=pd['dob'],
            modality=pd['modality'],
            status=pd['status'],
            has_file=pd['has_file'],
            has_lesions=pd['has_lesions'],
            lesion_volume=pd['lesion_volume'],
            findings=pd['findings'],
            signature=pd['signature'],
            metrics=pd['metrics'],
            slices=pd['slices']
        )

        print(
            f"Created patient case: "
            f"{patient.name} ({patient.id})"
        )

    print("Development seed completed successfully!")


if __name__ == '__main__':
    seed_db()
