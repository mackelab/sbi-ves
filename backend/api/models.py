import uuid
from hmac import compare_digest
from typing import Optional

from . import db
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, Field


# ***** USER MANAGEMENT ***********************************************
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(32), primary_key=True, default=lambda: str(uuid4()))
    firstName = db.Column('first_name', db.String(255), nullable=False, key='firstName')
    lastName = db.Column('last_name', db.String(255), nullable=False, key='lastName')
    institution = db.Column(db.String(255))
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    measurements = db.relationship('Measurement', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)
    createdAt = db.Column('created_at', db.DateTime, default=datetime.utcnow(), key='createdAt')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, firstName={self.firstName})>"

    def to_dict(self):
        print("self", self)
        return {c.key: getattr(self, c.key) if not isinstance(getattr(self, c.key), uuid.UUID) else str(
            getattr(self, c.key)) for c in self.__table__.columns}

    def to_dto(self):
        return UserDTO(self.id, self.firstName, self.lastName, self.institution, self.username, self.email)

    def check_password(self, password):
        return compare_digest(password, self.password)


class UserDTO(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    institution: str
    username: str
    email: str

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

    def to_user(self):
        return User(id=self.id, firstName=self.firstName, lastName=self.lastName, institution=self.institution,
                    username=self.username, password=self.password, email=self.email, created_at=self.created_at)


# ***** REGISTRATION **************************************************

class RegisterUserDTO(BaseModel):
    id: UUID | None
    firstName: str
    lastName: str
    institution: str
    username: str
    email: str
    password: str
    confirmPassword: str

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

    def to_user(self):
        return User(id=self.id, firstName=self.firstName, lastName=self.lastName, institution=self.institution,
                    username=self.username, password=self.password, email=self.email)


# ***** MEASUREMENT MANAGEMENT ****************************************

class Measurement(db.Model):
    __tablename__ = 'measurement'

    id = db.Column(db.String(32), primary_key=True, default=lambda: str(uuid4()))
    userId = db.Column('user_id', db.String(32), db.ForeignKey('user.id'), nullable=False, key='userId')
    fileId = db.Column('file_id', db.String(32), db.ForeignKey('file.id'), nullable=False, key='fileId')
    ab2_2 = db.Column(db.Float, nullable=True)
    ab2_2_5 = db.Column(db.Float, nullable=True)
    ab2_3 = db.Column(db.Float, nullable=True)
    ab2_3_6 = db.Column(db.Float, nullable=True)
    ab2_4_4 = db.Column(db.Float, nullable=True)
    ab2_5_2 = db.Column(db.Float, nullable=True)
    ab2_6_3 = db.Column(db.Float, nullable=True)
    ab2_7_5 = db.Column(db.Float, nullable=True)
    ab2_8_7 = db.Column(db.Float, nullable=True)
    ab2_10 = db.Column(db.Float, nullable=True)
    ab2_12 = db.Column(db.Float, nullable=True)
    ab2_14_5 = db.Column(db.Float, nullable=True)
    ab2_17_5 = db.Column(db.Float, nullable=True)
    ab2_21 = db.Column(db.Float, nullable=True)
    ab2_25 = db.Column(db.Float, nullable=True)
    ab2_30 = db.Column(db.Float, nullable=True)
    ab2_36 = db.Column(db.Float, nullable=True)
    ab2_44 = db.Column(db.Float, nullable=True)
    ab2_52 = db.Column(db.Float, nullable=True)
    ab2_63 = db.Column(db.Float, nullable=True)
    ab2_75 = db.Column(db.Float, nullable=True)
    ab2_87 = db.Column(db.Float, nullable=True)
    ab2_100 = db.Column(db.Float, nullable=True)
    location = db.Column('location', db.String(255), nullable=True)
    comment = db.Column('comment', db.String(255), nullable=True)
    measurementDate = db.Column('measurement_date', db.DateTime, nullable=True)
    createdAt = db.Column('created_at', db.DateTime, default=datetime.utcnow(), key='createdAt')

    def __repr__(self):
        return f"<Measurement(id={self.id}, userId={self.userId}, measurement_location={self.location})>"

    def to_dict(self):
        return {c.key: (getattr(self, c.key) if getattr(self, c.key) is not None else None)
        if not isinstance(
            getattr(self, c.key), uuid.UUID)
        else str(
            getattr(self, c.key))
                for c in self.__table__.columns}

    '''
    def to_dict(self):
        return {c.key: getattr(self, c.key) if not isinstance(getattr(self, c.key), uuid.UUID) else str(
            getattr(self, c.key)) for c in self.__table__.columns}

    '''

    def to_dto(self):
        return MeasurementDTO(self.id, self.userId, self.location, self.comment, self.measurementDate)


class MeasurementDTO(BaseModel):
    id: UUID
    userId: UUID
    location: Optional[str] = None
    comment: Optional[str] = None
    measurementDate: Optional[datetime] = None
    createdAt: datetime

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

    def to_measurement(self):
        return Measurement(id=self.id, userId=self.userId, location=self.location, comment=self.comment,
                           measurementDate=self.measurementDate)


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.String(32), primary_key=True, default=lambda: str(uuid4()))
    userId = db.Column('user_id', db.String(32), db.ForeignKey('user.id'), nullable=False, key='userId')
    fileName = db.Column('file_name', db.String(255), nullable=False)
    fileExtension = db.Column('file_extension', db.String(255), nullable=False)
    fileSize = db.Column('file_size', db.Integer, nullable=True)

    def __repr__(self):
        return f"<File(id={self.id}, userId={self.userId}, fileName={self.fileName})>"

    def to_dict(self):
        return {c.key: getattr(self, c.key) if not isinstance(getattr(self, c.key), uuid.UUID) else str(
            getattr(self, c.key)) for c in self.__table__.columns}
