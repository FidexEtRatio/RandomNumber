import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# resolutions preffered: 4096, 2048
# analysis codes available: 0335, 0094, 0131, 0171

# list of filters
analysis_code = ["0335", "0094", "0131", "0171"]
resolutions = ["4096_", "2048_"]

# directory to save
dir_name = "images"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# current date
date = datetime.now(timezone.utc)

found_imgs = {}

while len(found_imgs) < 4:
    #format date
    date_f = date.strftime("%Y/%m/%d")

    # root url
    url = f"https://sdo.gsfc.nasa.gov/assets/img/browse/{date_f}/"
    print(f"Checking root url: {url}\n")

    #fetch webpage
    response = requests.get(url)

    if response.status_code == 200:
       # parse webpage
        soup = BeautifulSoup(response.text, "html.parser")
        available_imgs = {a["href"] for a in soup.find_all("a") if a["href"].endswith(".jpg")}

        #filter images
        matching_imgs = {}
        for res in resolutions:
            for code in analysis_code:
                image_name = next((img for img in available_imgs if img.endswith(f"{res}{code}.jpg")), None)
                if image_name:
                    matching_imgs[code] = image_name
                    print(f"Found {image_name} for code {code}\n")
                    if len(matching_imgs) == 4:
                        break
        found_imgs.update(matching_imgs)

    
    # if the script was not able to find 4 imgs we go a day before
    if len(found_imgs) < 4:
        date -= timedelta(days=1)
    else:
        break # stop when having all the imgs

for code, img_name in found_imgs.items():
    img_url = url + img_name
    saving_path = os.path.join(dir_name, img_name)

    # download and save img
    img_resp = requests.get(img_url)
    if img_resp.status_code == 200:
        with open(saving_path, "wb") as file:
            file.write(img_resp.content)
        print(f"Downloaded {img_name} to {saving_path}\n")
    else:
        print(f"Failed to download {img_name}\n")

print("Data fetched successfully!")