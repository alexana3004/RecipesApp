from flask import Blueprint, render_template, session
from sqlalchemy import func
from app.utilities.main import get_categories
from app.models import Recipe, Review
from app import db

main = Blueprint("main", __name__, template_folder="templates")


@main.route('/')
@main.route('/home')
def index():
    """Displays homepage"""
    session['categories'] = get_categories()
    latest_recipes = db.session.query(
        Recipe, func.count(Review.rating).label('rating_count'), func.avg(Review.rating).label('avg_rating')).filter(
        Recipe.private.is_(False)).outerjoin(
        Review, Recipe.id == Review.recipe_id).group_by(Recipe.id).order_by(Recipe.id.desc()).limit(6).all()

    return render_template('index.html', recipes_data=latest_recipes)
