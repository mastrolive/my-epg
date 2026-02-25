import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import re

# Daftar Channel (Slug URL Vidio)
# Format: {"id_xmltv": "slug-vidio", "name": "Nama Channel"}
CHANNELS = [
    {"id": "sctv", "slug": "204-sctv", "name": "SCTV"},
    {"id": "indosiar", "slug": "205-indosiar", "name": "Indosiar"},
    {"id": "moji", "slug": "279-moji-tv", "name": "Moji"},
    {"id": "mentari", "slug": "8122-mentari-tv", "name": "Mentari TV"},
    {"id": "v-premier", "slug": "6331-vidio-premier", "name": "Vidio Premier"}
]

def format_xml_time(dt_obj):
    return dt_obj.strftime("%Y%m%d%H%M%S +0700")

def get_epg():
    root = ET.Element("tv")
    root.set("generator-info-name", "Vidio-Scraper-EPG")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for ch in CHANNELS:
        # 1. Tambah Definisi Channel
        c_elem = ET.SubElement(root, "channel", id=ch['id'])
        ET.SubElement(c_elem, "display-name").text = ch['name']

        # 2. Scraping Jadwal
        url = f"https://www.vidio.com/live/{ch['slug']}/schedule"
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mencari elemen jadwal (biasanya dalam class schedule-item)
            items = soup.find_all('li', class_='schedule-item') 
            
            for item in items:
                time_str = item.find('div', class_='schedule-item__time').text.strip() # Contoh "18:00"
                title = item.find('div', class_='schedule-item__title').text.strip()
                
                # Logika Waktu (Sederhana: Hari Ini)
                now = datetime.now()
                start_dt = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %H:%M")
                
                # Asumsi durasi 1 jam jika tidak ada waktu selesai (Bisa diimprove)
                stop_dt = start_dt + timedelta(hours=1)

                p_elem = ET.SubElement(root, "programme", 
                                      start=format_xml_time(start_dt), 
                                      stop=format_xml_time(stop_dt), 
                                      channel=ch['id'])
                ET.SubElement(p_elem, "title").text = title
                ET.SubElement(p_elem, "desc").text = f"Tayangan {title} di {ch['name']}"

        except Exception as e:
            print(f"Error scraping {ch['name']}: {e}")

    # Simpan ke file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # Agar XML rapi
    tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_epg()
