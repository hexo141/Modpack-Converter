import requests
import pathlib
import zipfile
import os
import concurrent.futures
search_pool = []
if not os.path.exists("temp"):
    os.makedirs("temp")

def search_mod(mod_name):
    search = requests.get(f"https://api.modrinth.com/v2/search?query={mod_name}",timeout=20,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"})
    return search
def loadpack(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("temp")
    mods_path = pathlib.Path("temp") / "overrides" /"mods"
    mod_names = []
    for mod in mods_path.iterdir():
        print(f"Adding {mod} to search pool")
        # 提取mod名称
        mod_name = mod.name.split(".")[0]
        mod_names.append(mod_name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(search_mod, mod_names)
    for search in results:
        print(search.json())
    







