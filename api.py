
from flask import Flask, jsonify
import sqlite3

# Configuration
app = Flask(__name__)

DATABASE = "business_data.db"


# Connexion à la base SQLite
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# 1. Vérifier que l'API fonctionne
@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "API opérationnelle"
    }), 200


# 2. Afficher les 100 premières ventes
@app.route("/sales", methods=["GET"])
def get_sales():

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM final_consolidated_data
            LIMIT 100
        """)

        rows = cursor.fetchall()

        sales = [dict(row) for row in rows]

        return jsonify({
            "status": "success",
            "count": len(sales),
            "data": sales
        }), 200

    except sqlite3.Error as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


# 3. Afficher les ventes totales par ville
@app.route("/sales-by-city", methods=["GET"])
def sales_by_city():

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                city,
                SUM(revenue) AS total_revenue
            FROM final_consolidated_data
            GROUP BY city
            ORDER BY total_revenue DESC
        """)

        rows = cursor.fetchall()

        result = [dict(row) for row in rows]

        return jsonify({
            "status": "success",
            "count": len(result),
            "data": result
        }), 200

    except sqlite3.Error as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        conn.close()


# 4. Lancement de l'API
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
