import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def generate_epg():
    # Cipta root element
    tv = ET.Element("tv", {
        "generator-info-name": "Custom Unifi EPG Generator",
        "source-info-name": "Unifi TV"
    })

    # Contoh penambahan Channel (Anda boleh tambah list penuh di sini)
    channels = [
        {"id": "UnifiTV101", "name": "TV1"},
        {"id": "UnifiTV102", "name": "TV2"},
    ]

    for ch in channels:
        channel_el = ET.SubElement(tv, "channel", id=ch["id"])
        ET.SubElement(channel_el, "display-name").text = ch["name"]

    # Contoh penambahan Program (Logik scrapping biasanya diletakkan di sini)
    # Ini sekadar placeholder agar fail tidak kosong
    prog = ET.SubElement(tv, "programme", {
        "start": datetime.now().strftime("%Y%m%d%H%M%S +0800"),
        "stop": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S +0800"),
        "channel": "UnifiTV101"
    })
    ET.SubElement(prog, "title").text = "Berita Semasa"
    ET.SubElement(prog, "desc").text = "Paparan berita terkini dari dalam dan luar negara."

    # Simpan fail
    tree = ET.ElementTree(tv)
    tree.write("unifi.xml", encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    generate_epg()
