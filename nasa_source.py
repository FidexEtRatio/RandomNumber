import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

def get_current_sun_data():
    # resolutions preffered: 4096, 2048
    # analysis codes available: HMI171, 0131, 211193171n, 0171

    # list of filters
    analysis_code = ["HMI171", "0131", "211193171n", "0171"]
    resolutions = ["4096_", "2048_"]

    # directory to save
    dir_name = "images"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # current date
    date = datetime.now(timezone.utc)

    found_imgs = {}

    days_searched = 0
    while len(found_imgs) < 4 and days_searched <= 5: # search 4 images and up until 5 days ago
        #format date
        date_f = date.strftime("%Y/%m/%d")

        # root url
        url = f"https://sdo.gsfc.nasa.gov/assets/img/browse/{date_f}/"
        print(f"Checking root url: {url}...")

        #fetch webpage
        response = requests.get(url)

        if response.status_code == 200:
           # parse webpage
            soup = BeautifulSoup(response.text, "html.parser")

            # sort images by hour to find only the latest ones
            available_imgs = sorted(
                (a["href"] for a in soup.find_all("a") if a["href"].endswith(".jpg")),
                key=lambda img: img.split("_")[1],
                reverse=True
            )

            #filter images
            matching_imgs = {}
            for res in resolutions:
                for code in analysis_code:
                    image_name = next((img for img in available_imgs if img.endswith(f"{res}{code}.jpg")), None)
                    if image_name:
                        matching_imgs[code] = image_name
                        print(f"Found {image_name} for code {code}...")
                        if len(matching_imgs) == 4:
                            break
                if len(matching_imgs) == 4:
                    break
            found_imgs.update(matching_imgs)


        # if the script was not able to find 4 imgs we go a day before
        if len(found_imgs) < 4:
            date -= timedelta(days=1)
            days_searched += 1
        else:
            break # stop when having all the imgs

    success = True

    for code, img_name in found_imgs.items():
        img_url = url + img_name
        saving_path = os.path.join(dir_name, img_name)

        # download and save img
        img_resp = requests.get(img_url)
        if img_resp.status_code == 200:
            with open(saving_path, "wb") as file:
                file.write(img_resp.content)
            print(f"Downloaded {img_name} to {saving_path}...")
        else:
            print(f"Failed to download {img_name}")
            success = False

    if success:
        print("Data fetched successfully...")
    else:
        print("Error in fetching all data!")
    
    return success