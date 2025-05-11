# Neverin.hr Weather Metrics Scraper & Visualization

## Overview

This project is designed to scrape weather metrics from the [Neverin.hr](https://www.neverin.hr) website, store the collected data into an InfluxDB time-series database, and visualize the metrics using Grafana dashboards.

The system consists of three main components:
1.  **Weather Scraper**: A Python script (assumption, to be detailed by user) responsible for fetching data from Neverin.hr.
2.  **InfluxDB**: A time-series database used to store the scraped weather metrics efficiently.
3.  **Grafana**: A visualization platform used to create dashboards and graphs from the data stored in InfluxDB.

These components (InfluxDB and Grafana) are orchestrated using Docker and Docker Compose for easy setup and deployment.

## Features

* Automated scraping of weather data from Neverin.hr.
* Storage of time-series weather data in InfluxDB.
* Visualization of weather metrics through Grafana.
* Easy deployment of InfluxDB and Grafana using Docker Compose.
* Persistent data storage for both InfluxDB and Grafana.

## Prerequisites

* **Docker**: Ensure Docker is installed on your system. ([Get Docker](https://docs.docker.com/get-docker/))
* **Docker Compose**: Ensure Docker Compose is installed. (It's usually included with Docker Desktop for Windows and Mac. For Linux, you might need to install it separately: [Install Docker Compose](https://docs.docker.com/compose/install/))
* **Python 3.x**: For running the scraper script (e.g., Python 3.8+).
* **Git**: For cloning the project repository (if applicable).