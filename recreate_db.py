import os
from app import db
from app.models import User

if os.path.exists('app.db'):
    os.remove('app.db')

db.create_all()
u = User(login='pinky')
u.set_password('bearofbeer2003')
db.session.add(u)
db.session.commit()
