#!/usr/bin/env python3
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from influxdb_client import InfluxDBClient, Point, WritePrecision

# ─── Configuration ────────────────────────────────────────────────────────────
URL           = "https://www.neverin.hr/postaja/zagreb-vukomerec/"
INFLUX_URL    = "http://localhost:8086"
INFLUX_TOKEN  = "JL0GI-GlbIrMaFNkBqr04y4bOVPlgQ0CI4T-0CtEBf26Mu7P30-JJWqxnUVr_knFCXwrZZ2wvR0IDjdjhM6ZpQ=="
INFLUX_ORG    = "cloudworks"
INFLUX_BUCKET = "weather"

# ─── Label → field map ────────────────────────────────────────────────────────
LABEL_MAP = {
    "Temperatura zraka":             "air_temperature",
    "Trend temperature":             "temp_trend",
    "Osjet vjetra":                  "real_feel",
    "Točka rosišta":                 "dew_point",
    "Relativna vlažnost":            "relative_humidity",
    "Tlak zraka":                    "pressure",
    "Brzina vjetra":                 "wind_speed",
    "Udari vjetra":                  "wind_gusts",
    "Smjer vjetra":                  "wind_direction",
    "Oborine u posljednjih 1 sat":  "precip_1h",
    "Oborine u posljednja 24 sata": "precip_24h",
    "UV indeks":                     "uv_index",
    "Sunčevo zračenje":              "sun_iradiation",
}

# ─── InfluxDB client ──────────────────────────────────────────────────────────
client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_precision=WritePrecision.S)

# ─── Selenium setup ────────────────────────────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium-browser"

service = Service(executable_path="/usr/bin/chromedriver")
driver  = webdriver.Chrome(service=service, options=options)


def scrape_and_write():
    driver.get(URL)
    time.sleep(10)  # wait for JS to inject everything

    soup = BeautifulSoup(driver.page_source, "html.parser")
    fields = {}

    for label_text, field_name in LABEL_MAP.items():
        # match the label, stripping any trailing colon
        el = soup.find(
            string=lambda s: s
            and s.strip().rstrip(":") == label_text
        )
        if not el:
            continue


        raw_text = el.find_next().get_text(strip=True)

        # pull out the first number
        m = re.search(r"[-+]?\d+(?:[.,]\d+)?", raw_text)
        if not m:
            continue

        try:
            val = float(m.group().replace(",", "."))
        except ValueError:
            continue

        fields[field_name] = val

    if not fields:
        print("⚠️  No data parsed—skipping Influx write")
        return

    pt = Point("zagreb_vukomerec").tag("station", "zagreb_vukomerec")
    for k, v in fields.items():
        pt = pt.field(k, v)

    write_api.write(bucket=INFLUX_BUCKET, record=pt)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Wrote: {fields}")


if __name__ == "__main__":
    try:
        while True:
            scrape_and_write()
            time.sleep(600)  # 10 minutes
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        driver.quit()
