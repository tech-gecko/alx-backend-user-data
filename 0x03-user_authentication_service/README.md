# User Authentication Service
This directory contains tasks on user authentication for a Flask application. It uses SQLAlchemy ORM for the DB.

# Interaction Flow
app.py interacts with auth.py, which in turn interacts with db.py, which in turn interacts with user.py

# Data
This API expects data to be sent in forms. In a real life example, most data would be sent as JSON. If you want your API to accept both formats, that can also be done. Below is how data as JSON would be retrieved in your routes and sent in your integration test, respectively:

## Route
from Flask import request
field = request.get_json().get('field_key_name')

## Integration Test
import requests
response = requests.method('url', json={...})
assert response.json() == {...}