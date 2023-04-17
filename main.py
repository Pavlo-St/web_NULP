from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, and_
from flask import Flask, request, jsonify, json, make_response
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import flask_swagger_ui, get_swaggerui_blueprint
from flask_httpauth import HTTPBasicAuth
from TablesSQL import User, Reservation, Room
# from flask_restful import Api, Resource
import bcrypt as bcrypt

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "GET", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}})




#app = Flask(__name__)
auth = HTTPBasicAuth()

# SQLalchemy
engine = create_engine("mysql+pymysql://root:qwerty@127.0.0.1:3306/world", echo=True)
session = sessionmaker(bind=engine)
s = session()

# Marshmallow
ma = Marshmallow(app)

# SwaggerUrL
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL,
                                            config={'app_name': 'Room Booking API'})
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


from flask_cors import CORS


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    header['Access-Control-Allow-Headers'] = 'content-type'
    return response




# ERROR STATUSES
@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(403)
def handle_403_error(_error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)


@auth.verify_password
def verify_password(username, password):
    try:
        user = s.query(User).filter(User.Username == username).one()
        if not user:
            return make_response(404)
        if bcrypt.checkpw(password.encode("utf-8"), user.Password.encode("utf-8")):
            return user
        else:
            return make_response(401)
    except:
        return None


@auth.get_user_roles
def get_user_roles(user):
    return user.Role


# SCHEMAS
class UserSchema(ma.Schema):
    class Meta:
        fields = ('Username', 'Name', 'Surname', 'Email')


user_schema = UserSchema(many=False)
users_schema = UserSchema(many=True)


class ReservationSchema(ma.Schema):
    class Meta:
        fields = ('BeginTime', 'EndTime', 'UserId', 'RoomId')


reseration_schema = ReservationSchema(many=False)
reserations_schema = ReservationSchema(many=True)


class RoomSchema(ma.Schema):
    class Meta:
        fields = ('RoomId', 'Size')


rooms_schema = RoomSchema(many=True)


# USER METHODS


@app.route("/user/register", methods=["POST"])
def createUser():
    try:
        # UserId = request.json['UserId']
        Username = request.json['Username']
        Name = request.json['Name']
        Surname = request.json['Surname']
        Email = request.json['Email']
        Password = request.json['Password']
        Password = bcrypt.hashpw(Password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        Role = "User"
        # bcrypt.generate_password_hash
        new_user = User(Username=Username,
                        Name=Name, Surname=Surname,
                        Email=Email, Password=Password, Role=Role)
        s.add(new_user)
        s.commit()
        return user_schema.jsonify(new_user)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


@app.route("/user/<int:userId>", methods=["GET"])
@auth.login_required(role='Admin')
def getUserById(userId):
    user = s.query(User).filter(User.UserId == userId).one()
    return user_schema.jsonify(user)


@app.route("/user/<int:userId>", methods=["DELETE"])
@auth.login_required
def deleteUserById(userId):
    currentUser = auth.current_user()
    user = s.query(User).filter(User.UserId == userId).one()
    if (currentUser.Role != "Admin" or (
            currentUser.Role == "Admin" and user.Role == "Admin")) and userId != currentUser.UserId:
        return handle_403_error(1)
    s.delete(user)
    s.commit()
    return user_schema.jsonify(user)


# RESERVATION METHODS
@app.route("/reservation/create", methods=["POST"])
@auth.login_required
def createReservation():
    try:
        currentUser = auth.current_user()
        ReservationId = request.json['ReservationId']
        BeginTime = request.json['BeginTime']
        EndTime = request.json['EndTime']
        RoomId = request.json['RoomId']

        new_reservation = Reservation(ReservationId=ReservationId,
                                      BeginTime=datetime.strptime(BeginTime, "%Y-%m-%d %H:%M"),
                                      EndTime=datetime.strptime(EndTime, "%Y-%m-%d %H:%M"),
                                      UserId=currentUser.UserId,
                                      RoomId=RoomId)

        exists = s.query(Reservation).filter(
            and_(Reservation.BeginTime >= datetime.strptime(BeginTime, "%Y-%m-%d %H:%M")
                 , Reservation.BeginTime <= datetime.strptime(EndTime, "%Y-%m-%d %H:%M")
                 , Reservation.EndTime <= datetime.strptime(EndTime, "%Y-%m-%d %H:%M")
                 , Reservation.RoomId == RoomId)).first() is not None

        dif = datetime.strptime(EndTime, "%Y-%m-%d %H:%M") - datetime.strptime(BeginTime, "%Y-%m-%d %H:%M")

        if dif.days > 5:
            return jsonify({"Error": "Too much time"})

        if dif.seconds < 3600:
            return jsonify({"Error": "Too less time"})

        if exists:
            return jsonify({"Error": "Room is already booked"})

        if datetime.strptime(BeginTime, "%Y-%m-%d %H:%M") >= datetime.strptime(EndTime, "%Y-%m-%d %H:%M"):
            return jsonify({"Error": "Invalid date input"})

        s.add(new_reservation)
        s.commit()
        return reseration_schema.jsonify(new_reservation)
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


@app.route("/reservation/rooms/<int:reservationId>", methods=["DELETE"])
@auth.login_required
def deleteReservationById(reservationId):
    user = auth.current_user()
    reservation = s.query(Reservation).filter(Reservation.ReservationId == reservationId).one()
    if user.Role != "Admin" and reservation.UserId != user.UserId:
        return handle_403_error()
    s.delete(reservation)
    s.commit()
    return jsonify({"Success": "Reservation deleted."})


@app.route("/reservation/rooms/<int:reservationId>", methods=["PUT"])
@auth.login_required
def updateReservationById(reservationId):
    user = auth.current_user()
    reservation = s.query(Reservation).filter(Reservation.ReservationId == reservationId).one()
    if user.Role != "Admin" and reservation.UserId != user.UserId:
        return handle_403_error()
    try:
        BeginTime = request.json['BeginTime']
        EndTime = request.json['EndTime']
        UserId = request.json['UserId']
        RoomId = request.json['RoomId']

        reservation.BeginTime = BeginTime
        reservation.EndTime = EndTime
        reservation.UserId = UserId
        reservation.RoomId = RoomId

        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})

    return reseration_schema.jsonify(reservation)


@app.route("/reservation/rooms", methods=["GET"])
def GetALLRooms():
    rooms = s.query(Room).all()
    result_set = rooms_schema.dump(rooms)
    return jsonify(result_set)


@app.route("/reservation/get/<string:beginTime>/<string:endTime>/<int:roomId>", methods=["GET"])
def GetAvailableRoomOne(beginTime, endTime, roomId):
    try:
        exists = s.query(Reservation).filter(
            and_(Reservation.BeginTime == datetime.strptime(beginTime, "%Y-%m-%d %H:%M")
                 , Reservation.EndTime == datetime.strptime(endTime, "%Y-%m-%d %H:%M")
                 , Reservation.RoomId == roomId)).first() is not None
        if exists:
            return jsonify({"State": "Reserved"})
        else:
            return jsonify({"State": "Available"})
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})


if __name__ == "__main__":
    app.run()
