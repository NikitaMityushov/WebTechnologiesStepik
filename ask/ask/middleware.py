from qa.models import Session
from datetime import datetime


class CheckSessionMiddleware:
    
    def process_request(request):
        try:
            sessid = request.COOKIE.get('sessid')
            session = Session.objects.get(
                key=sessid,
                expires__gt=datetime.now(),
            )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None
