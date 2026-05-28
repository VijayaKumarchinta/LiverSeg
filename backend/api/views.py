import logging
import os
import nibabel as nib
import numpy as np
from PIL import Image
from io import BytesIO

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import authenticate
from django.http import HttpResponse, FileResponse, Http404, JsonResponse

from .models import User, Patient
from .serializers import UserSerializer, PatientSerializer
from .permissions import IsAdminRole, IsRadiologistOrAdmin

logger = logging.getLogger(__name__)

# ── File upload validation ────────────────────────────────────────────────────
MAX_SCAN_SIZE_MB = 500
MAX_PREVIEW_SIZE_MB = 10

def validate_upload(upload_file, allowed_extensions, max_mb):
    """Validate file size and extension before saving."""
    if upload_file.size > max_mb * 1024 * 1024:
        raise ValueError(f"File size exceeds the {max_mb} MB limit.")
    filename = upload_file.name.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"Unsupported file type. Allowed extensions: {', '.join(allowed_extensions)}")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def register(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                first_name=data.get('name', '').split(' ')[0],
                last_name=' '.join(data.get('name', '').split(' ')[1:]),
                role=data.get('role', 'radiologist')
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny],
            throttle_classes=[ScopedRateThrottle], throttle_scope='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Blacklist the refresh token to invalidate the session."""
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'message': 'Logged out successfully.'})
        except TokenError:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        from django.conf import settings
        if not settings.DEBUG:
            return Response(
                {'error': 'Password reset is disabled in production. Token-based flow via email is required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({'error': 'Username and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-scan_date')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ('run_segmentation', 'upload_scan', 'upload_mask',
                           'upload_preview', 'create', 'destroy',
                           'update', 'partial_update'):
            return [IsRadiologistOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_serializer_context(self):
        """Pass request to serializer so it can build absolute URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    # ── POST /api/patients/{id}/upload_scan/ ─────────────────────────────
    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='upload_scan'
    )
    def upload_scan(self, request, pk=None):
        patient = self.get_object()

        ct_file = request.FILES.get('ct_scan')
        if not ct_file:
            return Response(
                {'error': 'No file provided. Send file as multipart field named "ct_scan".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_upload(ct_file,
                allowed_extensions=['.nii', '.nii.gz', '.dcm'],
                max_mb=MAX_SCAN_SIZE_MB)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if patient.ct_scan:
            patient.ct_scan.delete(save=False)

        patient.ct_scan = ct_file
        patient.has_file = True
        patient.status = 'Ready'
        patient.save()

        serializer = self.get_serializer(patient)
        return Response({
            'message': f'CT scan uploaded successfully for patient {patient.id}',
            'ct_scan_url': serializer.data.get('ct_scan_url'),
            'patient': serializer.data
        }, status=status.HTTP_200_OK)

    # ── POST /api/patients/{id}/upload_mask/ ─────────────────────────────
    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='upload_mask'
    )
    def upload_mask(self, request, pk=None):
        patient = self.get_object()

        mask_file = request.FILES.get('liver_mask')
        if not mask_file:
            return Response(
                {'error': 'No file provided. Send file as multipart field named "liver_mask".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_upload(mask_file,
                allowed_extensions=['.nii', '.nii.gz', '.png', '.jpg', '.jpeg'],
                max_mb=MAX_SCAN_SIZE_MB)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if patient.liver_mask:
            patient.liver_mask.delete(save=False)

        patient.liver_mask = mask_file
        patient.save()

        serializer = self.get_serializer(patient)
        return Response({
            'message': f'Liver mask uploaded successfully for patient {patient.id}',
            'liver_mask_url': serializer.data.get('liver_mask_url'),
            'patient': serializer.data
        }, status=status.HTTP_200_OK)

    # ── POST /api/patients/{id}/upload_preview/ ───────────────────────────
    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='upload_preview'
    )
    def upload_preview(self, request, pk=None):
        patient = self.get_object()

        preview_file = request.FILES.get('preview_image')
        if not preview_file:
            return Response(
                {'error': 'No file provided. Send file as multipart field named "preview_image".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_upload(preview_file,
                allowed_extensions=['.png', '.jpg', '.jpeg'],
                max_mb=MAX_PREVIEW_SIZE_MB)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if patient.preview_image:
            patient.preview_image.delete(save=False)

        patient.preview_image = preview_file
        patient.save()

        serializer = self.get_serializer(patient)
        return Response({
            'message': f'Preview image uploaded successfully for patient {patient.id}',
            'preview_image_url': serializer.data.get('preview_image_url'),
            'patient': serializer.data
        }, status=status.HTTP_200_OK)

    # ── POST /api/patients/{id}/run_segmentation/ ─────────────────────────
    @action(
        detail=True,
        methods=['post'],
        url_path='run_segmentation'
    )
    def run_segmentation(self, request, pk=None):
        # ── PRODUCTION SAFETY BLOCK ───────────────────────────────────────
        from django.conf import settings
        if not settings.DEBUG:
            return Response(
                {'error': 'AI segmentation is not yet validated for clinical production use.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # ── END SAFETY BLOCK ─────────────────────────────────────────────

        patient = self.get_object()

        if not patient.ct_scan and not patient.has_file:
            return Response(
                {'error': 'No CT scan uploaded for this patient. Upload a scan first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if patient.status == 'Analyzing':
            return Response(
                {'error': 'Segmentation is already running for this patient.'},
                status=status.HTTP_409_CONFLICT
            )

        from .tasks import segment_liver

        patient.status = 'Analyzing'
        patient.save()

        task = segment_liver.delay(patient.id)

        return Response({
            'status': 'Analyzing',
            'patient_id': patient.id,
            'task_id': task.id,
            'message': (
                'Segmentation initiated. The AI pipeline is processing the CT volume in the background. '
                'Poll GET /api/patients/{id}/ to check status. '
                'Status will update to "Completed" when done.'
            )
        }, status=status.HTTP_202_ACCEPTED)

    # ── GET /api/patients/{id}/slice/?index={i}&type={ct|mask} ───────────
    @action(
        detail=True,
        methods=['get'],
        url_path='slice'
    )
    def get_slice(self, request, pk=None):
        """
        Extract a specific axial slice from a NIfTI volume and return as PNG.
        Parameters:
        - index: integer (axial slice index, default 0)
        - type: 'ct' or 'mask' (default 'ct')
        - ww: window width (default 400)
        - wl: window level (default 40)
        """
        patient = self.get_object()
        slice_idx = int(request.query_params.get('index', 0))
        img_type = request.query_params.get('type', 'ct')

        if img_type == 'ct':
            if not patient.ct_scan:
                return Response({'error': 'No CT scan available.'}, status=404)
            file_path = patient.ct_scan.path
        else:
            if not patient.liver_mask:
                return Response({'error': 'No mask available.'}, status=404)
            file_path = patient.liver_mask.path

        if not os.path.exists(file_path):
            return Response({'error': 'File not found on disk.'}, status=404)

        try:
            img = nib.load(file_path)
            data = img.get_fdata()

            if slice_idx < 0:
                slice_idx = 0
            if slice_idx >= data.shape[2]:
                slice_idx = data.shape[2] - 1

            slice_data = data[:, :, slice_idx]
            slice_data = np.rot90(slice_data)

            if img_type == 'ct':
                ww = float(request.query_params.get('ww', 400))
                wl = float(request.query_params.get('wl', 40))
                vmin = wl - (ww / 2)
                vmax = wl + (ww / 2)
                slice_data = np.clip(slice_data, vmin, vmax)
                slice_data = (slice_data - vmin) / (vmax - vmin) * 255.0
                slice_data = slice_data.astype(np.uint8)
                image = Image.fromarray(slice_data, mode='L')
            else:
                color_map = {
                    0: [0, 0, 0, 0],
                    1: [15, 118, 110, 255],
                    2: [225, 29, 72, 255]
                }
                rgba = np.zeros((slice_data.shape[0], slice_data.shape[1], 4), dtype=np.uint8)
                for class_val, color in color_map.items():
                    rgba[slice_data == class_val] = color
                image = Image.fromarray(rgba, mode='RGBA')

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return HttpResponse(buffer, content_type='image/png')

        except Exception as e:
            logger.exception("Slice extraction failed for patient %s", pk)
            return Response(
                {'error': 'An internal error occurred. Please contact support.'},
                status=500
            )


# ── Protected Media Serving ───────────────────────────────────────────────────
def protected_media(request, path):
    """Serve media files only to authenticated users (JWT-aware)."""
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    from django.conf import settings as django_settings

    auth = JWTAuthentication()
    try:
        result = auth.authenticate(request)
        if result is None:
            raise AuthenticationFailed
    except Exception:
        return JsonResponse({'error': 'Authentication required.'}, status=401)

    full_path = os.path.join(django_settings.MEDIA_ROOT, path)
    if not os.path.exists(full_path):
        raise Http404

    return FileResponse(open(full_path, 'rb'))