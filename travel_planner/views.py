import json
from datetime import datetime, timedelta

from flask import render_template, send_file, Response

from main import app
from models import Trip


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/travel-plan')
def get_travel_plan():
    date = datetime.utcnow()
    date_in_month = date + timedelta(days=30)

    trips = [dict(trip) for trip in Trip.query.filter(Trip.start_date >= date, Trip.start_date <= date_in_month).all()]

    return Response(json.dumps(trips), mimetype="application/json", 
                        headers={'Content-Disposition':'attachment;filename=trip-plan.json'})
