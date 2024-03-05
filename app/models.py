from app import db, login_manager
from flask_login import UserMixin
from .utilities.scraper_bot import ScraperBot
from sqlalchemy import CheckConstraint, func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    favourite_recipes = db.relationship('Recipe', secondary='favourites', backref='user_fav')
    added_recipes = db.relationship('Recipe', backref='created_by')
    reviews = db.relationship('Review', backref='user', cascade="all, delete")

    def __repr__(self):
        return f'User : {self.username}'

    def toggle_favourite(self, recipe_id):
        """
        Toggles recipe within user's favourite recipes
        :param recipe_id: Recipe's id to be toggled in the favourite recipes list
        :return:
        """
        recipe = Recipe.query.get(recipe_id)
        if recipe in self.favourite_recipes:
            self.favourite_recipes.remove(recipe)
            db.session.commit()

        else:
            self.favourite_recipes.append(recipe)
            db.session.commit()

    def add_recipe(self, new_recipe):
        """
        Creates a new private recipe object in the Recipe table referenced to the user object
        :param new_recipe: New recipe object
        :return:
        """
        recipe = Recipe(
            title=new_recipe['title'],
            category=new_recipe['category'],
            prep_time=new_recipe['prep_time'],
            cook_time=new_recipe['cook_time'],
            servings=new_recipe['servings'],
            ingredients=new_recipe['ingredients'].replace(',', ' | '),
            instructions=new_recipe['instructions'].replace('.', ' | '),
            img_filename=new_recipe['img_file'].filename if new_recipe['img_file'].filename else None,
            private=True,
            user_id=self.id
        )
        db.session.add(recipe)
        db.session.commit()

    def submit_rating(self, rating, recipe_id):
        """
        Replaces old rating if exists, else creates a new rating for the recipe with id = recipe_id
        :param rating: int (1 - 5)
        :param recipe_id: Recipe's id on which to add/replace rating
        :return:
        """
        old_rating = Review.query.filter(Review.rating.isnot(None), Review.user_id == self.id, Review.recipe_id == recipe_id).first()
        if old_rating:
            old_rating.rating = rating
        else:
            new_rating = Review(rating=rating, user_id=self.id, recipe_id=recipe_id)
            db.session.add(new_rating)
        db.session.commit()

    def post_comment(self, body, recipe_id):
        """
        Creates a new comment object in the Review table
        :param body: Submitted comment text
        :param recipe_id: Recipe's id on which the comment is submitted
        :return:
        """
        new_comment = Review(body=body, user_id=self.id, recipe_id=recipe_id)
        db.session.add(new_comment)
        db.session.commit()


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    prep_time = db.Column(db.String(50))
    cook_time = db.Column(db.String(50))
    servings = db.Column(db.String(10))
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    img_filename = db.Column(db.String(100), default='default.jpg')
    url = db.Column(db.String(100))
    private = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    reviews = db.relationship('Review', backref='recipe', cascade="all, delete")

    def __repr__(self):
        return f'Recipe : {self.title}'

    def get_recipe_data(self, url):
        """
        Scrapes recipe's details from the given url and creates a new recipe object in the Recipe table
        :param url: url from which to scrape recipe's data
        :return:
        """
        scraper = ScraperBot(url)
        recipe_details = scraper.get_details()
        self.title = scraper.get_title()
        self.category = scraper.get_category()
        self.prep_time = recipe_details['prep_time']
        self.cook_time = recipe_details['cook_time']
        self.servings = recipe_details['servings']
        self.ingredients = scraper.get_ingredients()
        self.instructions = scraper.get_instructions()
        self.img_filename = scraper.get_image_filename()
        self.url = url
        scraper.download_img()


class Favourites(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), primary_key=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('COALESCE(rating, body) NOT NULL'),
        CheckConstraint('rating <= 5 AND rating >= 0'),
    )

    def __repr__(self):
        if self.rating:
            return f'Rating from user: {self.user_id} for recipe: {self.recipe_id}'
        return f'Comment from user: {self.user_id} for recipe: {self.recipe_id}'



