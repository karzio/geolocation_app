
# GEOLOCATION API

## Description

GeoLocation REST API that allows you to get the geolocation of a given IP address or a URL. The API is built using Django and uses the IP Stack API to get the geolocation data.

## Installation

Use docker for a quick set up.
Before running the docker commands, copy the `.env.example` file to `.env` and fill in the IP Stack API key.

```bash
IP_STACK_API_KEY=your_api_key
```

Then run the following commands:

```bash
docker compose build
docker compose up
```

The API will be available at `http://localhost:8000/`.

For API with UI, head to `http://localhost:8000/docs/`.

## Usage

The GeoLocation model holds data for a web address and this data consists of: latitude, longitude, country, city, and zip code.

The API has 4 endpoints:

1. GET `/geolocation/` - List the IDs' and web addresses' of all the geolocations.
2. GET `/geolocation/{id}/` - Get the details of a geolocation data of a specific ID.
3. DELETE `/geolocation/{id}/` - Delete the geolocation data of a specific ID.
4. POST `/geolocation/` - Create a new geolocation data by providing a web address.

This demo is populated with a small fixture of test data found in test_data.json.

## Features

Based on the above list of endpoints, the app can list all web addresses, show details of a web address, delete web address from the database and add new address.

Additionally, when adding new address, it is being validated with Django URL Validator. Also, the app does not allow duplicated web addresses in the database.
The duplicates are checked based on a normalized web address. Normalization removes protocol prefix and eventually "www." part. 

