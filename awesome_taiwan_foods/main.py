import time
import requests


def fetch_tasting_ids():
    api_url = "https://bo.taste-institute.com/rails/web/tastings/ids"
    data = {
        "awards": None,
        "mother_categories": None,
        "sta_years": [2023, 2022, 2021],
        "q": None,
    }

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

        return []


def fetch_tasting_details(ids):
    api_url = "https://bo.taste-institute.com/rails/web/tastings"
    data = {"ids": ids}
    response = requests.post(api_url, json=data)

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()

        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

        return []


def filter_taiwan_products(products):
    return [product for product in products if product.get("country") == "TAIWAN"]


def main():
    tasting_ids = fetch_tasting_ids()
    batch_size = 15
    taiwan_products = []

    for i in range(0, len(tasting_ids), batch_size):
        batch_ids = tasting_ids[i : i + batch_size]
        product_details = fetch_tasting_details(batch_ids)
        taiwan_products += filter_taiwan_products(product_details)
        time.sleep(1)

    for product in taiwan_products:
        print(product)


if __name__ == "__main__":
    main()
