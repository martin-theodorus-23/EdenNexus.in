from flask import Flask, render_template, abort, jsonify, send_file, request
import csv,json, os

prd_file = "/home/edennexus/mysite_2/db/products.csv"

# functions
def load_products_from_csv(file_path= prd_file):
    products = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Automatically detects column names
        for row in reader:
            products.append(row)  # Keep the row exactly as it is (dynamic)
    return products

# =================================

app = Flask(__name__)


# ✅ login Page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/")
def index():
    return render_template('home.html')


# ✅ Home Page
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    products = load_products_from_csv()

    # ✅ Get all unique categories from CSV
    categories = sorted(list(set([item["category"] for item in products])))

    # ✅ Group products by category (for tab-based display)
    products_by_category = {}
    for category in categories:
        products_by_category[category] = [p for p in products if p["category"] == category]

    return render_template(
        'shop.html',
        products=products,
        categories=categories,
        products_by_category=products_by_category
    )

# ✅ MAC Page
@app.route('/mac')
def mac():
    return render_template('mac.html')

# ✅ Cart Page
@app.route('/cart')
def cart():
    return render_template('eden_nexus_cart_demo (2).html')

# ✅ Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ✅ About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Get the absolute path to the folder where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/trade')
def trader_dashboard():
    # Ensure 'trader_pro.html' is in the exact same folder as this python file.
    file_path = os.path.join(BASE_DIR, 'trader_pro.html')

    return send_file(file_path)

# ✅ 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

