# HotStreak Sports Scraper

This project scrapes **basketball (NBA)**, **baseball (MLB)**, and **football (NFL)** match data from the [HotStreak](https://hs3.hotstreak.gg/) platform using its **GraphQL API**.

---

## Folder Structure
- `config/` → Configuration files (`config.yml`)
- `src/` → Core code (classes, connectors, connections)
- `data/` → Logs and extracted JSON output

---

## Setup Instructions

```bash
pip install -r requirements.txt
python -m playwright install
python main.py
