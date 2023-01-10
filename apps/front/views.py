from flask import Blueprint, request, session, render_template
from flask_jwt_extended import create_access_token
from sqlalchemy.sql.expression import func
import json
import ast

from exts import db
from utils import restful
from utils.petrecommend import recommend_main
from models.auth_model import UserModel, DonateModel, Recommend_List,SelectModel, Permission
from models.pet_model import PetModel, ApplyModel, CityModel, VarietyModel

bp = Blueprint("front", __name__, url_prefix="/")


@bp.get('/petcms')
def cms():
    return render_template("cms/index.html")


# 登入
@bp.post("/login")
def login():
    data = json.loads(request.get_data())
    email = data['email']
    password = data['password']
    remember = data['remember']
    user = UserModel.query.filter_by(email=email).first()
    print(user)
    if not user:
        return restful.params_error("請註冊！")
    if not user.check_password(password):
        return restful.params_error("密碼錯誤！")
    if user.is_active != 1:
        return restful.params_error("用戶權限異常，如有疑問請洽客服！")
    # 把用戶id加密存到cookie
    session['user_id'] = user.user_id
    # 管理員才有token
    token = ""
    permissions = []
    if user.is_staff:
        token = create_access_token(identity=user.user_id)
        # 沒有下划線的權限返回到前端
        # 返回的權限全部小寫
        for attr in dir(Permission):
            if not attr.startswith("_"):
                permission = getattr(Permission, attr)
                if user.has_permission(permission):
                    permissions.append(attr.lower())
    if remember == 1:
        # 默認登入後7天有效(config.py)
        session.permanent = True
        print(session.permanent)
    user_dict = user.to_dict()
    user_dict['permissions'] = permissions
    print({"token": token, "user": user_dict})
    return restful.ok(data={"token": token, "user": user_dict})


# 註冊
@bp.route("/register", methods=['GET', 'POST'])
def register():
    data = json.loads(request.get_data())
    if data:
        email = data['email']
        username = data['username']
        password = data['password']
        user = UserModel(email=email, username=username, password=password)
        # print(user)
        db.session.add(user)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error()


# 偏好調查
@bp.post("/survey")
def prefer():
    data = json.loads(request.get_data())
    print(data)
    if data:
        userid = data['user_id']
        UserModel.query.filter_by(user_id=userid).update(
            dict(prefer_pet_category=data['prefer_pet_category'],
                 prefer_pet_variety=(",".join(data['prefer_pet_variety'])),
                 prefer_pet_sex=data['prefer_pet_sex']))
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error()


# 用戶後台
@bp.route("/user", methods=['GET', 'POST'])
def setting():
    data = json.loads(request.get_data())
    # print(data)
    if data:
        userid = data['user_id']
        userinfo = UserModel.query.filter_by(user_id=userid).first()
        points = DonateModel.query.filter_by(user_id=userid).all()
        # 將points中的值迭代出來存成一個list
        pointlist = [point.to_dict() for point in points]
        # 將points中的值迭代出來加總
        donate_sum = 0
        for money in points:
            donate_sum += money.point_number
        applys = ApplyModel.query.filter_by(user_id=userid).all()
        applylist = [apply.to_dict() for apply in applys]
        return restful.ok(data={"userinfo": userinfo.to_dict(), "pointhistory": pointlist, "donate_sum": donate_sum,
                                "applyhistory": applylist})
    else:
        return restful.params_error(message='用戶資訊異常')


# 領養列表
@bp.route("/pets", methods=['GET', 'POST'])
def pet_commend_list():
    data = request.get_data()
    if data:
        try:
            data = json.loads(data)
            print(data)
            user_id = data['user_id']
            # print(user_id)
            recommend_main(user_id)
            content = Recommend_List.query.filter_by(user_id=user_id).order_by(Recommend_List.time.desc()).first()
            pet_list = ast.literal_eval(content.recommend_pets)
            data = {"user_id": content.user_id, "pet_list": pet_list}
            # print(data)
            return restful.ok(data=data)
        except:
            query_pet = PetModel.query.order_by(PetModel.pet_join_time.desc())
            pet_list = [pet.to_dict() for pet in query_pet]
            # data = {pet_list}
            # print(type(data))
            return restful.ok(data={"pet_list": pet_list})
    else:
        query_pet = PetModel.query.order_by(PetModel.pet_join_time.desc())
        pet_list = [pet.to_dict() for pet in query_pet]
        # data = {pet_list}
        # print(type(data))
        return restful.ok(data={"pet_list": pet_list})


# 領養列表單支
@bp.post("/petlist/info")
def petinfo():
    data = request.get_data()
    if data:
        data = json.loads(data)
        # print(data)
        user_id = data['user_id']
        if user_id:
            content = Recommend_List.query.filter_by(user_id=user_id).order_by(Recommend_List.time.desc()).first()
            pet_list = ast.literal_eval(content.recommend_pets)
            return restful.ok(data={"pet_list": pet_list})
    else:
        query_pet = PetModel.query.order_by(PetModel.pet_join_time.desc())
        pet_list = [pet.to_dict() for pet in query_pet]
        return restful.ok(data={"pet_list": pet_list})


