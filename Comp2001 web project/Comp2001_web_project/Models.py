from Comp2001_web_project import db,app


class User(db.Model):
    __tablename__ = 'USERS'
    __table_args__ = {'schema': 'CW2'}

    UserID = db.Column(db.String(10), primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(20))
    UserRole = db.Column(db.String(10), nullable=False, default='User')
    
    trail_logs = db.relationship('TrailCreationLog', backref='user', lazy=True)

class Trail(db.Model):
    __tablename__ = 'TRAIL'
    __table_args__ = {'schema': 'CW2'}


    TrailID = db.Column(db.String(10), primary_key=True)
    TrailName = db.Column(db.String(50), nullable=False)
    TrailSummary = db.Column(db.String(255))
    TrailDescription = db.Column(db.Text)
    Difficulty = db.Column(db.String(20))
    Location = db.Column(db.String(100))
    Distance = db.Column(db.Float)
    ElevationGain = db.Column(db.DECIMAL(10, 2))
    RouteType = db.Column(db.String(50))
    OwnedBy = db.Column(db.String(10), db.ForeignKey('User.UserID'))
    Rating = db.Column(db.Float)
    EstimatedTime = db.Column(db.String(10))
    Pt1_Lat = db.Column(db.DECIMAL(10, 6))
    Pt1_Long = db.Column(db.DECIMAL(10, 6))
    Pt1_Desc = db.Column(db.String(255))
    Pt2_Lat = db.Column(db.DECIMAL(10, 6))
    Pt2_Long = db.Column(db.DECIMAL(10, 6))
    Pt2_Desc = db.Column(db.String(255))
    Pt3_Lat = db.Column(db.DECIMAL(10, 6))
    Pt3_Long = db.Column(db.DECIMAL(10, 6))
    Pt3_Desc = db.Column(db.String(255))
    Pt4_Lat = db.Column(db.DECIMAL(10, 6))
    Pt4_Long = db.Column(db.DECIMAL(10, 6))
    Pt4_Desc = db.Column(db.String(255))
    Pt5_Lat = db.Column(db.DECIMAL(10, 6))
    Pt5_Long = db.Column(db.DECIMAL(10, 6))
    Pt5_Desc = db.Column(db.String(255))
    
    features = db.relationship('TrailFeature', backref='trail', lazy=True)

class Feature(db.Model):
    __tablename__ = 'FEATURE'
    __table_args__ = {'schema': 'CW2'}

    TrailFeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailFeature = db.Column(db.String(255), nullable=False)
    
class TrailFeature(db.Model):
    __tablename__ = 'TRAIL_FREATURE'
    __table_args__ = {'schema': 'CW2'}

    TrailID = db.Column(db.String(10), db.ForeignKey('Trail.TrailID'), primary_key=True)
    TrailFeatureID = db.Column(db.Integer, db.ForeignKey('Feature.TrailFeatureID'), primary_key=True)
    

with app.app_context():
    print("Registered Tables in SQLAlchemy:")
    print(db.metadata.tables.keys())