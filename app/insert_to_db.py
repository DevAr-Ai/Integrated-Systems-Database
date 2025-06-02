from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    users = [
        User(username='sales', department='Sales', password='234'),
        User(username='accounting', department='Accounting', password='123'),
        User(username='inventory', department='Inventory', password='345'),
        User(username='fulfillment', department='Fulfillment', password='456'),
        User(username='admin', department='IT', password='000'),
        User(username='manager', department='Sales', password='999'),
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Mock users inserted successfully!")
