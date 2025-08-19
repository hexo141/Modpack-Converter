import requests
import pathlib
import zipfile
import os
import concurrent.futures
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

search_pool = []
if not os.path.exists("temp"):
    os.makedirs("temp")

def search_mod(mod_name):
    session = requests.Session()
    retry = Retry(
        total=10,
        read=10,
        connect=10,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # 增加超时时间
    session.timeout = 20
    
    search = session.get(f"https://api.modrinth.com/v2/search?query={mod_name}",timeout=20,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"})
    return search
def loadpack(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            print(f"Extracting {filename} to temp")
            zip_ref.extract(filename, "temp")
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
    







