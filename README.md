<div align="center">

<!-- ANIMATED HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0f172a,1e293b,0284c7,2563eb&height=200&section=header&text=EPG&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%" alt="EPG Hub Banner" />

<br/>

# 📺 EPG Data

### *High-availability Electronic Program Guide (EPG) distribution engine & automated TV schedule provider.*

<p align="center">
  <a href="#-epg-data-feed-urls"><img src="https://img.shields.io/badge/Data%20Feed-XMLTV-7B2CBF?style=for-the-badge&logo=xml&logoColor=white" alt="Data Feed" /></a>
  <a href="#-epg-data-feed-urls"><img src="https://img.shields.io/badge/Delivery-Global%20CDN-00F5D4?style=for-the-badge&logo=cloudflare&logoColor=black" alt="CDN" /></a>
  <a href="#-automation--schedule"><img src="https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="Automation" /></a>
  <a href="#-epg-data-feed-urls"><img src="https://img.shields.io/badge/Status-Live%20Sync-00C853?style=for-the-badge&logo=statuspage&logoColor=white" alt="Status" /></a>
</p>

<!-- DYNAMIC STATUS & METRICS BADGES -->
<p align="center">
  <a href="https://github.com/mastrolive/my-epg/actions"><img src="https://img.shields.io/github/actions/workflow/status/mastrolive/my-epg/epg.yml?branch=main&style=for-the-badge&label=AUTO%20SYNC%20STATUS&logo=githubactions&logoColor=white&color=00f5d4" alt="Auto Sync Status" /></a>
  <img src="https://img.shields.io/badge/FORMAT-XMLTV%20COMPLIANT-FF6F00?style=for-the-badge&logo=rss&logoColor=white" alt="XMLTV Compliant" />
  <img src="https://img.shields.io/github/last-commit/mastrolive/my-epg?style=for-the-badge&label=LAST%20UPDATE&color=2563eb&logo=git&logoColor=white" alt="Last Commit" />
</p>

</div>

<br/>

---

## 📌 Overview

Welcome to the **my-epg** data vault. This repository functions as an automated pipeline for fetching, filtering, generating, and serving XMLTV-compliant Electronic Program Guide (EPG) schedules for TV streaming applications and IPTV players.

---

## ⚡ EPG Data Feed URLs

Access live EPG feeds directly via ultra-fast global CDN edge servers:

### 🌐 Direct CDN & Raw Links

| Feed Name | Direct Edge CDN URL | Raw GitHub URL |
| :--- | :--- | :--- |
| **`epg.xml`** | `https://cdn.jsdelivr.net/gh/mastrolive/my-epg@main/epg.xml` | `https://raw.githubusercontent.com/mastrolive/my-epg/main/epg.xml` |
| **`epg2.xml`** | `https://cdn.jsdelivr.net/gh/mastrolive/my-epg@main/epg2.xml` | `https://raw.githubusercontent.com/mastrolive/my-epg/main/epg2.xml` |
| **`my.xml`** | `https://cdn.jsdelivr.net/gh/mastrolive/my-epg@main/my.xml` | `https://raw.githubusercontent.com/mastrolive/my-epg/main/my.xml` |
| **`id.xml`** | `https://cdn.jsdelivr.net/gh/mastrolive/my-epg@main/id.xml` | `https://raw.githubusercontent.com/mastrolive/my-epg/main/id.xml` |
| **`utv.xml`** | `https://cdn.jsdelivr.net/gh/mastrolive/my-epg@main/utv.xml` | `https://raw.githubusercontent.com/mastrolive/my-epg/main/utv.xml` |

---

## 🔄 Automation & Schedule

This repository utilizes **GitHub Actions** workflows to automatically parse, sync, and update TV guide data on a daily schedule, ensuring zero manual intervention and accurate program timings.

```text
 ⚙️ AUTOMATION PIPELINE
 ├── 🛰️ Fetch Source Guides   ──► Ingest EPG Data Sources
 ├── 🧹 Filter & Format        ──► Time-Offset & XMLTV Standardization
 └── 🚀 Auto Commit & Push     ──► epg.xml / epg2.xml / my.xml / id.xml / utv.xml
