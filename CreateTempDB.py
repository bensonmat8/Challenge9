from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Base(db.Model):
    __tablename__ = 'tbl_Base_Premium'
    Base_Premium = db.Column(db.Integer, primary_key=True)

class Home_Age(db.Model):
    __tablename__ = 'tbl_Factor_Home_Age'
    Home_Age = db.Column(db.String(100), primary_key=True)
    Rating_Factor = db.Column(db.Float)

class Roof(db.Model):
    __tablename__ = 'tbl_Factor_Roof_Type'
    Roof_Type = db.Column(db.String(100), primary_key=True)
    Rating_Factor = db.Column(db.Float)

class Num_Units(db.Model):
    __tablename__ = 'tbl_Factor_Num_Units'
    Num_Units = db.Column(db.Integer, primary_key=True)
    Rating_Factor = db.Column(db.Float)

class Dwelling_Coverage(db.Model):
    __tablename__ = 'tbl_Factor_Dwelling_Coverage'
    Dwelling_Coverage = db.Column(db.Integer, primary_key=True)
    Rating_Factor = db.Column(db.Float)

db.create_all()

base = Base(Base_Premium=350)
db.session.add(base)
db.session.commit()

home_age = Home_Age(Home_Age='0-10', Rating_Factor=1.0)
db.session.add(home_age)
home_age = Home_Age(Home_Age='11-35', Rating_Factor=1.5)
db.session.add(home_age)
home_age = Home_Age(Home_Age='36-100', Rating_Factor=1.8)
db.session.add(home_age)
home_age = Home_Age(Home_Age='100+', Rating_Factor=1.95)
db.session.add(home_age)
db.session.commit()

new_roof = Roof(Roof_Type='Asphalt Shingles', Rating_Factor=1.0)
db.session.add(new_roof)
new_roof = Roof(Roof_Type='Tin', Rating_Factor=1.7)
db.session.add(new_roof)
new_roof = Roof(Roof_Type='Wood', Rating_Factor=2.0)
db.session.add(new_roof)
db.session.commit()

num_units = Num_Units(Num_Units=1, Rating_Factor=1.0)
db.session.add(num_units)
num_units = Num_Units(Num_Units=2, Rating_Factor=0.8)
db.session.add(num_units)
num_units = Num_Units(Num_Units=3, Rating_Factor=0.8)
db.session.add(num_units)
num_units = Num_Units(Num_Units=4, Rating_Factor=0.8)
db.session.add(num_units)
db.session.commit()

dwell = Dwelling_Coverage(Dwelling_Coverage=100000, Rating_Factor=0.971)
db.session.add(dwell)
dwell = Dwelling_Coverage(Dwelling_Coverage=150000, Rating_Factor=1.104)
db.session.add(dwell)
dwell = Dwelling_Coverage(Dwelling_Coverage=200000, Rating_Factor=1.314)
db.session.add(dwell)
dwell = Dwelling_Coverage(Dwelling_Coverage=250000, Rating_Factor=1.471)
db.session.add(dwell)
dwell = Dwelling_Coverage(Dwelling_Coverage=300000, Rating_Factor=1.579)
db.session.add(dwell)
dwell = Dwelling_Coverage(Dwelling_Coverage=350000, Rating_Factor=1.762)
db.session.add(dwell)
db.session.commit()