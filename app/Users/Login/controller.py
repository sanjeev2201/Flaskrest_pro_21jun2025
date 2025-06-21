from flask_restful import Resource
from flask import request,jsonify,Response
from app.Users.Registration.model import Users
from datetime import datetime
import json
from app.Connection.database import Session
import bcrypt


from functools import wraps
import jwt
from flask import request, abort
from flask import current_app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            session = Session()
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = session.query(Users).filter_by(id=data["id"],email=data['email'],status=1).first()
            # current_user = current_user.id
            if not current_user:
                return {
                    "message": "User not found or inactive",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except jwt.ExpiredSignatureError:
            return {
                "message": "Token has expired",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except jwt.InvalidTokenError:
            return {
                "message": "Invalid token",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


class LoginResource(Resource):
    def post(self):
        try:
            session = Session()
            payload = request.json
            Useremail = payload['email']
            UserPassword = payload['password'].encode()
            isuserexist = session.query(Users).filter_by(status=1,email=Useremail).first()
            if isuserexist:
                if bcrypt.checkpw(UserPassword,isuserexist.haspwd.encode()):
                    print('password match')
                    # data = {'message':"login successfully"}
                    token = jwt.encode({"id": isuserexist.id,'email':isuserexist.email}, current_app.config["SECRET_KEY"], algorithm="HS256")
                    data = {
                        'token':token,
                        'message':"login successfully"
                            }
                    
                    return Response(json.dumps(data,default=str),status=200)
                else:
                    print("password mismatch")
                    data = {'message':"password mismatch"}
                    return Response(json.dumps(data,default=str),status=404)
            else:
                print('User not found')
                data = {'message':"User not found"}
                return Response(json.dumps(data,default=str),status=404)
        except Exception as e:
            print(e)
        finally:
            session.close()