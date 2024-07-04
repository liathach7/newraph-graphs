from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
#from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)

#sess=Session(app)
#with app.app_context():
 #   db.create_all()


from app import routes,models