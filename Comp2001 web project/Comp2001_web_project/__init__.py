import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SKerslake:TkrC780+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_SKerslake?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create_app():
    from Comp2001_web_project import views 
    from Comp2001_web_project import models  
    
    
    return app


with app.app_context():
    try:
        db.engine.connect() 
        print("Database connected successfully!")
    except Exception as e:
        print("Error connecting to the database:", e)


if __name__ == "__main__":
    app = create_app()  
    print(app.url_map)  
    app.run(host="0.0.0.0", port=8000)