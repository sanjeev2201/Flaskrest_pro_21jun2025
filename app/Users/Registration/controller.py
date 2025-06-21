from flask_restful import Resource
from flask import request,jsonify,Response
from .model import Users
from datetime import datetime
import json,hashlib
import bcrypt
from app.Connection.database import Session
from app.Users.Login.controller import token_required
class UserResource(Resource):
    def get(self):
        try:
            # print(f"Uurrent Users: {current_user}")
            session = Session()
            users = session.query(Users).filter_by(status = 1).all()
            TrashAllusers = session.query(Users).filter_by(status = 0).all()
            TrashUsers = session.query(Users).filter_by(status = 0).count()
            AllUsers = session.query(Users).count()
            TrashAllusersdata = GetAllUsers(TrashAllusers)
            if len(users)>0:
                data = GetAllUsers(users)
                data = {"data":data,"TrashAllusers":TrashAllusersdata,"AllUsers":AllUsers,'ActiveUsers':len(data),'TrashUsers':TrashUsers}
                return Response(json.dumps(data,default=str),status=200)
            else:
                data = {"data":[],"TrashAllusers":TrashAllusersdata,'AllUsers':AllUsers,'ActiveUsers':0,'TrashUsers':TrashUsers}
                return Response(json.dumps(data,default=str),status=200)
                
            
        except Exception as e:
            print(e)
        finally:
            session.close()

    def post(self):
        try:
            session = Session()
            payload = request.json
            payload['status'] = 1
            result = CheckUserEmail(payload['email'])
            if result['message']=='error':
                data = {'message':"email already exist"}
                return jsonify(data)
            # Hashpwd = hashlib.md5(payload['password']).hexdigest()
            pwd = payload['password'].encode()
            payload['haspwd'] = bcrypt.hashpw(pwd, bcrypt.gensalt())
            payload['username'] = payload['firstName'] +' '+ payload['lastName']
            payload.pop('firstName',None)
            payload.pop('lastName',None)
            Insert = Users(**payload)
            session.add(Insert)
            session.commit()
            data = {'message':"Registration added sucessfully"}
            return Response(json.dumps(data,default=str),status=201)
        except Exception as e:
            session.rollback()  # Roll back the session to undo changes if an error occurs
            msg = f"Error inserting user: {e}"
            data = {'message':msg}
            return jsonify(data)
        finally:
            session.close()  # Close the session to release resources
    @token_required
    def put(self,current_user):
        try:
            # print(f"Updated user: {current_user}")
            
            # # Debug output to check current_user type and attributes
            # print(f"Type of current_user: {type(current_user)}")
            # a = current_user()
            # print(current_user.id)
            # print(f"Attributes of current_user: {dir(current_user)}")
            payload = request.json
            ID = payload['id']
            session = Session()
            payload = request.json
            
            session.query(Users).filter_by(id = ID,status=1).update({Users.username:payload['username'],
                                                                    Users.phone:payload['phone'],
                                                                    Users.Updated_date:datetime.now()})

            session.commit()
            data = {'message':'User updated successfully'}
            return Response(json.dumps(data,default=str),status=200)
                
        except Exception as e:
            print(e)
        finally:
            session.close()
    def patch(self):
        session = Session()
        try:
            payload = request.json
            Userid = payload['id']
            data = session.query(Users).filter_by(id= Userid,status=0).first()
            data.status = 1
            data.Updated_date = datetime.now()
            session.merge(data)
            session.commit()
            data = {'message':'User Restore successfully'}
            return Response(json.dumps(data,default=str),status=200)
    
        except Exception as e:
            print(e)
        finally:
            session.close()
    def delete(self):
        try:
            payload = request.json
            ID = payload['id']
            session = Session()
            data = session.query(Users).filter_by(id= ID,status=1).first()
            data.status = 0
            data.Updated_date = datetime.now()
            session.merge(data)
            session.commit()
            data = {'message':'User deleted successfully'}
            return Response(json.dumps(data,default=str),status=200)
    
        except Exception as e:
            print(e)
        finally:
            session.close()


def GetAllUsers(Users):
    AllUsers = [user.ConvertToDict() for user in Users]
    return AllUsers

def CheckUserEmail(Email):
    try:
        session = Session()
        data = session.query(Users).filter_by(email = Email,status=1).first()
        if data:
            errormsg = {"message":"error"}
            return errormsg
        else:
            successmsg = {"message":"success"}
            return successmsg
    except Exception as e:
        errormsg = {"error":e}
        return errormsg


