import json
from dataclasses import dataclass


@dataclass
class Product:
    """Represents a product with all its details"""

    category: str
    name: str
    link: str
    price: float
    description: str


def parse_products_json_data(
    file_path: str = "tests/products.json",
) -> dict[str, list[Product]]:
    with open(file_path, "r") as f:
        expected_products = json.load(f)
    expected_products_data = {"phone": [], "laptop": [], "monitor": []}

    for expected_product_name in expected_products_data:
        category_products = {
            name: details
            for name, details in expected_products.items()
            if details["category"] == expected_product_name
        }

        for name, value in category_products.items():
            prod = Product(
                category=value["category"],
                name=name,
                link=value["link"],
                price=value["price"],
                description=value["description"],
            )
            expected_products_data[expected_product_name].append(prod)

    return expected_products_data
