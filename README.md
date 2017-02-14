# TravelPlanner
Simple travel planner app build with Flask and React


## Installation
    git clone https://github.com/drakipovic/TravelPlanner
    pip install -r requirements.txt
    npm install -g webpack
    npm install
    
## Start
    webpack --watch
    python run.py
    
## Tests
    pytest


## API Endpoints
    /api/token [POST]
    /api/users [POST, GET]
    /api/users/<username> [PUT, DELETE]
    /api/users/<username>/trips [POST, GET]
    /api/users/<username>/trips/<trip_id> [PUT, DELETE]
