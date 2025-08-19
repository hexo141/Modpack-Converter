import requests
import pathlib
import zipfile
import os
import concurrent.futures
search_pool = []
if not os.path.exists("temp"):
    os.makedirs("temp")
def loadpack(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("temp")
    mods_path = pathlib.Path("temp") / "overrides" /"mods"
    for mod in mods_path.iterdir():
        search = requests.get(f"https://api.modrinth.com/v2/search?query={mod}",timeout=20)
        search_pool.append(search)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(loadpack, search_pool)
    for search in search_pool:
        print(search.json())
    







