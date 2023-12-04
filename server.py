from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("eshop.db")
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     price INTEGER)
""")
con.commit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
def products():
    con = sqlite3.connect("eshop.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    products = []
    for row in result:
        products.append({'name': row[1], 'id': row[0], 'price': row[2]})
    return render_template("products.html", products=products)

@app.route("/add/product", methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get("price")
        con = sqlite3.connect("eshop.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        con.commit()
        return redirect("/products")
    else:
        return render_template("add_product.html")
