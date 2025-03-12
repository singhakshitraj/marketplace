

class UserAlreadyExists(Exception):
    def __init__(self,message='User Already Exists'):
        self.messsage = message
        
class IncorrectCredentials(Exception):
    def __init__(self, message='Auth Credentials Incorrect'):
        self.message = message
        
class NotARecruiterAccount(Exception):
    def __init__(self,message='This is not a Recruiter Account'):
        self.message = message

class LoginException(Exception):
    def __init__(self, message='Not Logged In'):
        self.message = message