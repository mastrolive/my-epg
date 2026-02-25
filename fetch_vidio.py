import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# Daftar Channel sesuai ID di Vidio
CHANNELS = [
    {"id": "sctv", "vidio_id": "204", "name": "SCTV"},
    {"id": "indosiar", "vidio_id": "205", "name": "Indosiar"},
    {"id": "moji", "vidio_id": "279", "name": "Moji"},
    {"id": "mentari", "vidio_id": "8122", "name": "Mentari TV"},
    {"id": "champions1", "vidio_id": "6331", "name": "Champions TV 1"},
    {"id": "champions2", "vidio_id": "6332", "name": "Champions TV 2"}
]

def get_epg():
    root = ET.Element("tv")
    root.set("generator-info-name", "Otomatis-Vidio-EPG")

    # Header agar tidak diblokir
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.vidio.com/"
    }

    for ch in CHANNELS:
        # 1. Tambah Info Channel
        c_node = ET.SubElement(root, "channel", id=ch['id'])
        ET.SubElement(c_node, "display-name").text = ch['name']

        # 2. Ambil Data dari API Jadwal Vidio
        # Mengambil jadwal untuk hari ini
        today = datetime.now().strftime("%Y-%m-%d")
        api_url = f"https://www.vidio.com/live/{ch['vidio_id']}/schedules?date={today}"
        
        try:
            print(f"Mengambil jadwal: {ch['name']}")
            response = requests.get(api_url, headers=headers, timeout=10)
            data = response.json()

            # Pastikan ada data jadwal
            if "schedules" in data:
                for prog in data["schedules"]:
                    title = prog.get("title", "No Title")
                    start_str = prog.get("start_time") # Format: "2024-05-20T18:00:00.000+07:00"
                    end_str = prog.get("end_time")
                    
                    if start_str and end_str:
                        # Konversi format waktu ke XMLTV (YYYYMMDDHHMMSS +0700)
                        # Kita bersihkan formatnya agar standar
                        start_xml = start_str.replace("-", "").replace(":", "").replace(".000", "").replace("T", "")
                        end_xml = end_str.replace("-", "").replace(":", "").replace(".000", "").replace("T", "")

                        p_node = ET.SubElement(root, "programme", 
                                              start=start_xml, 
                                              stop=end_xml, 
                                              channel=ch['id'])
                        ET.SubElement(p_node, "title").text = title
                        ET.SubElement(p_node, "desc").text = f"Tayangan {title} di {ch['name']}"

        except Exception as e:
            print(f"Gagal di {ch['name']}: {e}")

    # Simpan file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("vidio.xml", encoding="utf-8", xml_declaration=True)
    print("Selesai! File vidio.xml telah diupdate dengan jadwal.")

if __name__ == "__main__":
    get_epg()
