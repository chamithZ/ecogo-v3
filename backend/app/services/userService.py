from app.models.user import User

class UserService:
    
    @staticmethod
    def register_user(data):
        return User.create_user(data)

    @staticmethod
    def get_user(user_id):
        return User.get_user_by_id(user_id)

    @staticmethod
    def authenticate_user(email, password):
        return User.verify_password(email, password)
