# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    unitNo = db.Column(db.String(10), nullable=False, unique=True)
    unitName = db.Column(db.String(50), nullable=False)

class InvoiceDetails(db.Model):
    __tablename__ = 'invoice_details'
    id = db.Column(db.Integer, primary_key=True)
    lineNo = db.Column(db.String(10), nullable=False, unique=True)
    productName = db.Column(db.String(100), nullable=False)
    unitNo = db.Column(db.String(10), db.ForeignKey('units.unitNo'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    expiryDate = db.Column(db.Date, nullable=False)
