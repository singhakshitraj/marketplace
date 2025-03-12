from .models import Candidates
from .exceptions import UserNotLoggedIn,CandidateNotFound

class CheckCandidateAccountMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self,request):
        cands = Candidates.objects.filter(user=request.user)
        if cands is None:
            raise UserNotLoggedIn('User Not Logged In!!')
        elif len(cands)<1:
            raise CandidateNotFound('Not Logged In As Candidate')
        return self.get_response(request)