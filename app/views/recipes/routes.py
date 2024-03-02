from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user
from app.recipes_table.main import update_recipes_table
from app.utils import save_image, remove_old_image
from app.models import Recipe, Review
from app.forms import CommentForm, AddRecipeForm
from app import db
from sqlalchemy import func

recipes = Blueprint("recipes", __name__, template_folder="templates")


@recipes.route('/update-recipes')
@login_required
def update_recipes():
    """Checks for new recipes on the server. If found scrapes them and adds them to database"""
    if current_user.id != 1:
        abort(403)
    new_recipes_count = update_recipes_table()
    if new_recipes_count == 1:
        flash("1 new recipe has been added to the collection.")
    elif new_recipes_count != 0 and new_recipes_count > 1:
        flash(f"{new_recipes_count} new recipes have been added to the collection.")
    else:
        flash("No new recipes have been added to your database.")
    return redirect(url_for('main.index'))


@recipes.route('/search-results', methods=['GET', 'POST'])
def show_results():
    """Shows search results"""
    if request.method == 'POST':
        query = request.form.get('query')
    else:
        query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    per_page = 2

    if query:
        ingredients = query.split(' ')
        results = db.session.query(Recipe)
        for ingredient in ingredients:
            results = results.filter(Recipe.ingredients.contains(ingredient) | Recipe.category.contains(ingredient))
        results = results.all()
        search_results = db.session.query(
            Recipe, func.count(Review.rating).label('rating_count'), func.avg(Review.rating).label('avg_rating')).filter(
            Recipe.id.in_([recipe.id for recipe in results])).outerjoin(
            Review, Recipe.id == Review.recipe_id).group_by(Recipe.id).order_by(Recipe.id.desc()).paginate(page=page, per_page=per_page)
        total_pages = search_results.total // per_page
        if search_results.total % per_page != 0:
            total_pages += 1

        return render_template('recipes/search_results.html', query=query, recipes_data=search_results, per_page=per_page, total_pages=total_pages)
    else:
        return render_template('recipes/search_results.html', query=query)


@recipes.route('/recipe/<recipe_title>', methods=['GET', 'POST'])
def recipe(recipe_title):
    """Displays recipe"""
    form = CommentForm()
    recipe_id = request.args.get('recipe_id')
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.private:
        if current_user.is_anonymous or recipe.user_id != current_user.id:
            abort(403)

    recipe = db.session.query(Recipe, func.count(Review.rating).label('rating_count'), func.avg(Review.rating).label('avg_rating')).filter(
        Recipe.id == recipe_id).outerjoin(Review, Recipe.id == Review.recipe_id).group_by(Recipe.id).all()
    data = {
        'recipe': recipe[0],
        'ratings': Review.query.filter(Review.rating.isnot(None), Review.recipe_id == recipe_id).all(),
        'comments': Review.query.filter(Review.body.isnot(None), Review.recipe_id == recipe_id).order_by(Review.date_created.desc()).all()
    }

    if form.validate_on_submit():
        current_user.post_comment(form.body.data, recipe_id)
        return redirect(url_for('recipes.recipe', recipe_title=recipe_title, recipe_id=recipe_id))

    return render_template('recipes/recipe.html', data=data, comment_form=form)


@recipes.route('/submit-rating', methods=['POST'])
@login_required
def submit_rating():
    """Adds rating to database for the current recipe"""
    next_url = request.form.get('next_url')
    recipe_id = request.args.get('recipe_id')
    new_rating = int(request.form.get('rating'))
    recipe_id = Recipe.query.get_or_404(recipe_id).id
    current_user.submit_rating(new_rating, recipe_id)
    return redirect(next_url)


@recipes.route('/toggle-recipe-favourites', methods=['POST'])
@login_required
def toggle_favourite():
    """Toggles the recipe in the user's favourite recipes list"""
    next_url = request.form.get('next_url')
    recipe_id = request.args.get('recipe_id')
    current_user.toggle_favourite(recipe_id)
    return redirect(next_url)


@recipes.route('/favourite-recipes')
@login_required
def favourites():
    """Displays user's favourite recipes"""
    favourite_recipes = current_user.favourite_recipes
    return render_template('recipes/user_recipes.html', recipes=favourite_recipes, is_private=False)


@recipes.route('/user-recipes')
@login_required
def user_recipes():
    """Displays recipes created by current user"""
    added_recipes = current_user.added_recipes[::-1]
    return render_template('recipes/user_recipes.html', recipes=added_recipes, is_private=True)


@recipes.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """Adds new recipe to database"""
    form = AddRecipeForm()
    if form.validate_on_submit():
        if form.img_file.data:
            save_image(form.img_file.data)
        current_user.add_recipe(new_recipe=form.data)
        flash("Your recipe has been successfully added.")
        return redirect(url_for('recipes.user_recipes'))
    return render_template('recipes/add-recipe.html', form=form)


@recipes.route('/edit-recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """Edits recipe in database"""
    recipe_to_edit = Recipe.query.get_or_404(recipe_id)
    if current_user.is_anonymous or recipe_to_edit.user_id != current_user.id:
        abort(403)
    form = AddRecipeForm(data=recipe_to_edit.__dict__)
    if form.validate_on_submit():
        if form.img_file.data:
            remove_old_image(recipe_to_edit.img_filename)
            save_image(form.img_file.data)
            recipe_to_edit.img_filename = form.img_file.data.filename
        form.ingredients.data = form.ingredients.data.replace(',', ' | ')
        form.instructions.data = form.instructions.data.replace('.', ' | ')
        form.populate_obj(recipe_to_edit)
        db.session.commit()
        flash("Your recipe has been successfully edited.")
        return redirect(url_for('recipes.user_recipes'))
    return render_template('recipes/add-recipe.html', form=form)


@recipes.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """Deletes recipe from database"""
    recipe_to_delete = Recipe.query.get_or_404(recipe_id)
    if current_user.is_anonymous or recipe_to_delete.user_id != current_user.id:
        abort(403)
    db.session.delete(recipe_to_delete)
    db.session.commit()
    return redirect(url_for('recipes.user_recipes'))


