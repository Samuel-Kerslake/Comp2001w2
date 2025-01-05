from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from functools import wraps
import requests
import jwt
import datetime
from COMP2001w2 import app, views
from Authentication import token_required, role_required, SECRET_KEY

# Initialize the Flask-RESTX API
api = Api(
    app,
    version='1.0',
    title='COMP2001 Microservice Samuel Kerslake',
    description='API for managing users, trails, and features.',
    doc='/swagger', 
    security='BearerAuth'
)

# Define the security scheme for the API
api.authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

# Define namespaces for better organization
users_ns = api.namespace('users', description='User  operations')
trails_ns = api.namespace('trails', description='Trail operations')
features_ns = api.namespace('features', description='Feature operations')
views_ns = api.namespace('views', description='View operations')
auth_ns = api.namespace('auth', description='Authentication operations')

# Define models for request and response validation
user_model = api.model('USERS ', {
    'User ID': fields.String(required=True, description='The user ID'),
    'Username': fields.String(required=True, description='The user\'s name'),
    'Email': fields.String(required=True, description='The user\'s email address'),
    'Password': fields.String(required=True, description='The user\'s password'),
    'User Role': fields.String(required=True, description='The role of the user'),
})

trail_model = api.model('TRAIL', {
    'TrailID': fields.String(required=True, description='The trail\'s ID'),
    'TrailName': fields.String(required=True, description='The name of the trail'),
    'TrailSummary': fields.String(required=True, description='A summary of the trail'),
    'TrailDescription': fields.String(required=True, description='A description of the trail'),
    'Difficulty': fields.String(required=True, description='The trail\'s difficulty'),
    'Location': fields.String(required=True, description='The location of the trail'),
    'Distance': fields.Float(required=True, description='The distance of the trail in kilometers'),
    'ElevationGain': fields.Float(required=True, description='The elevation gain of the trail in meters'),
    'RouteType': fields.String(required=True, description='The type of route'),
    'OwnedBy': fields.String(required=True, description='The user ID of the trail owner'),
    'Rating': fields.Float(required=True, description='The rating of the trail'),
    'EstimatedTime': fields.String(required=True, description='The estimated time to complete the trail'),
    'Pt1_Desc': fields.String(required=True, description='Description of Point 1'),
    'Pt1_Lat': fields.Float(required=True, description='Latitude of Point 1'),
    'Pt1_Long': fields.Float(required=True, description='Longitude of Point 1'),
    'Pt2_Desc': fields.String(required=True, description='Description of Point 2'),
    'Pt2_Lat': fields.Float(required=True, description='Latitude of Point 2'),
    'Pt2_Long': fields.Float(required=True, description='Longitude of Point 2'),
    'Pt3_Desc': fields.String(required=True, description='Description of Point 3'),
    'Pt3_Lat': fields.Float(required=True, description='Latitude of Point 3'),
    'Pt3_Long': fields.Float(required=True, description='Longitude of Point 3'),
    'Pt4_Desc': fields.String(required=True, description='Description of Point 4'),
    'Pt4_Lat': fields.Float(required=True, description='Latitude of Point 4'),
    'Pt4_Long': fields.Float(required=True, description='Longitude of Point 4'),
    'Pt5_Desc': fields.String(required=True, description='Description of Point 5'),
    'Pt5_Lat': fields.Float(required=True, description='Latitude of Point 5'),
    'Pt5_Long': fields.Float(required=True, description='Longitude of Point 5'),
})

feature_model = api.model('FEATURE', {
    'TrailFeatureID': fields.String(required=True, description='The feature ID'),
    'TrailFeature': fields.String(required=True, description='The name of the feature'),
})

login_model = api.model('Login', {
    'email': fields.String(required =True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('user_login')
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user with the Auth API and issue a token for API endpoints"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email and password are required'}, 400

        try:
            response = requests.post(
                AUTH_API_URL,
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                try:
                    auth_response = response.json()
                    if isinstance(auth_response, list) and len(auth_response) >= 2 and auth_response[0] == "Verified":
                        verified_status = auth_response[1]
                        token = jwt.encode(
                            {
                                "email": email,
                                "role": "Admin" if verified_status == "True" else "User ",
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                            },
                            SECRET_KEY,
                            algorithm="HS256",
                        )

                        return {
                            "message": "Login successful",
                            "verified": verified_status == "True",
                            "token": token
                        }, 200

                    else:
                        return {"message": "Unexpected API response format", "response_content": auth_response}, 500

                except ValueError:
                    return {"message": "Invalid JSON response from Auth API"}, 500

            else:
                return {
                    "message": f"Authentication failed with status code {response.status_code}",
                    "response_text": response.text
                }, response.status_code

        except requests.RequestException as e:
            return {"message": f"Error connecting to Auth API: {str(e)}"}, 500


@users_ns.route('')
class Users(Resource):
    @users_ns.doc('get_all_users')
    def get(self):
        return views.get_all_users()

    @users_ns.expect(user_model)
    @users_ns.doc('create_user')
    def post(self):
        return views.create_user()


@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The user\'s ID')
class User(Resource):
    @users_ns.doc('get_user_by_id', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def get(self, user_id):
        return views.get_user_by_id(user_id)

    @users_ns.expect(user_model)
    @users_ns.doc('update_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, user_id):
        return views.update_user(user_id)

    @users_ns.doc('delete_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, user_id):
        return views.delete_user(user_id)


@trails_ns.route('')
class Trails(Resource):
    @trails_ns.doc('get_all_trails')
    def get(self):
        return views.get_all_trails()

    @trails_ns.expect(trail_model)
    @trails_ns.doc('create_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        return views.create_trail()


@trails_ns.route('/<string:trail_id>')
@trails_ns.param('trail_id', 'The trail ID')
class Trail(Resource):
    @trails_ns.doc('get_trail_by_id')
    def get(self, trail_id):
        return views.get_trail_by_id(trail_id)

    @trails_ns.expect(trail_model)
    @trails_ns.doc('update_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, trail_id):
        return views.update_trail(trail_id)

    @trails_ns.doc('delete_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, trail_id):
        return views.delete_trail(trail_id)


@features_ns.route('')
class Features(Resource):
    @features_ns.doc('get_all_features')
    def get(self):
        return views.get_all_features()

    @features_ns.expect(feature_model)
    @features_ns.doc('create_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        return views.create_feature()

@features_ns.route('/< string:feature_id>')
@features_ns.param('feature_id', 'The feature ID')
class Feature(Resource):
    @features_ns.doc('get_feature_by_id')
    def get(self, feature_id):
        return views.get_feature_by_id(feature_id)

    @features_ns.expect(feature_model)
    @features_ns.doc('update_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, feature_id):
        return views.update_feature(feature_id)

    @features_ns.doc('delete_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, feature_id):
        return views.delete_feature(feature_id)

@views_ns.route('')
class Views(Resource):
    @views_ns.doc('get_all_views')
    def get(self):
        return views.get_all_views()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)