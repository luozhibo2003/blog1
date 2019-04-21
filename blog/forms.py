from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional, URL, ValidationError

from blog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    # 因为Flask-SQLAlchemy依赖于程序上下文才能正常工作（内部使用current_app获取配置信息），
    # 所以这个查询调用要放到构造方法中执行，
    # 在构造方法中对self.category.choices赋值的效果和在类中实例化
    # SelectField类并设置choices参数相同。
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('分类', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类名称已经存在')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0.255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
