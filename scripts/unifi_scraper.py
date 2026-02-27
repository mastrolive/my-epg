import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def generate_unifi_xml():
    # URL API yang anda berikan (Gunakan link yang ada userId anda)
    api_url = "https://user-catalog.api.tm.quickplay.com/catalog/user/content?tags=user_streaming_apps_collection,continue_watching,favorite,favorite_channel,my_channels&userId=25120207182870547&profileId=4618331&reg=my&dt=androidmobile&client=tm-unifitv-androidmobile"
    
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()

        # Root XML
        tv = ET.Element("tv", {"generator-info-name": "Gemini-Unifi-Quickplay"})

        # Cari content dalam 'my_channels' atau 'favorite_channel'
        for section in data.get("contents", []):
            # Kita fokus pada seksyen saluran sahaja
            if "channel" in section.get("title", "").lower() or "my_channels" in section.get("tags", ""):
                for item in section.get("contents", []):
                    ch_id = item.get("id")
                    ch_name = item.get("title")
                    # Ambil logo dari objek images
                    ch_logo = ""
                    if "images" in item:
                        # Biasanya logo ada dalam 'tile' atau 'brand'
                        ch_logo = item["images"].get("brand", {}).get("url", "")

                    # Cipta elemen <channel>
                    channel_el = ET.SubElement(tv, "channel", id=f"Unifi.{ch_id}")
                    ET.SubElement(channel_el, "display-name").text = ch_name
                    if ch_logo:
                        ET.SubElement(channel_el, "icon", src=ch_logo)

                    # Jana Programme dummy (Memandangkan API ini hanya untuk katalog)
                    # Jika anda ada API untuk EPG jadual, kita boleh gantikan di sini
                    now = datetime.now()
                    for i in range(3): # Jana 3 rancangan (6 jam total)
                        start = (now + timedelta(hours=i*2)).strftime("%Y%m%d%H0000 +0800")
                        stop = (now + timedelta(hours=(i+1)*2)).strftime("%Y%m%d%H0000 +0800")
                        
                        prog = ET.SubElement(tv, "programme", {
                            "start": start,
                            "stop": stop,
                            "channel": f"Unifi.{ch_id}"
                        })
                        ET.SubElement(prog, "title").text = f"Siaran Langsung {ch_name}"
                        ET.SubElement(prog, "desc").text = "Saksikan rancangan menarik di Unifi TV."

        # Simpan fail
        tree = ET.ElementTree(tv)
        ET.indent(tree, space="  ")
        tree.write("unifi.xml", encoding="UTF-8", xml_declaration=True)
        print("Fail unifi.xml berjaya dihasilkan!")

    except Exception as e:
        print(f"Ralat berlaku: {e}")

if __name__ == "__main__":
    generate_unifi_xml()
