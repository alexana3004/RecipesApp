from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Checks if 'username' is already registered in the database
        :param username:
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Try another.')

    def validate_email(self, email):
        """
        Checks if 'email' is already registered in the database
        :param email:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Try another.')


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired()])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[InputRequired('')])
    submit = SubmitField('Send')


class AddRecipeForm(FlaskForm):
    title = StringField('Title:', validators=[InputRequired()])
    category = StringField('Category:')
    prep_time = StringField('Preparation Time:')
    cook_time = StringField('Cooking Time:')
    servings = StringField('Servings:')
    ingredients = TextAreaField('Ingredients:', validators=[InputRequired()])
    instructions = TextAreaField('Instructions:', validators=[InputRequired()])
    img_file = FileField('Upload Image:', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Save')

    def populate_form(self, recipe_to_edit):
        """
        Autofill the form with the recipe data to be edited
        :param recipe_to_edit: recipe object
        :return:
        """
        self.title = recipe_to_edit.title
        self.category = recipe_to_edit.category
        self.prep_time = recipe_to_edit.prep_time
        self.cook_time = recipe_to_edit.cook_time
        self.servings = recipe_to_edit.servings
        self.ingredients = recipe_to_edit.ingredients
        self.instructions = recipe_to_edit.instructions
        return self
