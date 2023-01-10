from flask import Flask, render_template
from flask_migrate import Migrate

import config
import commands
from exts import db, cors, jwt
from apps.front import front_bp
from apps.cms import cms_bp


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(config)

db.init_app(app)
jwt.init_app(app)
# 跨域
cors.init_app(app)

## ORM-mysql
# 初始化倉庫:flask db init
# orm--script:flask db migrate
# script work:flask db upgrade
migrate = Migrate(app, db)


# 註冊blueprint
app.register_blueprint(front_bp)
app.register_blueprint(cms_bp)

# 註冊命令
# flask init_roles
# flask bind_roles
app.cli.command("bind_roles")(commands.bind_roles)
app.cli.command("init_roles")(commands.init_roles)
app.cli.command("init_developer")(commands.init_developer)
app.cli.command("init_admin")(commands.init_admin)


@app.route('/')
def hello_world():
    return render_template("front/index.html")


if __name__ == '__main__':
    app.run(port=8000, host="localhost")
