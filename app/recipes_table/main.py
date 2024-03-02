from app.recipes_table.scraper_bot import ScraperBot
from app.models import Recipe
from app import db

main_categories = ['dinner']


def get_all_recipes_urls():
    """
    Scrapes all recipe urls for all categories in main_categories
    :return: A list with recipe urls
    """
    urls = []
    for category in main_categories:
        s = ScraperBot(f"https://myfoodbook.com.au/categories/{category}?")
        total_pages = s.get_pages_total()
        for n in range(1):  # total_pages
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
