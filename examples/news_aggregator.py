#!/usr/bin/env python3
"""
News Aggregator Example

Extracts top stories from multiple news sources
and creates a unified feed.
"""

from nova_autopilot import AutoPilot
from datetime import datetime
import json


NEWS_SOURCES = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com",
        "extraction": "top 10 story titles and URLs from the front page"
    },
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com",
        "extraction": "top 5 featured article headlines and URLs"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com",
        "extraction": "top 5 headlines from the main section"
    }
]


def aggregate_news(sources: list[dict] = None) -> dict:
    """
    Aggregate news from multiple sources.

    Args:
        sources: List of news sources to check

    Returns:
        Aggregated news feed
    """
    if sources is None:
        sources = NEWS_SOURCES

    pilot = AutoPilot(headless=True, timeout=30)
    feed = {
        "generated_at": datetime.utcnow().isoformat(),
        "sources": []
    }

    for source in sources:
        print(f"Fetching from {source['name']}...")

        result = pilot.extract(
            f"Extract the {source['extraction']}. "
            f"Return as JSON array with objects containing 'title' and 'url'.",
            starting_url=source["url"]
        )

        source_data = {
            "name": source["name"],
            "url": source["url"],
            "fetched_at": datetime.utcnow().isoformat()
        }

        if result.success:
            source_data["stories"] = result.data
            source_data["count"] = len(result.data) if isinstance(result.data, list) else 0
        else:
            source_data["error"] = result.error
            source_data["stories"] = []

        feed["sources"].append(source_data)

    # Calculate totals
    feed["total_stories"] = sum(
        s.get("count", 0) for s in feed["sources"]
    )

    return feed


def display_feed(feed: dict):
    """Display the aggregated feed."""
    print("\n" + "=" * 60)
    print(f"NEWS AGGREGATOR - {feed['generated_at']}")
    print(f"Total Stories: {feed['total_stories']}")
    print("=" * 60 + "\n")

    for source in feed["sources"]:
        print(f"\n📰 {source['name']}")
        print("-" * 40)

        if "error" in source:
            print(f"  ❌ Error: {source['error']}")
            continue

        for i, story in enumerate(source.get("stories", [])[:5], 1):
            title = story.get("title", "No title")
            url = story.get("url", "")
            print(f"  {i}. {title[:50]}...")
            if url:
                print(f"     {url[:60]}...")


def main():
    print("News Aggregator - Fetching stories...")
    feed = aggregate_news()

    display_feed(feed)

    # Save feed
    output_file = f"news_feed_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(feed, f, indent=2)
    print(f"\n\nFeed saved to {output_file}")


if __name__ == "__main__":
    main()
