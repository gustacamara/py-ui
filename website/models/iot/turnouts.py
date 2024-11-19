from models.db import db

class Turnout(db.Model):
    __tablename__ = 'turnouts'
    id = db.Column('id', db.Integer, primary_key=True)
    left_angle = db.Column(db.Integer)
    right_angle = db.Column(db.Integer)

    def save_turnout(id, left_angle, right_angle):
        turnout = Turnout(id=id, left_angle=left_angle, right_angle=right_angle)
        db.session.add(turnout)
        db.session.commit()

    def get_turnouts():
        turnouts = Turnout.query.all()
        return turnouts

    def get_single_turnout(id):
        turnout = Turnout.query.filter(Turnout.id == id).first()
        return turnout

    def update_turnout(id, left_angle, right_angle):
        turnout = Turnout.query.filter(Turnout.id == id).first()
        if turnout is not None:
            turnout.left_angle = left_angle
            turnout.right_angle = right_angle
            db.session.commit()
            return Turnout.get_turnouts()

    def delete_turnout(id):
        turnout = Turnout.query.filter(Turnout.id == id).first()
        if turnout is not None:
            db.session.delete(turnout)
            db.session.commit()
        return Turnout.get_turnouts()
