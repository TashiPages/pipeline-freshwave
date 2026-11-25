
import pandas as pd
import sqlite3
import requests

# Configuration de la base de données
business_data = "business_data.db"


#--------------------------------------------------------

# 1. Support fichiers 
# 1.1 SQL : Initialisation de la base de données SQLite
def init_database():

    print("Initialisation de la base de données...")

    conn = sqlite3.connect(business_data)
    cursor = conn.cursor()

    try:
        # Lecture et exécution du fichier stores.sql
        with open("stores.sql", "r", encoding="utf-8") as file:
            stores_sql = file.read()
            cursor.executescript(stores_sql)

        # Lecture et exécution du fichier products.sql
        with open("products.sql", "r", encoding="utf-8") as file:
            products_sql = file.read()
            cursor.executescript(products_sql)

        conn.commit()

        print("Tables stores et products créées avec succès.")

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'initialisation : {e}")
        raise

    finally:
        conn.close()

#--------------------------------------------------------

# 1.2 API :



# 1.2.1 identifier les infos disponibles dans l'url :
 
# 1.2.1.1. Partir de l'adresse que tu possèdes :https://archive-api.open-meteo.com/v1/archive
# 1.2.1.2. Faire une recherche Google Open-Meteo API documentation archive
# 1.2.1.3. aller sur le site officiel open-meteo Puis chercher une rubrique appelée :Documentation, API Documentation ou Historical Weather API
""" Chemin : 
1.Identifier le fournisseur
Exemple : Open-Meteo.
2.Chercher sa documentation
Exemple : Open-Meteo API documentation.
3.Identifier le bon service
Exemple : Historical Weather API plutôt que Weather Forecast API.
4.Chercher les paramètres disponibles
Exemple : latitude, longitude, start_date, end_date.
5.Chercher les variables disponibles
Exemple : température, pluie, vent.
6.Tester une requête
Vérifier que l'API renvoie bien les données attendues.(p.ex https://archive-api.open-meteo.com/v1/archive?latitude=48.8566&longitude=2.3522&start_date=2024-05-01&end_date=2024-05-05)"""

# 1.2.2 Definir des variables
START_DATE = "2024-05-01"

END_DATE = "2024-08-31"

CITY_COORDS = {
    "Paris": (48.8566, 2.3522),
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Nantes": (47.2184, -1.5536),
    "Toulouse": (43.6047, 1.4442),
    "Nice": (43.7102, 7.2620)}


# 1.2.3 API :Créer la fonction fetch_weather_for_city()

def fetch_weather_for_city(city, lat, lon):

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],
        "timezone": "Europe/Paris"
    }

    # Appel de l'API
    response = requests.get(url, params=params, timeout=30)

    # Vérification de la réponse
    response.raise_for_status()

    # Conversion de la réponse JSON
    data = response.json()

    # Création du DataFrame
    weather = pd.DataFrame(data["daily"])

    # Renommer les colonnes
    weather = weather.rename(columns={
        "time": "date",
        "temperature_2m_max": "temperature_max",
        "temperature_2m_min": "temperature_min",
        "precipitation_sum": "precipitation",
        "wind_speed_10m_max": "wind_speed_max"
    })

    # Ajouter la ville
    weather["city"] = city

    return weather

#--------------------------------------------
# 2. Extraction des données
def extract():

# 2.1 Extraction CSV
# 2.1.1 Lire les fichiers csv 
    sales = pd.read_csv("sales.csv")
    marketing = pd.read_csv("marketing_campaigns.csv")






# 2.2 Extraction SQL

# 2.2.1 Connexion à la base de données SQLite
    conn = sqlite3.connect(business_data)


# 2.2.2 Extraction des tables SQLite dans des DataFrames
    stores = pd.read_sql("SELECT * FROM stores", conn)
    products = pd.read_sql("SELECT * FROM products", conn)

# 2.2.3 Fermeture de la conenction
    conn.close()


