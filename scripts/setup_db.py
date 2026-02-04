import requests
import zipfile
from pathlib import Path
import io
import csv
import sqlite3

GEONAMES_URL = "https://download.geonames.org/export/dump/cities15000.zip"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "geodata.db"

def download_data():
    try :
        response = requests.get(GEONAMES_URL)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(DATA_DIR)
        print("Data downloaded and extracted successfully")

    except :
        print("Error")


def populate_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS locations (name TEXT, lat REAL, lon REAL, country TEXT)")
    with open(DATA_DIR / "cities15000.txt", mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader :
            name, lat, lon, country = row[1], float(row[4]), float(row[5]), row[8]
            cursor.execute("INSERT INTO locations (name, lat, lon, country) VALUES (?, ?, ?, ?)", (name, lat, lon, country))
    connection.commit()
    connection.close()
    print("Database populated successfully!")


if __name__ == "__main__":
    if not (DATA_DIR / "cities15000.txt").exists():
        download_data()
    if not DB_PATH.exists() :
        populate_db()
