from bs4 import BeautifulSoup
import requests

url_root = "https://myfoodbook.com.au"


class ScraperBot:
    def __init__(self, url):
        self.url = url
        self.soup = self.create_soup()

    def create_soup(self):
        """
        Creates BS object from self.url
        :return: BS object
        """
        response = requests.get(self.url)
        contents = response.text
        soup = BeautifulSoup(contents, "html.parser")
        return soup

    def get_pages_total(self):
        """
        Fetches total number of pages
        :return: last page number
        """
        href = self.soup.select_one('.pager-last a').get('href')
        pages_num = href.split('=')[1]
        return int(pages_num)

    def get_urls_from_page(self):
        """
        Fetches all recipe urls from self.url
        :return: A list with recipe urls
        """
        all_recipes = [url_root + a.get('href') for a in self.soup.select('.recipe-card-list .card-photo a')]
        return all_recipes

    def get_title(self):
        """
        :return: Recipe's title
        """
        title = self.soup.find('title').getText().split('Recipe')[0]
        return title

    def get_ingredients(self):
        """
        :return: Recipe's ingredients string
        """
        ingredients_list = [ingredient.getText() for ingredient in
                            self.soup.select("label[itemprop='recipeIngredient']")]
        ingredients = '|'.join(ingredients_list)
        return ingredients

    def get_instructions(self):
        """
        :return: Recipe's instructions string
        """
        instructions_list = [step.getText() for step in self.soup.find_all(class_="method-step")]
        instructions = '|'.join(instructions_list)
        return instructions

    def get_details(self):
        """
        :return: Recipe's details dictionary
        """
        prep_time = self.soup.select_one('.recipe-props > div:nth-child(1)').getText().split(':')[1]
        cook_time = self.soup.select_one('.recipe-props > div:nth-child(2)').getText().split(':')[1]
        serves = self.soup.select_one('.recipe-props > div:nth-child(3)').getText().split(':')[1]
        return {'prep_time': prep_time, 'cook_time': cook_time, 'serves': serves}

    def get_category(self):
        """
        :return: Recipe's category
        """
        category = self.soup.select_one("meta[itemprop='recipeCategory']").get('content')
        return category

    def get_image_source(self):
        """
        :return: Recipe's image url
        """
        img_src = self.soup.select_one(".cp-car-photo source[media='(min-width:740px)']").get("srcset").split(' ')[0]
        return img_src

    def get_image_filename(self):
        """
        :return: Recipe's image filename
        """
        filename = self.get_image_source().split('/')[-1].replace('%20', '-')
        return filename

    def download_img(self):
        """
        Saves recipe's image to static/images folder
        :return:
        """
        file_path = f"./static/images/{self.get_image_filename()}"
        response = requests.get(url_root + self.get_image_source())
        with open(file_path, "wb") as file:
            file.write(response.content)
