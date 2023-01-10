from models.auth_model import UserModel, RoleModel, Permission
from exts import db


# 0b001
# 0b010
# 0b011 = ob001 | ob010
# 1|0=1,1|1=1,0|0=0

def init_roles():
    # 管理員
    admin_role = RoleModel(name="管理員", desc="負責管理寵物與用戶",
                           permissions=Permission.USER | Permission.PETS)
    # 開發人員
    developer_role = RoleModel(name="開發人員", desc="負責網站開發", permissions=Permission.ALL_PERMISSION)

    db.session.add_all([admin_role, developer_role])
    db.session.commit()
    print("添加成功！")


def init_developer():
    role = RoleModel.query.filter_by(name="開發人員").first()
    user = UserModel(username="aaaaaa", email="aaaaaa@aa.com", password='aaaaaa', is_staff=True, role=role)
    db.session.add(user)
    db.session.commit()
    print('開發人員創建成功！')


def init_admin():
    role = RoleModel.query.filter_by(name="管理員").first()
    user = UserModel(username="bbbbbb", email="bbbbbb@bb.com", password='bbbbbb', is_staff=True, role=role)
    db.session.add(user)
    db.session.commit()
    print('管理員創建成功！')


def bind_roles():
    user1 = UserModel.query.filter_by(email="aaaaaa@aa.com").first()
    user2 = UserModel.query.filter_by(email="bbbbbb@bb.com").first()

    role1 = RoleModel.query.filter_by(name="開發人員").first()
    role2 = RoleModel.query.filter_by(name="管理員").first()

    user1.role = role1
    user2.role = role2

    db.session.commit()
    print("權限绑定成功！")
