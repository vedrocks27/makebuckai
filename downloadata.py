import zipfile
import requests
from io import BytesIO

# URL of the MovieLens latest small dataset
url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

# Send a request to the URL
response = requests.get(url)
content = BytesIO(response.content)

# Unzip the content
with zipfile.ZipFile(content, 'r') as zip_ref:
    zip_ref.extractall("movielens")

print("Download completed and files extracted.")
