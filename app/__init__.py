from flask import Flask
from flask_restful import Api
from app.Users.Registration.controller import UserResource
from app.Users.Login.controller import LoginResource
from app.Users.FileUpload.fileupload import FileUploadResource
from flask_cors import CORS
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY') or '24234gdfgijghjgfj@$#%^#^'
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# Define API routes
api.add_resource(UserResource, '/register')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(FileUploadResource, '/fileupload')

if __name__ == "__main__":
    app.run(debug=True)