from flask import Blueprint,request
from flask_jwt_extended import get_jwt_identity

from utils import restful
from exts import db
from models.auth_model import UserModel, Permission
from models.pet_model import PetModel
from .forms import AddPetForm


bp = Blueprint("cms", __name__, url_prefix="/petcms")


@bp.before_request
def petcms_before_request():
    if request.method == 'OPTIONS':
        return


@bp.get("/")
def test():
    # 這個identity是當初透過create_access_token傳入的identity
    identity = get_jwt_identity()
    return restful.ok(message="success", data={"identity": identity})


@bp.get("/pet/list")
def pet_list():
    pets = PetModel.query.order_by(PetModel.pet_id.desc())
    pet_dict = [pet.to_dict() for pet in pets]
    return restful.ok(data=pet_dict)


@bp.post("/pet/add")
def add_pet():
    form = AddPetForm(request.form)
    # print(form)
    if form.validate():
        pet_name = form.value.get("pet_name")
        pet_category = form.value.get("pet_category")
        pet_sex = form.value.get("pet_sex")
        pet_date = form.value.get("pet_date")
        pet_age = form.value.get("pet_age")
        pet_location = form.value.get("pet_location")
        pet_coat = form.value.get("pet_coat")
        pet_build = form.value.get("pet_build")
        pet_TNR = form.value.get("pet_TNR")
        pet_picture = form.value.get("pet_picture")
        pet_info = PetModel(pet_name=pet_name, pet_category=pet_category, pet_sex=pet_sex, pet_date=pet_date,
                            pet_age=pet_age, pet_location=pet_location, pet_coat=pet_coat, pet_build=pet_build,
                            pet_TNR=pet_TNR, pet_picture=pet_picture)
        print(pet_info)
        db.session.add(pet_info)
        db.session.commit()
        return restful.ok(data=pet_info.to_dict())
    else:
        return restful.params_error(message=form.messages[0])


@bp.post("/pet/delete")
def delete_pet():
    pet_id = request.form.get("pet_id")
    if not pet_id:
        return restful.params_error(message="沒有收到浪浪id！")
    try:
        pet_model = PetModel.query.get(pet_id)
    except Exception as e:
        print(e)
        return restful.params_error(message="浪浪編號不存在！")
    db.session.delete(pet_model)
    db.session.commit()
    return restful.ok()


@bp.get("/user/list")
def user_list():
    user_obj = UserModel.query.order_by(UserModel.join_time.desc()).all()
    user_dict = [user.to_dict() for user in user_obj]
    return restful.ok(data=user_dict)


@bp.post("/user/active")
def active_user():
    is_active = request.form.get('is_active', type=int)
    user_id = request.form.get("user_id")
    user = UserModel.query.get(user_id)
    user.is_active = is_active
    db.session.commit()
    return restful.ok(data=user.to_dict())
