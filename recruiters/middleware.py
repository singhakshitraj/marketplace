from .models import Recruiter
from .exceptions import NotARecruiterAccount,LoginException

class CheckRecruiterAccountMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user is None:
            raise LoginException('Login Failed')
        rec = Recruiter.objects.filter(user=request.user)
        if rec is None:
            raise Exception('Unable To Fetch Data From Server')
        if len(rec)!=1:
            raise NotARecruiterAccount('Access denied because this is not a recruiter account.')
        return self.get_response(request)