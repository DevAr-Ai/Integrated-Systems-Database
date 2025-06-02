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
