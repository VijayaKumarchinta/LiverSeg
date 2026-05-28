import logging
import json

audit_logger = logging.getLogger('phi_audit')

class AuditMiddleware:
    PHI_PATHS = ['/api/patients', '/api/users', '/media/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if any(request.path.startswith(p) for p in self.PHI_PATHS):
            audit_logger.info(json.dumps({
                'user': str(request.user),
                'method': request.method,
                'path': request.path,
                'ip': self.get_client_ip(request),
                'status': response.status_code,
                'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            }))
        return response

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')