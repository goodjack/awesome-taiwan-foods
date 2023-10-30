from operator import itemgetter
from time import sleep
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

        ids = response.json()

        return sorted(ids, reverse=True)
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


def generate_markdown_table(products, title: str):
    table = f"\n## {title}\n\n"
    table += "| 產品圖 | 產品 | 公司名稱 | 得獎年份 |\n"
    table += "| --- | --- | --- | --- |\n"
    for product in products:
        image_url = product.get("packshot", {}).get("url")
        if image_url:
            image_tag = f'<img width="75px" src="https://assets.taste-institute.com{image_url}">'
        else:
            image_tag = None

        table += f"| {image_tag} | [{product['productName']}](https://www.taste-institute.com/ct/awarded-products/product-details/{product['tastingId']}) | {product['companyName']} | {product['staYear']} |\n"
    return table


def write_to_readme(taiwan_products: list):
    taiwan_products.sort(key=itemgetter("staYear", "tastingId"), reverse=True)
    three_star = [product for product in taiwan_products if product["stars"] == 3]
    two_star = [product for product in taiwan_products if product["stars"] == 2]
    one_star = [product for product in taiwan_products if product["stars"] == 1]

    with open("README.md", "w", encoding="utf-8") as readme:
        readme.write(
            "# Awesome Taiwan Foods 台灣獲獎食品\n目前包含 International Taste Institute 獲獎食品\n"
        )
        readme.write(generate_markdown_table(three_star, "ITI 最佳風味獎 三星 ⭐️⭐️⭐️"))
        readme.write(generate_markdown_table(two_star, "ITI 最佳風味獎 二星 ⭐️⭐️"))
        readme.write(generate_markdown_table(one_star, "ITI 最佳風味獎 一星 ⭐️"))


def main():
    tasting_ids = fetch_tasting_ids()
    batch_size = 15
    taiwan_products = []

    for i in range(0, len(tasting_ids), batch_size):
        batch_ids = tasting_ids[i : i + batch_size]
        product_details = fetch_tasting_details(batch_ids)
        taiwan_products += filter_taiwan_products(product_details)
        print(f"\r{i}/{len(tasting_ids)}", end="")
        sleep(0.5)

    write_to_readme(taiwan_products)


if __name__ == "__main__":
    main()
