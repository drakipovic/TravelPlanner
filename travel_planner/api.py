from datetime import datetime

from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity
from flask import jsonify, request

from main import app
from models import User, Trip


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


jwt = JWT(app, authenticate, identity)


class UsersView(Resource):

    @jwt_required()
    def get(self):
        users = [dict(user) for user in User.query.all()]

        return jsonify({"users": users})

    def post(self):
        data = request.get_json()

        if User.query.filter_by(username=data["username"]).count() > 0:
            return jsonify({"error": "Username taken."})
        
        user = User(data["username"], data["password"], data.get("role", 'user'))
        user.save()
    
        return jsonify({"success": True})


class UserView(Resource):

    @jwt_required()
    def put(self, username):
        user = current_identity

        if user.username != username and user.role == 'user':
            return jsonify({"error": "You don't have permission to edit other users entries."})

        data = request.get_json()

        user.username = data["username"]
        user.role = data.get("role", 'user')
        user.save()

        return jsonify({"user": dict(user)})
    
    @jwt_required()
    def delete(self, username):
        user = current_identity

        if user.username != username and user.role == 'user':
            return jsonify({"error": "You don't have permission to edit other users entries."})
        
        user.delete()

        return jsonify({"success": True})
       
        
class TripView(Resource):

    @jwt_required()
    def put(self, username, trip_id):
        user = current_identity

        if user.username != username and user.role != 'admin':
            return jsonify({"error": "You don't have permission to edit other users entries."})

        data = request.get_json()

        trip = Trip.query.get(trip_id)

        trip.destination = data["destination"]
        trip.start_date = datetime.strptime(data["startDate"], "%m/%d/%Y")
        trip.end_date = datetime.strptime(data["endDate"], "%m/%d/%Y")
        trip.comment = data["comment"]
        trip.save()

        return jsonify({"trip": dict(trip)})

    @jwt_required()
    def delete(self, username, trip_id):
        user = current_identity

        if user.username != username and user.role != 'admin':
            return jsonify({"error": "You don't have permission to edit other users entries."})

        trip = Trip.query.get(trip_id)
        trip.delete()

        return jsonify({"success": True})


class TripsView(Resource):

    @jwt_required()
    def get(self, username):
        user = User.query.filter_by(username=username).first()

        trips = [dict(trip) for trip in Trip.query.filter_by(user_id=user.id).all()]

        return jsonify({'trips': trips})

    @jwt_required()
    def post(self, username):
        user = current_identity

        if user.username != username and user.role != 'admin':
            return jsonify({"error": "You don't have permission to edit other users entries."})

        data = request.get_json()
        
        trip = Trip(destination=data["destination"], comment=data["comment"],
                    start_date=datetime.strptime(data["startDate"], "%m/%d/%Y"),
                    end_date=datetime.strptime(data["endDate"], "%m/%d/%Y"),
                    user_id=user.id)
        
        trip.save()

        return jsonify({"success": True})


class TripsFilterView(Resource):

    @jwt_required()
    def get(self, username, from_date, to_date):

        start_date = datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.strptime(to_date, "%Y-%m-%d")

        user = User.query.filter_by(username=username).first()

        trips = [dict(trip) for trip in Trip.query.filter(user.id == Trip.user_id, 
                                                                Trip.start_date > start_date,
                                                                Trip.end_date < end_date)]
        
        return jsonify({"trips": trips})