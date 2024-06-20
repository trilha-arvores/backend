import jwt

from models import Admin


class AuthenticationService:
    SECRET_KEY = "6rgzQkWPu0uR5Dpc"

    @classmethod
    def generate_token(cls, admin_id: id):
        payload = {"admin_id": admin_id}
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def authenticate(cls, request):
        token = request.headers.get("Authorization")
        if token is None:
            raise Exception('Authorization Header required.')

        admin_id = cls.verify_token(token)
        user = Admin.query.filter_by(id=admin_id).first()
        if None in (admin_id, user):
            raise Exception('Failed to authenticate user.')

        return admin_id

    @classmethod
    def verify_token(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])
            return str(payload["admin_id"])

        except jwt.InvalidTokenError:
            return None
