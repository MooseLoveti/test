import sys
import requests
import os
import time
from datetime import datetime
args = sys.argv

count_min = int(args[1])
count_max = int(args[2])
last_update = int(args[3])

#search.py 1000 3000 12としたら「インストール数1000~3000 最終更新日12か月(1年前)のプラグインを総ダウンロードしたい

api_url = "https://api.wordpress.org/plugins/info/1.2/"
page = 1

#保存先ディレクトリ
save_dir = os.path.join(os.path.dirname(__file__), "plugin")
os.makedirs(save_dir, exist_ok=True)

while True:
    payload = {
        "action": "query_plugins",
        "request[per_page]" : 100,
        "request[page]" : page,
        "request[fields][active_installs]": True,
        "request[fields][last_updated]" : True
    }
    r = requests.get(api_url,params=payload)
    data = r.json()

    if not data.get("plugins"):
        break
    
    for plugin in data["plugins"]:
        installs = plugin.get("active_installs",0)
        updated = plugin.get("last_updated", "")
        dt = datetime.strptime(updated, "%Y-%m-%d %I:%M%p GMT")
        diff_month = (time.gmtime().tm_year - dt.year) * 12 + (time.gmtime().tm_mon - dt.month)

        if count_min <= installs <= count_max and last_update <= diff_month:
            #ZIPの保存を行う
            filename = plugin.get("download_link", "")
            if not filename:
                continue
            slug = plugin.get("slug", "hogehoge")
            file_path = os.path.join(save_dir,f"{slug}.zip")
            resp = requests.get(filename, stream=True)
            with open(file_path,"wb") as f:
                f.write(resp.content)
    page += 1


