from django.contrib.auth.models import User


def create_login_user(name, email, password):
    USER_USERNAME = name
    USER_EMAIL = email
    USER_PASSWORD = password
    # Create user
    user_data = {
        "username": USER_USERNAME,
        "email": USER_EMAIL,
        "password": USER_PASSWORD,
    }
    user2 = User._default_manager.create_user(**user_data)
    user2.save()
