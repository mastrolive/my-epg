import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# Daftar Channel Astro (ID sesuai Content API Astro)
CHANNELS = [
    {"id": "astro-ria", "stb": "104", "name": "Astro Ria"},
    {"id": "astro-prima", "stb": "105", "name": "Astro Prima"},
    {"id": "astro-aec", "stb": "306", "name": "Astro AEC"},
    {"id": "astro-ceria", "stb": "611", "name": "Astro Ceria"},
    {"id": "astro-arena", "stb": "801", "name": "Astro Arena"},
    {"id": "astro-arena-2", "stb": "802", "name": "Astro Arena 2"},
    {"id": "supersport-1", "stb": "811", "name": "Astro SuperSport 1"},
    {"id": "supersport-2", "stb": "812", "name": "Astro SuperSport 2"},
    {"id": "supersport-3", "stb": "813", "name": "Astro SuperSport 3"},
    {"id": "supersport-4", "stb": "814", "name": "Astro SuperSport 4"},
    {"id": "premier-league-1", "stb": "821", "name": "Astro Premier League 1"},
    {"id": "premier-league-2", "stb": "822", "name": "Astro Premier League 2"},
    {"id": "beinsports-1", "stb": "818", "name": "beIN SPORTS 1"},
    {"id": "beinsports-2", "stb": "819", "name": "beIN SPORTS 2"},
    {"id": "beinsports-3", "stb": "820", "name": "beIN SPORTS 3"},
    {"id": "spotv", "stb": "816", "name": "SPOTV"},
    {"id": "spotv2", "stb": "817", "name": "SPOTV 2"}
]

def get_astro_epg():
    root = ET.Element("tv")
    root.set("generator-info-name", "Astro-EPG-Generator")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://content.astro.com.my/"
    }

    for ch in CHANNELS:
        # Tambah Channel Info
        c_node = ET.SubElement(root, "channel", id=ch['id'])
        ET.SubElement(c_node, "display-name").text = ch['name']

        # API Astro (v2)
        api_url = f"https://contentapi.astro.com.my/v2/channel/{ch['stb']}/schedules"
        
        try:
            print(f"Scraping {ch['name']}...")
            response = requests.get(api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                schedules = data.get("response", {}).get("schedules", [])

                for prog in schedules:
                    title = prog.get("title")
                    start_raw = prog.get("datetime") # Format: 2024-05-20 18:00:00.0
                    duration = prog.get("duration") # Format: 01:00:00

                    if start_raw and duration:
                        # Parse start time
                        start_dt = datetime.strptime(start_raw.split('.')[0], "%Y-%m-%d %H:%M:%S")
                        
                        # Hitung stop time
                        h, m, s = map(int, duration.split(':'))
                        stop_dt = start_dt + timedelta(hours=h, minutes=m, seconds=s)

                        # Format XMLTV (+0800 Malaysia)
                        start_xml = start_dt.strftime("%Y%m%d%H%M%S +0800")
                        stop_xml = stop_dt.strftime("%Y%m%d%H%M%S +0800")

                        p_node = ET.SubElement(root, "programme", start=start_xml, stop=stop_xml, channel=ch['id'])
                        ET.SubElement(p_node, "title", lang="ms").text = title
                        
                        desc = prog.get("shortSynopsis") or prog.get("longSynopsis")
                        if desc:
                            ET.SubElement(p_node, "desc", lang="ms").text = desc
                            
                        # Tambah Kategori (Sports, Movie, dsb)
                        genre = prog.get("genre")
                        if genre:
                            ET.SubElement(p_node, "category", lang="en").text = genre

        except Exception as e:
            print(f"Error pada {ch['name']}: {e}")

    # Simpan hasil sebagai astro.xml
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("astro.xml", encoding="utf-8", xml_declaration=True)
    print("Selesai! astro.xml berhasil dibuat.")

if __name__ == "__main__":
    get_astro_epg()
