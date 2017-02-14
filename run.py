import os

from travel_planner.main import app, api, db
from travel_planner.api import UsersView, UserView, TripsView, TripView, TripsFilterView
from travel_planner.views import *


api.add_resource(UsersView, '/users')
api.add_resource(UserView, '/users/<username>')
api.add_resource(TripsView, '/users/<username>/trips')
api.add_resource(TripView, '/users/<username>/trips/<int:trip_id>')
api.add_resource(TripsFilterView, '/users/<username>/trips/<from_date>&<to_date>')

db.create_all()

app.run(port=5000, debug=True)