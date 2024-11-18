from models.db import db

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column('id', db.Integer, primary_key=True)
    location = db.Column(db.String(255))
    sensor_type = db.Column(db.Integer)

    def save_sensor(id, location, sensor_type):
        sensor = Sensor(id=id, location=location, sensor_type=sensor_type)
        db.session.add(sensor)
        db.session.commit()

    def get_sensors():
        sensors = Sensor.query.all()
        return sensors

    def get_single_sensor(id):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        return sensor

    def update_sensor(id, location, sensor_type):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        if sensor is not None:
            sensor.location = location
            sensor.sensor_type = sensor_type
            db.session.commit()
            return Sensor.get_sensors()

    def delete_sensor(id):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        if sensor is not None:
            db.session.delete(sensor)
            db.session.commit()
        return Sensor.get_sensors()
