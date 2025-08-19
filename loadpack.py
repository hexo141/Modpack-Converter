import requests
import pathlib
import zipfile
import os
import concurrent.futures
response = requests.get("https://api.modrinth.com/",timeout=20)
search_pool = []
if not os.path.exists("temp"):
    os.makedirs("temp")
def loadpack(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(pathlib.Path("temp") / path)
    mods_path = pathlib.Path("temp") / path / "overrides"/"mods"
    for mod in mods_path.iterdir():
        search = requests.get(f"https://api.modrinth.com/v2/search?query={mod}")
        search_pool.append(search)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(loadpack, search_pool)
    for search in search_pool:
        print(search.json())
    







