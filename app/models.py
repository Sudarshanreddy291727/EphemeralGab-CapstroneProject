from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    connection_id = db.Column(db.String(36), unique=True, nullable=False)  # New field

    def __repr__(self):
        return f"User('{self.username}')"
