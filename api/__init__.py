from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path='/api/static')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akhlaq:akhlaq_1010@localhost/learning'
# app.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://akhlaq:akhlaq_1010@localhost/learning'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'neduet33iacc44&'

