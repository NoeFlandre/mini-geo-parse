import requests
import zipfile
from pathlib import Path
import io

GEONAMES_URL = "https://download.geonames.org/export/dump/cities15000.zip"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

try :
    response = requests.get(GEONAMES_URL)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(DATA_DIR)
    print("Data downloaded and extracted successfully")

except :
    print("Error")