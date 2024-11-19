from models.db import db

class Cab(db.Model):
    __tablename__ = 'cabs'
    id = db.Column('id', db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cab.query.all()

    @staticmethod
    def get_by_id(id):
        return Cab.query.filter(Cab.id == id).first()

    def update(self, model, manufacturer):
        self.model = model
        self.manufacturer = manufacturer
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        cab = Cab.query.filter(Cab.id == id).first()
        if cab is not None:
            db.session.delete(cab)
            db.session.commit()
