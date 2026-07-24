# Search Open Beauty Facts API for a product and return its ingredient list
import requests

class IngredientFetcher:
    def get_product_ingredients(self, product_name):
        params = {
            'search_terms' : product_name,
            'search_simple' : 1,
            'action' : 'process',
            'json' : 1
        }
        response = requests.get('https://world.openbeautyfacts.org/cgi/search.pl', params=params)
        data = response.json()
        if not data['products'] or not data['products'][0].get('ingredients_text_en'):
            return None
        product = data['products'][0]['ingredients_text_en']
        return product
