from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class VendorForm(FlaskForm):
    name = StringField('Vendor Name', validators=[DataRequired()])
    submit = SubmitField('Create Vendor')

class ExpenseForm(FlaskForm):
    vendor_id = SelectField('Vendor', coerce=int)
    amount = StringField('Amount', validators=[DataRequired()])
    description = StringField('Description')
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    description = StringField('Description')
    assigned_to = SelectField('Assign To Department', choices=[
        ('Accounting', 'Accounting'),
        ('Sales', 'Sales'),
        ('Inventory', 'Inventory'),
        ('Fulfillment', 'Fulfillment')
    ])
    submit = SubmitField('Create Task')

class InventoryForm(FlaskForm):
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    item = StringField('Item Name', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Add to Inventory')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    components = StringField('Components (comma-separated inventory item IDs)', validators=[DataRequired()])
    assigned_to = SelectField('Assign To', choices=[
        ('', 'Keep in Inventory'),
        ('Sales', 'Sales'),
        ('Accounting', 'Accounting'),
        ('Inventory', 'Inventory'),
        ('Fulfillment', 'Fulfillment')
    ])
    submit = SubmitField('Create Product')

class FulfillPOForm(FlaskForm):
    po_id = SelectField('Purchase Order', coerce=int)
    submit = SubmitField('Mark as Fulfilled')


class InvoiceApprovalForm(FlaskForm):
    invoice_id = SelectField('Invoice to Approve', coerce=int)
    account_type = SelectField('Assign to Account', choices=[
        ('Bank', 'Bank'),
        ('Cash', 'Cash'),
        ('All', 'All')
    ])
    submit = SubmitField('Mark Paid and Assign')


class BuyerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email')
    company = StringField('Company')
    submit = SubmitField('Add Buyer')

from wtforms import SelectField, IntegerField, DateField

class POForm(FlaskForm):
    buyer_id = SelectField('Buyer', coerce=int)
    item_1 = SelectField('Item 1', coerce=int)
    qty_1 = IntegerField('Qty 1')
    due_date = DateField('Due Date', format='%Y-%m-%d')
    submit = SubmitField('Create Purchase Order')

class POForm(FlaskForm):
    buyer_id = SelectField('Buyer', coerce=int)
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])

    item_1 = SelectField('Item 1', coerce=int)
    qty_1 = IntegerField('Qty 1')

    item_2 = SelectField('Item 2', coerce=int)
    qty_2 = IntegerField('Qty 2')

    item_3 = SelectField('Item 3', coerce=int)
    qty_3 = IntegerField('Qty 3')

    item_4 = SelectField('Item 4', coerce=int)
    qty_4 = IntegerField('Qty 4')

    item_5 = SelectField('Item 5', coerce=int)
    qty_5 = IntegerField('Qty 5')

    submit = SubmitField('Create Purchase Order')


class InvoiceForm(FlaskForm):
    buyer_id = SelectField('Buyer', coerce=int)

    item_1 = SelectField('Item 1', coerce=int)
    qty_1 = IntegerField('Qty 1')
    price_1 = IntegerField('Price 1')

    item_2 = SelectField('Item 2', coerce=int)
    qty_2 = IntegerField('Qty 2')
    price_2 = IntegerField('Price 2')

    item_3 = SelectField('Item 3', coerce=int)
    qty_3 = IntegerField('Qty 3')
    price_3 = IntegerField('Price 3')

    item_4 = SelectField('Item 4', coerce=int)
    qty_4 = IntegerField('Qty 4')
    price_4 = IntegerField('Price 4')

    item_5 = SelectField('Item 5', coerce=int)
    qty_5 = IntegerField('Qty 5')
    price_5 = IntegerField('Price 5')

    submit = SubmitField('Create Invoice')


class InvoiceApprovalForm(FlaskForm):
    invoice_id = SelectField('Invoice to Approve', coerce=int)
    account_type = SelectField('Assign to Account', choices=[
        ('Bank', 'Bank'),
        ('Cash', 'Cash'),
        ('All', 'All')
    ])
    submit = SubmitField('Mark as Paid')
