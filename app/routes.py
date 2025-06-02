from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import (
    LoginForm, VendorForm, ExpenseForm, TaskForm,
    InventoryForm, ProductForm, FulfillPOForm, InvoiceApprovalForm, POForm, BuyerForm, InvoiceForm
)
from app import login_manager, db
from app.models import (
    User, Vendor, Expense, Task, InventoryItem,
    Product, PurchaseOrder, Invoice, BankAccount, Buyer
)

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

            # ✅ Redirect based on department
            if user.department == 'Accounting':
                return redirect(url_for('main.accounting_home'))
            elif user.department == 'Inventory':
                return redirect(url_for('main.inventory_home'))
            elif user.department == 'Fulfillment':
                return redirect(url_for('main.fulfillment_home'))
            elif user.department == 'Sales': 
                return redirect(url_for('main.sales_home'))
            else:
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

    inventory_items = InventoryItem.query.all()
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

        used_ids = [int(cid.strip()) for cid in product_form.components.data.split(',')]
        for inv_id in used_ids:
            item = InventoryItem.query.get(inv_id)
            if item:
                db.session.delete(item)

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


@main.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    report_type = request.args.get('type')  # vendor, sales, or po
    data = []

    if report_type == 'vendor':
        data = db.session.query(Vendor.name, Expense.amount, Expense.date).join(Expense).all()
    elif report_type == 'sales':
        data = Invoice.query.order_by(Invoice.id).all()
    elif report_type == 'po':
        data = PurchaseOrder.query.order_by(PurchaseOrder.id).all()

    return render_template('reports.html', report_type=report_type, data=data)

@main.route('/sales')
@login_required
def sales_home():
    if current_user.department != 'Sales':
        return redirect(url_for('main.department_home'))
    return render_template('sales.html', user=current_user)

@main.route('/sales/buyer', methods=['GET', 'POST'])
@login_required
def create_buyer():
    if current_user.department != 'Sales':
        return redirect(url_for('main.department_home'))

    form = BuyerForm()
    if form.validate_on_submit():
        buyer = Buyer(name=form.name.data, email=form.email.data, company=form.company.data)
        db.session.add(buyer)
        db.session.commit()
        flash('Buyer added.')
        return redirect(url_for('main.create_buyer'))

    return render_template('create_buyer.html', form=form)

@main.route('/sales/po', methods=['GET', 'POST'])
@login_required
def create_po():
    if current_user.department != 'Sales':
        return redirect(url_for('main.department_home'))

    form = POForm()
    form.buyer_id.choices = [(b.id, b.name) for b in Buyer.query.all()]
    inventory = InventoryItem.query.all()
    inv_choices = [(i.id, i.item) for i in inventory]

    for i in range(1, 6):
        getattr(form, f'item_{i}').choices = inv_choices

    if form.validate_on_submit():
        selected_items = []
        for i in range(1, 6):
            item_id = getattr(form, f'item_{i}').data
            qty = getattr(form, f'qty_{i}').data
            if item_id and qty:
                selected_items.append((item_id, qty))

        if not selected_items:
            flash("Please select at least one item.")
            return redirect(url_for('main.create_po'))

        # Build PO string like: "2:5,4:3" → item_id:qty
        items_str = ",".join(f"{item}:{qty}" for item, qty in selected_items)

        # Deduct inventory
        for item_id, qty in selected_items:
            inv = InventoryItem.query.get(item_id)
            if inv:
                inv.quantity = max(inv.quantity - qty, 0)

        po = PurchaseOrder(
            title="PO",
            description=f"Due by {form.due_date.data}",
            items_needed=items_str,
            fulfilled=False
        )
        db.session.add(po)
        db.session.commit()
        flash("Purchase Order submitted to Fulfillment.")
        return redirect(url_for('main.create_po'))

    return render_template('create_po.html', form=form)



@main.route('/fulfillment/po', methods=['GET', 'POST'])
@login_required
def fulfillment_po():
    if current_user.department != 'Fulfillment':
        return redirect(url_for('main.department_home'))

    unfulfilled_pos = PurchaseOrder.query.filter_by(fulfilled=False).all()

    if request.method == 'POST':
        po_id = request.form.get('po_id')
        po = PurchaseOrder.query.get(int(po_id))
        if po:
            po.fulfilled = True
            db.session.commit()
            flash('PO marked as fulfilled.')
        return redirect(url_for('main.fulfillment_po'))

    return render_template('fulfillment_po.html', pos=unfulfilled_pos)



@main.route('/sales/invoice', methods=['GET', 'POST'])
@login_required
def create_invoice():
    if current_user.department != 'Sales':
        return redirect(url_for('main.department_home'))

    form = InvoiceForm()
    form.buyer_id.choices = [(b.id, b.name) for b in Buyer.query.all()]
    inventory = InventoryItem.query.all()
    item_choices = [(i.id, i.item) for i in inventory]

    for i in range(1, 6):
        getattr(form, f'item_{i}').choices = item_choices

    if form.validate_on_submit():
        items = []
        total = 0

        for i in range(1, 6):
            item_id = getattr(form, f'item_{i}').data
            qty = getattr(form, f'qty_{i}').data
            price = getattr(form, f'price_{i}').data

            if item_id and qty and price:
                items.append(f"{item_id}:{qty}:{price}")
                total += qty * price

                # Deduct inventory
                inv = InventoryItem.query.get(item_id)
                if inv:
                    inv.quantity = max(inv.quantity - qty, 0)

        invoice = Invoice(
            buyer_id=form.buyer_id.data,
            items=",".join(items),
            total=total,
            is_paid=False
        )
        db.session.add(invoice)
        db.session.commit()
        flash("Invoice created and sent to Accounting.")
        return redirect(url_for('main.create_invoice'))

    return render_template('create_invoice.html', form=form)


@main.route('/accounting/invoices', methods=['GET', 'POST'])
@login_required
def approve_invoice():
    if current_user.department != 'Accounting':
        return redirect(url_for('main.department_home'))

    form = InvoiceApprovalForm()
    unpaid_invoices = Invoice.query.filter_by(is_paid=False).all()
    form.invoice_id.choices = [(inv.id, f"Invoice #{inv.id} - ${inv.total}") for inv in unpaid_invoices]

    if form.validate_on_submit():
        invoice = Invoice.query.get(form.invoice_id.data)
        if invoice:
            invoice.is_paid = True

            account = BankAccount.query.filter_by(type=form.account_type.data).first()
            if not account:
                account = BankAccount(type=form.account_type.data, balance=0.0)
                db.session.add(account)

            account.balance += invoice.total
            db.session.commit()
            flash('Invoice marked as paid and assigned to account.')
            return redirect(url_for('main.approve_invoice'))

    accounts = BankAccount.query.all()
    return render_template('approve_invoice.html', form=form, accounts=accounts)
