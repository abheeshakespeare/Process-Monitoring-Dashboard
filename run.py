from flask import Flask 
from flask_cors import CORS 
import psutil 
 
app = Flask(__name__) 
CORS(app) 


from app.routes import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)