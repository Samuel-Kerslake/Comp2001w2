from flask import Flask, request, jsonify
from Comp2001_web_project import db
from Comp2001_web_project import app
from sqlalchemy import text
from Authentication import token_required, role_required

@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        query = text("EXEC [CW2].[GetUserByID] @UserID = :UserID")
        result = db.session.execute(query, {'UserID': user_id})
        users = [dict(row._mapping) for row in result.fetchall()]
        
        if not users:
            return jsonify({"message": "User not found"}), 404
        
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch user", "error": str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not all(key in data for key in ['UserID', 'Username', 'Email', 'Password', 'UserRole']):
            return jsonify({"message": "All user fields are required"}), 400

        query = text("""
            EXEC [CW2].[AddUser] 
            @UserID = :UserID, @Username = :Username, @Email = :Email, @Password = :Password, @UserRole = :UserRole
        """)
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC [CW2].[UpdateUser] 
            @UserID = :UserID, @Username = :Username, @Email = :Email, @Password = :Password, @UserRole = :UserRole
        """)
        db.session.execute(query, {'UserID': user_id, **data})
        db.session.commit()
        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant update user", "error": str(e)}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    try:
        query = text("EXEC [CW2].[DeleteUser] @UserID = :UserID")
        db.session.execute(query, {'UserID': user_id})
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant delete user", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['GET'])
def get_trail_by_id(trail_id):
    try:
        query = text("EXEC [CW2].[GetTrailByID] @TrailID = :TrailID")
        result = db.session.execute(query, {'TrailID': trail_id})
        trails = [dict(row._mapping) for row in result.fetchall()]
        
        if not trails:
            return jsonify({"message": "Trail not found"}), 404
        
        return jsonify(trails), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch trail", "error": str(e)}), 500


@app.route('/trails', methods=['POST'])
@token_required
def create_trail():
    try:
        data = request.get_json()
        
        required_fields = [
            'TrailID', 'TrailName', 'TrailSummary', 'TrailDescription', 
            'Difficulty', 'Location', 'Distance', 'ElevationGain', 'RouteType', 
            'OwnedBy', 'Rating', 'EstimatedTime',
            'Pt1_Desc', 'Pt1_Lat', 'Pt1_Long',
            'Pt2_Desc', 'Pt2_Lat', 'Pt2_Long',
            'Pt3_Desc', 'Pt3_Lat', 'Pt3_Long',
            'Pt4_Desc', 'Pt4_Lat', 'Pt4_Long',
            'Pt5_Desc', 'Pt5_Lat', 'Pt5_Long'
        ]

        if not all(key in data for key in required_fields):
            return jsonify({"message": "All trail and coordinate fields are required"}), 400

        data['UserID'] = data['OwnerID'] 

        query = text("""
            EXEC [CW2].[AddTrail] 
            @TrailID = :TrailID, @TrailName = :TrailName, @TrailSummary = :TrailSummary,
            @TrailDescription = :TrailDescription, @Difficulty = :Difficulty, 
            @Location = :Location, @Distance = :Distance, @ElevationGain = :ElevationGain, 
            @RouteType = :RouteType, @OwnerID = :OwnerID, @Rating = :Rating, 
            @EstimatedTime = :EstimatedTime,
            @Pt1_Desc = :Pt1_Desc, @Pt1_Lat = :Pt1_Lat, @Pt1_Long = :Pt1_Long,
            @Pt2_Desc = :Pt2_Desc, @Pt2_Lat = :Pt2_Lat, @Pt2_Long = :Pt2_Long,
            @Pt3_Desc = :Pt3_Desc, @Pt3_Lat = :Pt3_Lat, @Pt3_Long = :Pt3_Long,
            @Pt4_Desc = :Pt4_Desc, @Pt4_Lat = :Pt4_Lat, @Pt4_Long = :Pt4_Long,
            @Pt5_Desc = :Pt5_Desc, @Pt5_Lat = :Pt5_Lat, @Pt5_Long = :Pt5_Long
        """)

        db.session.execute(query, data)
        db.session.commit()

        return jsonify({"message": "Trail created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['PUT'])
@token_required
def update_trail(trail_id):
    try:
        data = request.get_json()
        
        required_fields = [
            'TrailName', 'TrailSummary', 'TrailDescription', 
            'Difficulty', 'Location', 'Distance', 'ElevationGain', 'RouteType', 
            'OwnerID', 'Rating', 'EstimatedTime',
            'Pt1_Desc', 'Pt1_Lat', 'Pt1_Long',
            'Pt2_Desc', 'Pt2_Lat', 'Pt2_Long',
            'Pt3_Desc', 'Pt3_Lat', 'Pt3_Long',
            'Pt4_Desc', 'Pt4_Lat', 'Pt4_Long',
            'Pt5_Desc', 'Pt5_Lat', 'Pt5_Long'
        ]

        if not all(key in data for key in required_fields):
            return jsonify({"message": "All trail and coordinate fields are required"}), 400

        data['UserID'] = data['OwnerID'] 

        query = text("""
            EXEC [CW2].[UpdateTrail] 
            @TrailID = :TrailID, @TrailName = :TrailName, @TrailSummary = :TrailSummary,
            @TrailDescription = :TrailDescription, @Difficulty = :Difficulty, 
            @Location = :Location, @Distance = :Distance, @ElevationGain = :ElevationGain, 
            @RouteType = :RouteType, @OwnerID = :OwnerID, @Rating = :Rating, 
            @EstimatedTime = :EstimatedTime,
            @Pt1_Desc = :Pt1_Desc, @Pt1_Lat = :Pt1_Lat, @Pt1_Long = :Pt1_Long,
            @Pt2_Desc = :Pt2_Desc, @Pt2_Lat = :Pt2_Lat, @Pt2_Long = :Pt2_Long,
            @Pt3_Desc = :Pt3_Desc, @Pt3_Lat = :Pt3_Lat, @Pt3_Long = :Pt3_Long,
            @Pt4_Desc = :Pt4_Desc, @Pt4_Lat = :Pt4_Lat, @Pt4_Long = :Pt4_Long,
            @Pt5_Desc = :Pt5_Desc, @Pt5_Lat = :Pt5_Lat, @Pt5_Long = :Pt5_Long
        """)

        db.session.execute(query, {'TrailID': trail_id, **data})
        db.session.commit()

        return jsonify({"message": "Trail updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cannot update trail", "error": str(e)}), 500


@app.route('/trails/<trail_id>', methods=['DELETE'])
@token_required
def delete_trail(trail_id):
    try:
        query = text("EXEC [CW2].[DeleteTrail] @TrailID = :TrailID")
        db.session.execute(query, {'TrailID': trail_id})
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant delete trail", "error": str(e)}), 500


@app.route('/features/<feature_id>', methods=['GET'])
def get_feature_by_id(feature_id):
    try:
        query = text("EXEC [CW2].[GetFeature] @TrailFeatureID = :TrailFeatureID")
        result = db.session.execute(query, {'TrailFeatureID': feature_id})
        features = [dict(row._mapping) for row in result.fetchall()]
        
        if not features:
            return jsonify({"message": "Feature not found"}), 404
        
        return jsonify(features), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch feature", "error": str(e)}), 500

@app.route('/features', methods=['POST'])
@token_required
def create_feature():
    try:
        data = request.get_json()
        if not 'TrailFeature' in data:
            return jsonify({"message": "TrailFeature field is required"}), 400

        query = text("""
            EXEC [CW2].[AddFeature] 
            @TrailFeature = :TrailFeature
        """)
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"message": "Feature created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": "Cant create feature", "error": str(e)}), 500

@app.route('/features/<feature_id>', methods=['DELETE'])
@token_required
def delete_feature(feature_id):
    try:
        query = text("EXEC [CW2].[DeleteFeature] @TrailFeatureID = :TrailFeatureID")
        db.session.execute(query, {'TrailFeatureID': feature_id})
        db.session.commit()
        return jsonify({"message": "Feature deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Cant delete feature", "error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        query = text("EXEC [CW2].[GetUsers]")
        result = db.session.execute(query)
        
        users = [dict(row._mapping) for row in result.fetchall()]

        if not users:
            return jsonify({"message": "No users found"}), 404

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch users", "error": str(e)}), 500


@app.route('/trails', methods=['GET'])
def get_all_trails():
    try:
        query = text("EXEC [CW2].[GetTrails]")
        result = db.session.execute(query)
        
        trails = [dict(row._mapping) for row in result.fetchall()]

        if not trails:
            return jsonify({"message": "No trails found"}), 404

        return jsonify(trails), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch trails", "error": str(e)}), 500


@app.route('/features', methods=['GET'])
def get_all_features():
    try:
        query = text("EXEC [CW2].[GetFeatures]")
        result = db.session.execute(query)
        
        features = [dict(row._mapping) for row in result.fetchall()]

        if not features:
            return jsonify({"message": "No features found"}), 404

        return jsonify(features), 200
    except Exception as e:
        return jsonify({"message": "Cant fetch features", "error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)