from .models import Recipe
from werkzeug.utils import secure_filename
import os
from PIL import Image
from flask import current_app
from sqlalchemy.sql import func


def get_categories():
    """

    :return: A list with all unique categories of recipes from Recipe table
    """
    recipes_categories = Recipe.query.with_entities(Recipe.category).filter(Recipe.private.is_(False)).group_by(
        Recipe.category).order_by(func.count(Recipe.id).desc()).all()
    distinct_categories = [ctg[0] for ctg in recipes_categories[:10] if ctg[0]]
    return distinct_categories


def save_image(image):
    """
    Saves image to the static/images folder
    :param image: Image object
    :return:
    """
    output_size = (500, 500)
    image_fn = secure_filename(image.filename)
    img = Image.open(image)
    img.thumbnail(output_size)
    img.save(os.path.join(current_app.root_path, 'static/images', image_fn))


def remove_old_image(img_filename):
    """
    Deletes the file named 'img_filename' if different from 'default.jpg'
    :param img_filename: Picture filename
    :return:
    """
    if img_filename != 'default.jpg':
        img_path = os.path.join(current_app.root_path, 'static/images', img_filename)
        os.remove(img_path)
