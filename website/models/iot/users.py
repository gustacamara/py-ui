from models.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all():
        return User.query.all()

    def get_by_id(id):
        return User.query.filter(User.id == id).first()

    def update(self, name, password):
        self.name = name
        self.password = password
        db.session.commit()

    def delete_by_id(id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