# 2.3 Extraction API


    # 2.3.1 Liste pour stocker les données météo
    weather_data = []

    # 2.3.2 Parcourir toutes les villes
    for city, (lat, lon) in CITY_COORDS.items():

        print(f"Récupération des données météo pour {city}...")

        # 2.3.3 Récupérer les données météo de la ville
        city_weather = fetch_weather_for_city(city, lat, lon)

        # 2.3.4 Transformer date en données de date
        city_weather["date"] = pd.to_datetime(city_weather["date"])

        # 2.3.5 Ajouter le DataFrame à la liste
        weather_data.append(city_weather)

    # 2.3.5 Concaténer les données de toutes les villes
    weather = pd.concat(weather_data, ignore_index=True)

    # 2.3.6 Vérification des données
    print("\n--- Vérification des données météo ---")

    print("Dimensions du DataFrame :", weather.shape)

    print("\nVilles présentes :")
    print(weather["city"].unique())

    print("\nDate minimale :", weather["date"].min())
    print("Date maximale :", weather["date"].max())

  
# 2.4 Stocker les données dans un dictionaire que s'apelle data	 
    data = {"sales" : sales , "marketing_campaigns" : marketing , "stores" : stores , "products" : products,"weather": weather}



# 2.5 le resultat de cette fonction doit etre le dictionaire qu'on a crée et apellé data bien 

    return data

#--------------------------------------------------------



# 3. Transformation des données (Etape 4 de l'ennoncé)

# 3. Transformation des données
def transform(data):

    # 3.1 Récupérer les DataFrames depuis le dictionnaire data
    sales = data["sales"].copy()
    marketing = data["marketing_campaigns"].copy()
    stores = data["stores"].copy()
    products = data["products"].copy()
    weather = data["weather"].copy()

    # 3.2 Nettoyage des dates
    sales["date"] = pd.to_datetime(sales["date"])
    marketing["date"] = pd.to_datetime(marketing["date"])
    weather["date"] = pd.to_datetime(weather["date"])

    # 3.3 Filtrer les données sur la période mai-août 2024
    start_date = "2024-05-01"
    end_date = "2024-08-31"

    filtered_sales = sales[
        (sales["date"] >= start_date) &
        (sales["date"] <= end_date)
    ]

    filtered_marketing = marketing[
        (marketing["date"] >= start_date) &
        (marketing["date"] <= end_date)
    ]

    # 3.4 Fusion des ventes avec les magasins et les produits
    sales_global = filtered_sales.merge(
        stores,
        on="store_id",
        how="left"
    ).merge(
        products,
        on="product_id",
        how="left"
    )

    # 3.5 Fusion des données météo avec les ventes
    sales_global = sales_global.merge(
        weather,
        on=["date", "city"],
        how="left"
    )

    # 3.6 Création de la variable is_weekend
    sales_global["is_weekend"] = (
        sales_global["date"].dt.dayofweek.isin([5, 6])
    )

    # 3.7 Création de la variable temp_bucket
    sales_global["temp_bucket"] = pd.cut(
        sales_global["temperature_max"],
        bins=[
            -float("inf"),
            20,
            25,
            30,
            float("inf")
        ],
        labels=[
            "<=20°C",
            "20-25°C",
            "25-30°C",
            ">30°C"
        ]
    )

    # 3.8 Création de la variable rain_bucket
    sales_global["rain_bucket"] = pd.cut(
        sales_global["precipitation"],
        bins=[
            -0.001,
            0,
            5,
            20,
            float("inf")
        ],
        labels=[
            "0 mm",
            "0-5 mm",
            "5-20 mm",
            ">20 mm"
        ]
    )

    # 3.9 Calcul des agrégations
    sales_global_agg = sales_global.groupby(
        [
            "date",
            "store_id",
            "store_name",
            "city",
            "product_id",
            "product_name"
        ],
        as_index=False,
        observed=True
    ).agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("quantity_sold", "sum"),
        nb_transactions=("sale_id", "nunique")
    )


    # 3.10 KPI - Analyse des ventes par température

    ventes_vs_temp = sales_global.groupby(["temp_bucket","category"],observed = True).agg({"revenue":"mean"}).reset_index().round()

 
    # 3.11 KPI - Impact de la pluie sur les ventes
    ventes_vs_pluie = sales_global.groupby(["rain_bucket","category"],observed = True).agg({"revenue":"mean"}).reset_index().round()

    # 3.12 KPI - Impact des campagnes marketing
    sales_marketing_global = sales_global.merge(marketing, on = ["date","city"],
        how="inner")    
    marketing_impact = sales_marketing_global.groupby(["campaign_type"],observed = True).agg({"revenue":"mean","marketing_spend":"mean","campaign_id":"nunique"}).reset_index().round()

    # 3.13 KPI - Analyse des performances par ville
    ventes_vs_ville = sales_global.groupby(["city"],observed = True).agg({"revenue" : "sum"}).reset_index().round()

    # 3.14 KPI - Analyse des performances par week-end
    sales_global['day_type'] = sales_global['date'].dt.dayofweek.apply(
    lambda x: 'Weekend' if x >= 5 else 'Weekday'
)
    ventes_we = sales_global.groupby(["day_type"],observed = True).agg({"revenue" : "sum"}).reset_index().round()


    # 3.15 Creer DataFrame final
    final_consolidated_data = sales_marketing_global.groupby(["date", "city", "store_id", "product_name","temperature_max","precipitation"] , observed = True).agg({"revenue" : "sum", "quantity_sold": "sum", "sale_id" : "nunique","marketing_spend": "sum" }).reset_index().round()





    # 3.16 Vérification du résultat
    print("\n--- Vérification des données transformées ---")
    print("Dimensions :", sales_global.shape)
    print("Table global :")
    print( sales_global.head())
    print( sales_global.columns)

    print("Ventes par jour, magasin, ville et produit :")
    print(sales_global_agg)

    print("KPI - Analyse des ventes par température")
    print(ventes_vs_temp)

    print("KPI - Impact de la pluie sur les ventes")
    print(ventes_vs_pluie)

    print("KPI - Impact des campagnes marketing")
    print(marketing_impact)

    print("KPI - Analyse des performances par ville")
    print(ventes_vs_ville)

    print("KPI - Analyse des performances par week-end")
    print(ventes_we)

    print("Data Frame final")
    print(final_consolidated_data)

    # 3.17 Retourner les données transformées
    return final_consolidated_data    




