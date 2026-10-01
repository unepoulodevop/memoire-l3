"""
Application e-commerce minimale — Mémoire L3.
Catalogue de produits (lecture) + prise de commande (écriture),
utilisée pour démontrer la résilience de l'infrastructure (Chapitre 3).
"""
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Paramètres de connexion MySQL, fournis via variables d'environnement
# (injectées par Kubernetes dans le chart Helm — jamais écrits en dur).
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "mysql-primary"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "ecommerce"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "ecommerce"),
}


def get_db_connection():
    """Ouvre une nouvelle connexion MySQL pour la requête en cours."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
    """Affiche le catalogue de produits disponibles."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, stock FROM products ORDER BY id")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", products=products)


@app.route("/order", methods=["POST"])
def place_order():
    """Enregistre une nouvelle commande et décrémente le stock."""
    product_id = request.form["product_id"]
    customer_name = request.form["customer_name"]
    quantity = int(request.form["quantity"])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (product_id, customer_name, quantity) VALUES (%s, %s, %s)",
        (product_id, customer_name, quantity),
    )
    cursor.execute(
        "UPDATE products SET stock = stock - %s WHERE id = %s",
        (quantity, product_id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/healthz")
def healthz():
    """Endpoint de santé, utilisé par Kubernetes pour les sondes liveness/readiness."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)