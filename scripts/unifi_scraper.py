import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def generate_epg():
    # URL API yang anda berikan
    url = "https://user-catalog.api.tm.quickplay.com/catalog/user/content?tags=user_streaming_apps_collection,continue_watching,favorite,favorite_channel,because_you_watched_1,because_you_watched_2,because_you_watched_3,trending_now_movies,trending_now_shows,trending_now,my_channels,recommended_for_you,because_you_liked_1,because_you_liked_2,because_you_liked_3&userId=25120207182870547&profileId=4618331&timestamp=1772186186830&reg=my&dt=androidmobile&client=tm-unifitv-androidmobile&pf=Regular&ml=18&seg=Cohort3"

    headers = {
        "User-Agent": "tm-unifitv-androidmobile/1.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        tv = ET.Element("tv", {"generator-info-name": "Unifi-Quickplay-Scraper"})

        # Cari bahagian 'my_channels' atau 'favorite_channel' dalam JSON
        # Kita buat loop untuk extract channel
        for section in data.get('contents', []):
            if section.get('title') in ['My Channels', 'Favorite Channels', 'Trending Now']:
                for item in section.get('contents', []):
                    ch_id = item.get('id')
                    ch_name = item.get('title')
                    ch_icon = item.get('images', {}).get('logo', {}).get('url')

                    # Buat tag <channel>
                    channel_node = ET.SubElement(tv, "channel", id=f"Unifi.{ch_id}")
                    ET.SubElement(channel_node, "display-name").text = ch_name
                    if ch_icon:
                        ET.SubElement(channel_node, "icon", src=ch_icon)

                    # Buat dummy <programme> (Atau tarik jadual sebenar jika ada dalam JSON)
                    now = datetime.now()
                    start = now.strftime("%Y%m%d%H0000 +0800")
                    stop = (now + timedelta(hours=2)).strftime("%Y%m%d%H0000 +0800")

                    prog = ET.SubElement(tv, "programme", {
                        "start": start,
                        "stop": stop,
                        "channel": f"Unifi.{ch_id}"
                    })
                    ET.SubElement(prog, "title").text = f"Live: {ch_name}"
                    ET.SubElement(prog, "desc").text = "Saksikan siaran langsung di Unifi TV."

        # Simpan fail
        tree = ET.ElementTree(tv)
        ET.indent(tree, space="  ")
        tree.write("unifi.xml", encoding="UTF-8", xml_declaration=True)
        print("Fail unifi.xml berjaya dijana!")

    except Exception as e:
        print(f"Ralat: {e}")

if __name__ == "__main__":
    generate_epg()