# 4. Chargement des données
def load(data):
    print("Chargement des données dans SQLite...")

    # 4.1 Connexion à la base de données SQLite
    conn = sqlite3.connect(business_data)

    try:
        # 4.2 Enregistrer le DataFrame dans une table SQLite
        data.to_sql(
            "final_consolidated_data",
            conn,
            if_exists="replace",
            index=False
        )

        print("Données enregistrées avec succès.")

        # 4.3 Vérifier que la table existe
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='final_consolidated_data'
        """)

        table = cursor.fetchone()

        if table:
            print("La table final_consolidated_data existe.")

        # 4.4 Vérifier les colonnes de la table
        cursor.execute("PRAGMA table_info(final_consolidated_data)")

        columns = cursor.fetchall()

        print("\nColonnes enregistrées dans SQLite :")

        for column in columns:
            print(column[1])

        # 4.5 Vérifier le nombre de lignes enregistrées
        cursor.execute(
            "SELECT COUNT(*) FROM final_consolidated_data"
        )

        nb_lignes = cursor.fetchone()[0]

        print("\nNombre de lignes enregistrées :", nb_lignes)

    except Exception as e:
        print("Erreur lors du chargement :", e)
        raise

    finally:
        conn.close()

# 5. (Etape 7 de l'ennoncé) Exposition des données via une API REST


# 6. Programme principal
def main():

    # Initialisation de la base de données
    init_database()

    # Appel des fonctions du pipeline ETL
    data = extract()
    data = transform(data)
    load(data)

    print("pipeline.py s'exécute correctement.")


if __name__ == "__main__":
    main()
