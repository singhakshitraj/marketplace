
class AuthException(Exception):
    def __init__(self,message="Auth Exception"):
        self.message = message
        
class UserAlreadyExistsException(Exception):
    def __init__(self,message="User Already Exists!"):
        self.message = message

class UserNotLoggedIn(Exception):
    def __init__(self, message='User Not Logged In!!'):
        self.message = message
        
class CandidateNotFound(Exception):
    def __init__(self, message='Candidate Not Found'):
        self.message = message