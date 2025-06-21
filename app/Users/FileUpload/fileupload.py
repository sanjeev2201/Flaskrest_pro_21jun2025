from flask_restful import Resource
from app.Connection.database import Session
from flask import request,jsonify,Response,current_app
# from app import app
import os,json



    

class FileUploadResource(Resource):
    def post(self):
        try:
            session = Session()
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if file:
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
                data = {'message': 'File successfully uploaded'}
                return Response(json.dumps(data,default=str),status=200)
            
        except Exception as e:
            print(e)
        finally:
            session.close()
