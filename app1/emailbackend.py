from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class Emailbackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            print("Found user by email:", user)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
                print("Found user by username:", user)
            except UserModel.DoesNotExist:
                print("User not found")
                return None 
        
        if user.check_password(password):
            print("Stored hashed password:", user.password)
            print("Entered password:", password)
            print("Password correct")
            return user
        else:
            print("Stored hashed password:", user.password)
            print("Entered password:", password)
            print("Password incorrect")
        return None
