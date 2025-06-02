from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, VendorForm, ExpenseForm, TaskForm, InventoryForm, ProductForm, FulfillPOForm, InvoiceApprovalForm
from app.forms import LoginForm
from app import login_manager



main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.department_home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/home')
@login_required
def department_home():
    return render_template('home.html', user=current_user)

@main.route('/accounting', methods=['GET', 'POST'])
@login_required
def accounting_home():
    if current_user.department != 'Accounting':
        return redirect(url_for('main.department_home'))

    vendor_form = VendorForm()
    expense_form = ExpenseForm()
    task_form = TaskForm()

    # Populate vendor choices for expense form
    expense_form.vendor_id.choices = [(v.id, v.name) for v in Vendor.query.all()]

    if vendor_form.validate_on_submit() and vendor_form.submit.data:
        new_vendor = Vendor(name=vendor_form.name.data)
        db.session.add(new_vendor)
        db.session.commit()
        flash('Vendor created successfully!')
        return redirect(url_for('main.accounting_home'))

    if expense_form.validate_on_submit() and expense_form.submit.data:
        new_expense = Expense(
            vendor_id=expense_form.vendor_id.data,
            amount=float(expense_form.amount.data),
            description=expense_form.description.data,
            date=expense_form.date.data
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense recorded.')
        return redirect(url_for('main.accounting_home'))

    if task_form.validate_on_submit() and task_form.submit.data:
        new_task = Task(
            title=task_form.title.data,
            description=task_form.description.data,
            assigned_to=task_form.assigned_to.data,
            created_by='Accounting'
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task created and assigned.')
        return redirect(url_for('main.accounting_home'))

    tasks = Task.query.filter_by(assigned_to='Accounting').all()
    return render_template('accounting.html', vendor_form=vendor_form, expense_form=expense_form, task_form=task_form, tasks=tasks)


@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory_home():
    if current_user.department != 'Inventory':
        return redirect(url_for('main.department_home'))

    inventory_form = InventoryForm()
    task_form = TaskForm()

    if inventory_form.validate_on_submit() and inventory_form.submit.data:
        new_item = InventoryItem(
            date=inventory_form.date.data,
            item=inventory_form.item.data,
            quantity=int(inventory_form.quantity.data),
            cost=float(inventory_form.cost.data)
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added to inventory.')
        return redirect(url_for('main.inventory_home'))

    if task_form.validate_on_submit() and task_form.submit.data:
        task = Task(
            title=task_form.title.data,
            description=task_form.description.data,
            assigned_to=task_form.assigned_to.data,
            created_by='Inventory'
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created.')
        return redirect(url_for('main.inventory_home'))

    inventory_items = InventoryItem .query.all()
    tasks = Task.query.filter_by(assigned_to='Inventory').all()

    return render_template('inventory.html',
                           inventory_form=inventory_form,
                           task_form=task_form,
                           inventory_items=inventory_items,
                           tasks=tasks)


@main.route('/fulfillment', methods=['GET', 'POST'])
@login_required
def fulfillment_home():
    if current_user.department != 'Fulfillment':
        return redirect(url_for('main.department_home'))

    product_form = ProductForm()
    fulfill_form = FulfillPOForm()
    fulfill_form.po_id.choices = [(po.id, po.title) for po in PurchaseOrder.query.filter_by(fulfilled=False).all()]

    if product_form.validate_on_submit() and product_form.submit.data:
        new_product = Product(
            name=product_form.name.data,
            components=product_form.components.data,
            assigned_to=product_form.assigned_to.data if product_form.assigned_to.data else None
        )
        db.session.add(new_product)

        # Optionally remove inventory items (simulate)
        used_ids = [int(cid.strip()) for cid in product_form.components.data.split(',')]
        for inv_id in used_ids:
            item = InventoryItem.query.get(inv_id)
            if item:
                db.session.delete(item)  # simplistic for test case

        db.session.commit()
        flash('Product created and inventory updated.')
        return redirect(url_for('main.fulfillment_home'))

    if fulfill_form.validate_on_submit() and fulfill_form.submit.data:
        po = PurchaseOrder.query.get(fulfill_form.po_id.data)
        if po:
            po.fulfilled = True
            db.session.commit()
            flash('PO fulfilled.')
        return redirect(url_for('main.fulfillment_home'))

    pos = PurchaseOrder.query.filter_by(fulfilled=False).all()
    products = Product.query.all()
    return render_template('fulfillment.html', product_form=product_form, fulfill_form=fulfill_form, pos=pos, products=products)


@main.route('/bank', methods=['GET', 'POST'])
@login_required
def bank_home():
    if current_user.department != 'Accounting':
        return redirect(url_for('main.department_home'))

    form = InvoiceApprovalForm()
    unpaid = Invoice.query.filter_by(is_paid=False).all()
    form.invoice_id.choices = [(inv.id, f"Invoice #{inv.id} - ${inv.amount}") for inv in unpaid]

    if form.validate_on_submit():
        invoice = Invoice.query.get(form.invoice_id.data)
        if invoice:
            invoice.is_paid = True

            account = BankAccount.query.filter_by(type=form.account_type.data).first()
            if not account:
                account = BankAccount(type=form.account_type.data, balance=0.0)
                db.session.add(account)

            account.balance += invoice.amount
            db.session.commit()
            flash('Invoice marked as paid and assigned to account.')
            return redirect(url_for('main.bank_home'))

    accounts = BankAccount.query.all()
    return render_template('bank.html', form=form, accounts=accounts)
