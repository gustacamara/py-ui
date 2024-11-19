from models.db import db

class SensorHistory(db.Model):
    __tablename__ = 'sensors_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Text)
    datetime = db.Column(db.Text)
    sensor_id = db.Column(db.Integer)
    actuator_id = db.Column(db.Integer)
    registry_type = db.Column(db.Text)
    description = db.Column(db.Text)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all():
        return SensorHistory.query.all()

    def get_by_id(id):
        return SensorHistory.query.filter(SensorHistory.id == id).first()

    def update(self, value, datetime, sensor_id, actuator_id, registry_type, description):
        self.value = value
        self.datetime = datetime
        self.sensor_id = sensor_id
        self.actuator_id = actuator_id
        self.registry_type = registry_type
        self.description = description
        db.session.commit()

    def delete_by_id(id):
        sensor_history = SensorHistory.query.filter(SensorHistory.id == id).first()
        if sensor_history is not None:
            db.session.delete(sensor_history)
            db.session.commit()