"""Collect one snapshot of all Encicla stations and append it to a CSV.

Long format: one row per station per reading. All rows of a reading share
the same UTC timestamp (taken just before the request).
"""

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = (
    "https://webapp.metropol.gov.co/wsencicla/api/Disponibilidad/GetDisponibilidadMapas"
)
DEFAULT_OUTPUT = Path("data/snapshots.csv")
TIMEOUT_SECONDS = 30
# The API returns 403 for the default python-requests User-Agent.
HEADERS = {"User-Agent": "encicla-analytics/1.0 (portfolio project)"}

FIELDS = [
    "timestamp_utc",
    "zone_id",
    "zone_name",
    "station_id",
    "station_name",
    "address",
    "lat",
    "lon",
    "type",
    "capacity",
    "bikes",
    "places",
    "closed",
]


def fetch_stations():
    response = requests.get(API_URL, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or not data:
        raise ValueError("Unexpected API response: expected a non-empty list")
    return data


def clean(value):
    """Strip whitespace and the stray \r\n the API appends to text fields."""
    return value.strip() if isinstance(value, str) else value


def to_row(station, timestamp):
    return {
        "timestamp_utc": timestamp,
        "zone_id": station.get("idZona"),
        "zone_name": clean(station.get("nameZona")),
        "station_id": station.get("id"),
        "station_name": clean(station.get("name")),
        "address": clean(station.get("address")),
        "lat": station.get("lat"),
        "lon": station.get("lon"),
        "type": clean(station.get("type")),
        "capacity": station.get("capacity"),
        "bikes": station.get("bikes"),
        "places": station.get("places"),
        "closed": station.get("closed"),
    }


def append_rows(rows, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    write_header = not output.exists() or output.stat().st_size == 0
    with output.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stations = fetch_stations()
    rows = [to_row(s, timestamp) for s in stations]
    append_rows(rows, args.output)
    print(f"{timestamp}: wrote {len(rows)} stations to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ValueError) as exc:
        print(f"Collection failed: {exc}", file=sys.stderr)
        sys.exit(1)
