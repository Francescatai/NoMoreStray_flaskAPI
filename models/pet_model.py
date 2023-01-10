from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class PetModel(db.Model, SerializerMixin):
    __tablename__ = "pet_adopt_list"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_name = db.Column(db.String(50))
    pet_category = db.Column(db.String(5))
    pet_sex = db.Column(db.String(5))
    pet_variety = db.Column(db.String(10))
    pet_date = db.Column(db.String(10))
    pet_age = db.Column(db.String(10))
    pet_location = db.Column(db.String(100))
    pet_coat = db.Column(db.String(20))
    pet_build = db.Column(db.String(5))
    pet_TNR = db.Column(db.String(5))
    pet_health = db.Column(db.String(5))
    pet_url = db.Column(db.String(500))
    pet_picture = db.Column(db.String(500))
    pet_join_time = db.Column(db.DateTime, default=datetime.now)


class ApplyModel(db.Model, SerializerMixin):
    __tablename__ = "pet_apply_list"
    apply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), nullable=False)
    pet_id = db.Column(db.String(100), nullable=False)
    check_owner = db.Column(db.String(100), default=False)
    owner = db.Column(db.String(100))
    applicant_last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    applicant_first_name = db.Column(db.String(100), nullable=False)
    ID_number = db.Column(db.String(100), nullable=False)
    birth = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    contact_time = db.Column(db.String(100), nullable=False)
    second_contact_name = db.Column(db.String(100), nullable=False)
    second_contact_phone = db.Column(db.String(100), nullable=False)
    second_contact_email = db.Column(db.String(100), nullable=False)
    relation = db.Column(db.String(100), nullable=False)
    marriage = db.Column(db.String(100), default=False)
    family_members = db.Column(db.String(100), nullable=False)
    underage = db.Column(db.String(100), nullable=False)
    check_allergy = db.Column(db.String(100), nullable=False)
    family_income = db.Column(db.String(100), nullable=False)
    check_rent = db.Column(db.String(100), default=False)
    sqft = db.Column(db.String(100), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)
    is_apply = db.Column(db.String(10), default="已申請")


class CityModel(db.Model,SerializerMixin):
    __tablename__ = "city"
    serialize_only = ("city", )
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(200), nullable=False)


class VarietyModel(db.Model,SerializerMixin):
    __tablename__ = "pet_variety"
    serialize_only = ("variety",)
    variety_id = db.Column(db.Integer, primary_key=True)
    variety = db.Column(db.String(1000), nullable=False)