from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():

    if User.query.filter_by(username="admin").first():

        print("Admin already exists.")

    else:

        admin = User(
            full_name="Administrator",
            username="admin",
            email="admin@ngo.org",
            role="Admin"
        )

        admin.set_password("Admin@123")

        db.session.add(admin)

        db.session.commit()

        print("Admin user created.")