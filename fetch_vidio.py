import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import os

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
    root.set("generator-info-name", "Vidio-EPG-Generator")

    # Header lengkap agar tidak terdeteksi sebagai bot basic
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Origin": "https://www.vidio.com",
        "Referer": "https://www.vidio.com/",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    for ch in CHANNELS:
        # Tambah info channel
        c_node = ET.SubElement(root, "channel", id=ch['id'])
        ET.SubElement(c_node, "display-name").text = ch['name']

        # Ambil jadwal hari ini
        date_now = datetime.now().strftime("%Y-%m-%d")
        # Menggunakan endpoint API yang lebih stabil
        api_url = f"https://www.vidio.com/live/{ch['vidio_id']}/schedules?date={date_now}"
        
        try:
            print(f"Mengambil data untuk {ch['name']}...")
            response = requests.get(api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                schedules = data.get("schedules", [])
                
                if not schedules:
                    print(f"Data kosong untuk {ch['name']}")
                
                for prog in schedules:
                    title = prog.get("title", "No Title")
                    # Format asal: 2024-05-20T18:00:00.000+07:00
                    start_raw = prog.get("start_time")
                    end_raw = prog.get("end_time")
                    
                    if start_raw and end_raw:
                        # Membersihkan format waktu untuk XMLTV
                        start_xml = start_raw.replace("-", "").replace(":", "").replace(".000", "").replace("T", "")
                        end_xml = end_raw.replace("-", "").replace(":", "").replace(".000", "").replace("T", "")

                        p_node = ET.SubElement(root, "programme", 
                                              start=start_xml, 
                                              stop=end_xml, 
                                              channel=ch['id'])
                        ET.SubElement(p_node, "title", lang="id").text = title
                        ET.SubElement(p_node, "desc", lang="id").text = f"Program {title} di {ch['name']}"
            else:
                print(f"Error {response.status_code} pada channel {ch['name']}")

        except Exception as e:
            print(f"Gagal mengambil data {ch['name']}: {e}")

    # Simpan ke file vidio.xml
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("vidio.xml", encoding="utf-8", xml_declaration=True)
    print("Selesai! File vidio.xml telah diperbarui.")

if __name__ == "__main__":
    get_epg()
