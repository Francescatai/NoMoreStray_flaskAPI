from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid
from sqlalchemy_serializer import SerializerMixin
from exts import db


class Permission(object):
    ALL_PERMISSION = 0b11111111
    #  訪問者權限
    VISITOR = 0b00000001
    #  管理前台用户的權限
    USER = 0b00000010
    #  管理后台管理員權限
    STAFF = 0b00000100
    #  管理前台寵物權限
    PETS = 0b00001000


class RoleModel(db.Model, SerializerMixin):
    serialize_only = ("id", "name", "desc", "create_time")
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=Permission.VISITOR)


class UserModel(db.Model, SerializerMixin):
    # serialize_rules = ("-_password",)
    serialize_only = ("user_id", "email", "username", "join_time", "is_staff", "is_active")
    __tablename__ = "userinfo"
    user_id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    # 喜歡種類(貓/狗)
    prefer_pet_category = db.Column(db.String(10))
    # 喜歡寵物品種
    prefer_pet_variety = db.Column(db.String(250))
    prefer_pet_sex = db.Column(db.String(10))
    collect_pet_id = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    # 是否為黑名單(領養後未回報/異常行為):正常用戶:1/異常用戶:0
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

    role = db.relationship("RoleModel", backref="users")

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(UserModel, self).__init__(*args, **kwargs)

    # 把password定義成屬性
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)

    def has_permission(self, permission):
        # 當前用戶所擁有的權限&permission = permission
        # 0b011 & 0b001 = 0b001
        # 0b011 & 0b100 = 0b000
        return (self.role.permissions & permission) == permission


class DonateModel(db.Model, SerializerMixin):
    __tablename__ = "donate_list"
    serialize_only = (
        "donate_time", "donate_number", "donate_status", "donate_method", "donate_money", "point_time", "point_number",
        "point_history")
    donate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), nullable=False)
    donate_time = db.Column(db.DateTime, default=datetime.now)
    donate_number = db.Column(db.String(100), nullable=False)
    donate_status = db.Column(db.String(20), nullable=False)
    donate_method = db.Column(db.String(20), nullable=False)
    donate_money = db.Column(db.Integer, nullable=False)
    point_time = db.Column(db.DateTime, default=datetime.now)
    point_number = db.Column(db.Integer, nullable=False)
    point_history = db.Column(db.String(20), nullable=False)


class Recommend_List(db.Model, SerializerMixin):
    __tablename__ = "recommend"
    user_id = db.Column(db.String(100), nullable=False)
    recommend_pets = db.Column(db.String(10000), primary_key=True, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)


class SelectModel(db.Model, SerializerMixin):
    __tablename__ = "select_result"
    select_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), nullable=False)
    select_result = db.Column(db.String(10000), nullable=True)
    select_time = db.Column(db.TIMESTAMP, nullable=False)
