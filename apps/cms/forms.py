from wtforms.fields import StringField
from wtforms.validators import InputRequired
from wtforms import Form


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
        return message_list


class AddPetForm(BaseForm):
    pet_name = StringField(validators=[InputRequired(message='請輸入浪浪名字')])
    pet_category = StringField(validators=[InputRequired(message='請選擇浪浪類別！')])
    pet_sex = StringField(validators=[InputRequired(message='請選擇浪浪性別！')])
    pet_variety = StringField(validators=[InputRequired(message='請輸入浪浪品種！')])
    pet_date = StringField(validators=[InputRequired(message='請輸入浪浪收容日期！')])
    pet_age = StringField()
    pet_location = StringField(validators=[InputRequired(message='請輸入浪浪收容所所在地！')])
    pet_coat = StringField()
    pet_build = StringField(validators=[InputRequired(message='請選擇浪浪體型')])
    pet_TNR = StringField(validators=[InputRequired(message='請選擇浪浪是否結紮！')])
    pet_picture = StringField()