@bp.route("/select", methods=['GET', 'POST'])
def pet_select_list(**kwargs):
    data = json.loads(request.get_data())
    print(data)
    # user_id = "FPFfAn3ctkLEgh6uywP9HP"
    user_id = data['user_id']
    choice = {
        'pet_location': data['pet_location'],
        'pet_category': data['pet_category'],
        'pet_sex': data['pet_sex'],
        'pet_age': data['pet_age']
    }
    # print(choice)
    result = PetModel.query  #
    if choice['pet_category'] != '不限':
        result = result.filter_by(pet_category=choice['pet_category'])
    if choice['pet_sex'] != '不限':
        result = result.filter_by(pet_sex=choice['pet_sex'])
    if choice['pet_age'] != '不限':
        result = result.filter_by(pet_age=choice['pet_age'])

    result = result.filter(PetModel.pet_location.like(f"{choice['pet_location']}%"))
    result = result.order_by(func.rand())
    result = result.limit(15).all()
    selectlist = []
    for i in result:
        data = {}
        data['pet_variety'] = str(i.pet_variety)
        data['pet_location'] = str(i.pet_location)
        data['pet_picture'] = str(i.pet_picture)
        selectlist.append(data)
    print(type(selectlist))
    selectlist_str = str(selectlist)
    print(type(selectlist_str))
    # print()
    try:
        select = SelectModel(user_id=user_id, select_result=selectlist_str)
        db.session.add(select)
        db.session.commit()
        return restful.ok()
    except:
        SelectModel.query.filter_by(user_id=user_id).update(dict(select_result=selectlist_str))
        db.session.commit()
        return restful.ok()


@bp.route('/pets/select', methods=['GET', 'POST'])
def select_info():
    data = json.loads(request.get_data())
    user_id = data['user_id']
    # user_id = "FPFfAn3ctkLEgh6uywP9HP"
    selectinfo = SelectModel.query.filter_by(user_id=user_id).order_by(SelectModel.select_time.desc()).first()
    selectinfo_list = ast.literal_eval(selectinfo.select_result)
    print(selectinfo_list)
    return restful.ok(data={"select_list": selectinfo_list})


# 領養申請表
@bp.route("/apply", methods=['GET', 'POST'])
def pet_apply():
    req_json = json.loads(request.get_data())
    print(req_json)
    if req_json:
        user_id = req_json['user_id']
        pet_id = req_json['pet_id']
        check_owner = req_json["check_owner"]
        owner = req_json["owner"]
        applicant_last_name = req_json["applicant_last_name"]
        email = req_json["email"]
        applicant_first_name = req_json["applicant_first_name"]
        ID_number = req_json["ID_number"]
        birth = req_json["birth"]
        job = req_json["job"]
        city = req_json["city"]
        district = req_json["district"]
        phone = req_json["phone"]
        contact_time = req_json["contact_time"]
        second_contact_name = req_json["second_contact_name"]
        second_contact_phone = req_json["second_contact_phone"]
        second_contact_email = req_json["second_contact_email"]
        relation = req_json["relation"]
        marriage = req_json["marriage"]
        family_members = req_json["family_members"]
        underage = req_json["underage"]
        check_allergy = req_json["check_allergy"]
        family_income = req_json["family_income"]
        check_rent = req_json["check_rent"]
        sqft = req_json["sqft"]
        apply_info = ApplyModel(user_id=user_id, pet_id=pet_id, check_owner=check_owner, owner=owner,
                                applicant_last_name=applicant_last_name, email=email,
                                applicant_first_name=applicant_first_name, ID_number=ID_number, birth=birth, job=job,
                                city=city, district=district, phone=phone, contact_time=contact_time,
                                second_contact_name=second_contact_name, second_contact_phone=second_contact_phone,
                                second_contact_email=second_contact_email, relation=relation, marriage=marriage,
                                family_members=family_members, underage=underage, check_allergy=check_allergy,
                                family_income=family_income, check_rent=check_rent, sqft=sqft)

        db.session.add(apply_info)
        db.session.commit()
        return restful.ok(data=apply_info.to_dict())
    else:
        return restful.params_error(message="請先登入會員")


@bp.get("/city")
def city():
    content = CityModel.query.filter_by(city_id=1).first()
    city_list = ast.literal_eval(content.city)
    print(city_list)
    return restful.ok(data=city_list)


@bp.get("/variety")
def variety():
    content = VarietyModel.query.filter_by(variety_id=1).first()
    variety_list = ast.literal_eval(content.variety)
    print(variety_list)
    return restful.ok(data=variety_list)