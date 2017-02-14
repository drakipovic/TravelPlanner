from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from main import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(1000))
    role = db.Column(db.String(50))

    trips = db.relationship('Trip', backref='user', lazy='dynamic')

    def __init__(self, username, password, role='user'):
        self.username = username
        self.password_hash = self._set_password(password)
        self.role = role

    def __iter__(self):
        yield 'id', str(self.id)
        yield 'username', self.username

    def _set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Trip(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(1000))
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __iter__(self):
        yield 'tripId', self.trip_id
        yield 'startDate', datetime.strftime(self.start_date, "%m/%d/%Y")
        yield 'endDate', datetime.strftime(self.end_date, "%m/%d/%Y")
        yield 'destination', self.destination
        yield 'comment', self.comment
        delta = self.start_date - datetime.utcnow()
        yield 'daysToTrip', delta.days+1 if delta.days >= 0 else 'Been'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()