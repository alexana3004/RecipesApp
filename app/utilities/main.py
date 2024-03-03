from app.utilities.scraper_bot import ScraperBot
from app.models import Recipe
from app import db
from werkzeug.utils import secure_filename
import os
from PIL import Image
from flask import current_app
from sqlalchemy.sql import func

main_categories = ['dinner']


def get_all_recipes_urls():
    """
    Scrapes all recipe urls for all categories in main_categories
    :return: A list with recipe urls
    """
    urls = []
    for category in main_categories:
        s = ScraperBot(f"https://myfoodbook.com.au/categories/{category}?")
        # total_pages = s.get_pages_total()
        total_pages = 1
        for n in range(total_pages):
            page_num = n
            page_url = f"https://myfoodbook.com.au/categories/{category}?page={page_num}"
            scraper = ScraperBot(page_url)
            urls.extend(scraper.get_urls_from_page())
    return urls


def check_recipe_in_db(url):
    """
    :param url: Recipe url
    :return: True if url already exists in database.
    """
    if not Recipe.query.filter_by(url=url).first():
        return True


def write_to_db(recipe_obj):
    """
    Adds recipe object to database
    :param recipe_obj: recipe object
    :return:
    """
    db.session.add(recipe_obj)
    db.session.commit()


def update_recipes_table():
    """
    Scrapes new recipes and adds them to database
    :return: The total number of newly added recipes.
    """
    recipes_urls = get_all_recipes_urls()
    new_recipes_count = 0
    for url in recipes_urls:
        if check_recipe_in_db(url):
            recipe = Recipe()
            recipe.get_recipe_info(url)
            write_to_db(recipe)
            new_recipes_count += 1
    return new_recipes_count


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
