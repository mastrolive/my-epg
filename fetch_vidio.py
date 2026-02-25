import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Konfigurasi Channel Vidio
# Anda bisa menambah slug sesuai URL di Vidio.com/live/
CHANNELS = [
    {"id": "sctv", "slug": "204-sctv", "name": "SCTV"},
    {"id": "indosiar", "slug": "205-indosiar", "name": "Indosiar"},
    {"id": "moji", "slug": "279-moji-tv", "name": "Moji"},
    {"id": "mentari", "slug": "8122-mentari-tv", "name": "Mentari TV"},
    {"id": "champions1", "slug": "6331-champions-tv-1", "name": "Champions TV 1"},
    {"id": "champions2", "slug": "6332-champions-tv-2", "name": "Champions TV 2"}
]

def generate_vidio_xml():
    root = ET.Element("tv")
    root.set("generator-info-name", "Otomatis-Vidio-EPG")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for ch in CHANNELS:
        # Tambahkan Info Channel ke XML
        c_node = ET.SubElement(root, "channel", id=ch['id'])
        ET.SubElement(c_node, "display-name").text = ch['name']

        # Scraping Jadwal
        url = f"https://www.vidio.com/live/{ch['slug']}/schedule"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.find_all('li', class_='schedule-item')

            for item in items:
                time_str = item.find('div', class_='schedule-item__time').text.strip()
                title = item.find('div', class_='schedule-item__title').text.strip()
                
                # Format Waktu XMLTV (Asumsi Hari Ini)
                now = datetime.now()
                start_dt = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %H:%M")
                stop_dt = start_dt + timedelta(hours=1.5) # Estimasi durasi 90 menit

                start_xml = start_dt.strftime("%Y%m%d%H%M%S +0700")
                stop_xml = stop_dt.strftime("%Y%m%d%H%M%S +0700")

                p_node = ET.SubElement(root, "programme", start=start_xml, stop=stop_xml, channel=ch['id'])
                ET.SubElement(p_node, "title").text = title
                ET.SubElement(p_node, "desc").text = f"Tayangan {title} di {ch['name']}"
        
        except:
            print(f"Gagal mengambil data {ch['name']}")

    # Simpan Hasil ke File
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("vidio.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_vidio_xml()
