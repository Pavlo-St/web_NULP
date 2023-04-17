import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

engine = create_engine("mysql+pymysql://root:qwerty@127.0.0.1:3306/world", echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    UserId = Column(Integer, primary_key=True)
    Username = Column(String(50), nullable=False)
    Name = Column(String(10), nullable=False)
    Surname = Column(String(15), nullable=False)
    Email = Column(String(50), nullable=False)
    Role = Column(String(30), nullable=False)
    Password = Column(String(120), nullable=False)
    Reservation = relationship("Reservation", overlaps="Reservation")


class Reservation(Base):
    __tablename__ = 'Reservations'
    ReservationId = Column(Integer, primary_key=True)
    BeginTime = Column(sqlalchemy.DATETIME, nullable=False)
    EndTime = Column(sqlalchemy.DATETIME, nullable=False)
    UserId = Column(Integer, ForeignKey("Users.UserId"))
    RoomId = Column(Integer, ForeignKey("Rooms.RoomId"))

    Room = relationship("Room", overlaps="Reservation")
    User = relationship("User", overlaps="Reservation")


class Room(Base):
    __tablename__ = "Rooms"
    RoomId = Column(Integer, primary_key=True)
    Size = Column(String(20), nullable=False)
    Reservation = relationship("Reservation", overlaps="Reservation")

#Base.metadata.create_all(engine)
