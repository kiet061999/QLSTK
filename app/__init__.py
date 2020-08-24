from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://root:kiet01685258917@localhost/stk_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key='\xeen\x83\xfe\xe2\xd9ZS\x02\x7f_f\xeb\xde\xa2\xd4'

db = SQLAlchemy(app=app)
admin = Admin(app=app, name= "QUAN LY SO TIET KIEM", template_mode="bootstrap3")

