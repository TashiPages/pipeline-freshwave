import pandas as pd
import sqlite3
import requests

# 1. Extraction des données
def extract():
    print("Extraction des données...")
    pass


# 2. Transformation des données
def transform(data):
    print("Transformation des données...")
    pass


# 3. Chargement dans SQLite
def load(data):
    print("Chargement des données dans SQLite...")
    pass


# Programme principal
if __name__ == "__main__":
	data = extract()
	data = transform(data)
	load(data)
	print("pipeline.py s'éxecute correctement")
