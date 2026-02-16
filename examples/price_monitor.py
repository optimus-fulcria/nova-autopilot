#!/usr/bin/env python3
"""
Price Monitor Example

Monitors product prices across multiple e-commerce sites
and alerts when prices drop below threshold.
"""

from nova_autopilot import AutoPilot
import json


def monitor_prices(products: list[dict]) -> list[dict]:
    """
    Monitor prices for a list of products.

    Args:
        products: List of dicts with 'name', 'url', 'threshold'

    Returns:
        List of products with current prices and deal status
    """
    pilot = AutoPilot(headless=True)
    results = []

    for product in products:
        result = pilot.extract(
            f"Find the current price of the main product on this page. "
            f"Return as JSON with 'price' (number) and 'currency' (string).",
            starting_url=product["url"]
        )

        if result.success:
            price_data = result.data
            current_price = price_data.get("price", 0)
            is_deal = current_price > 0 and current_price < product["threshold"]

            results.append({
                "name": product["name"],
                "url": product["url"],
                "threshold": product["threshold"],
                "current_price": current_price,
                "currency": price_data.get("currency", "USD"),
                "is_deal": is_deal
            })
        else:
            results.append({
                "name": product["name"],
                "url": product["url"],
                "error": result.error
            })

    return results


def main():
    # Example product watchlist
    watchlist = [
        {
            "name": "Wireless Earbuds",
            "url": "https://www.amazon.com/dp/B0CXXXXXX",
            "threshold": 50.00
        },
        {
            "name": "USB-C Hub",
            "url": "https://www.amazon.com/dp/B0CYYYYYY",
            "threshold": 30.00
        }
    ]

    print("Price Monitor - Checking prices...")
    results = monitor_prices(watchlist)

    print("\n=== Price Report ===\n")
    for item in results:
        if "error" in item:
            print(f"❌ {item['name']}: Error - {item['error']}")
        elif item["is_deal"]:
            print(f"🔥 DEAL: {item['name']} - ${item['current_price']} "
                  f"(under ${item['threshold']} threshold)")
        else:
            print(f"📊 {item['name']}: ${item['current_price']}")

    # Save results
    with open("price_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nReport saved to price_report.json")


if __name__ == "__main__":
    main()
