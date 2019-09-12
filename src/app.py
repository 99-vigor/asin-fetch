import os

from app_config import MONGO_URL, DB_NAME, COLLECTION_NAME 
from flask import Flask
from asin_service import ASINService
from scraping.product_lookup_service import ProductLookupService
from repository.repository import Repository
from repository.repository_mongo import RepositoryMongo

app = Flask(__name__)

repo = Repository(RepositoryMongo(MONGO_URL, DB_NAME, COLLECTION_NAME))
lookup_service = ProductLookupService()
asin_service = ASINService(repo, lookup_service)

search_script = """
    <script language="javascript">
        function gotoASIN() {
            window.location.href = "/get/" + document.getElementById("asin_input").value;
        }
    </script>
"""
search_bar_component = """
    <form>
        <input type="text" id="asin_input"/>
        <input type="button" value="Search" onclick="gotoASIN()"/>
    </form>
"""

@app.route("/")
def hello():
    return """
        <html>
            <head>{}</head>
            <body>
                <div>
                    <h1>Welcome Jungle Scout!</h1>
                    <p>To test the app, type your desired ASIN in the field below and press "Search".</p>{}
                    <p>Alternatively, directly navigate to "/get/(ASIN)" to see product information for your desired item. Example: <a href="/get/B002QYW8LW">B002QYW8LW</a></p>
                </div>
            </body>
        </html>
    """.format(
        search_script,
        search_bar_component
    )

# Retrives an ASIN Entry from the database. If it is not present in the database,
# trigger a fetch operation for the ASIN from Amazon. The info is then rendered
@app.route("/get/<string:asin>", methods=["GET"])
def get_product(asin):
    try:
        # Attempt to retrieve info for this ASIN.
        # If it is not present in the database, a scraping operation is triggered.
        info = asin_service.get_product_info(asin)
        product_info = """
            <div>
                <h3>Product Info</h3>
                <ul>
                    <li><strong>ASIN: </strong>{}</li>
                    <li><strong>Category: </strong>{}</li>
                    <li><strong>Dimensions: </strong>{}</li>
                    <li><strong>Rank: </strong>{}</li>
                </ul>
            </div>
        """.format(
            info['asin'],
            info['category'],
            info['dimensions'],
            info['rank']
        )
    except Exception as e:
        product_info = 'Error: {}'.format(e)
    return "<html><head>{}</head><body>{}{}</body></html>".format(search_script, product_info, search_bar_component)

if __name__ == "__main__":
    app.run()