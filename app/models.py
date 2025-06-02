from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.String(50), nullable=False)  # department
    created_by = db.Column(db.String(50), nullable=False)   # department

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # or db.Date
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    components = db.Column(db.String(255))  # comma-separated list of inventory item IDs
    assigned_to = db.Column(db.String(50))  # e.g. Sales, or None

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    items_needed = db.Column(db.String(255))  # comma-separated item names or IDs
    fulfilled = db.Column(db.Boolean, default=False)


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True)  # Bank, Cash, All
    balance = db.Column(db.Float, default=0.0)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(100))
    amount = db.Column(db.Float)
    is_paid = db.Column(db.Boolean, default=False)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    company = db.Column(db.String(100))

class Invoice(db.Model):
    __tablename__ = 'invoice'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    items = db.Column(db.String(255))
    total = db.Column(db.Float)
    is_paid = db.Column(db.Boolean, default=False)


