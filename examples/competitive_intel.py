#!/usr/bin/env python3
"""
Competitive Intelligence Example

Monitors competitor websites for pricing changes,
new features, and content updates.
"""

from nova_autopilot import AutoPilot
from datetime import datetime
import json
import hashlib


class CompetitorMonitor:
    """Monitor competitor websites for changes."""

    def __init__(self, competitors: list[dict]):
        """
        Initialize monitor with competitor list.

        Args:
            competitors: List of dicts with 'name', 'url', 'track' (what to monitor)
        """
        self.competitors = competitors
        self.pilot = AutoPilot(headless=True)
        self.history_file = "competitor_history.json"
        self._load_history()

    def _load_history(self):
        """Load historical data."""
        try:
            with open(self.history_file) as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = {}

    def _save_history(self):
        """Save historical data."""
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def _content_hash(self, content: str) -> str:
        """Generate hash of content for change detection."""
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def check_competitor(self, competitor: dict) -> dict:
        """
        Check a single competitor for updates.

        Args:
            competitor: Competitor config dict

        Returns:
            Check result with any detected changes
        """
        name = competitor["name"]
        url = competitor["url"]
        track = competitor.get("track", "main content and pricing")

        print(f"Checking {name}...")

        result = self.pilot.extract(
            f"Extract {track}. Include any pricing information, "
            f"feature lists, and promotional offers you can find. "
            f"Return as JSON with relevant fields.",
            starting_url=url
        )

        check_result = {
            "name": name,
            "url": url,
            "checked_at": datetime.utcnow().isoformat(),
            "success": result.success
        }

        if result.success:
            content_str = json.dumps(result.data, sort_keys=True)
            current_hash = self._content_hash(content_str)

            check_result["data"] = result.data
            check_result["hash"] = current_hash

            # Check for changes
            previous = self.history.get(name, {})
            previous_hash = previous.get("hash")

            if previous_hash and previous_hash != current_hash:
                check_result["changed"] = True
                check_result["previous_data"] = previous.get("data")
                check_result["previous_checked"] = previous.get("checked_at")
            else:
                check_result["changed"] = False

            # Update history
            self.history[name] = {
                "hash": current_hash,
                "data": result.data,
                "checked_at": check_result["checked_at"]
            }
        else:
            check_result["error"] = result.error

        return check_result

    def run_check(self) -> list[dict]:
        """
        Run full competitive intelligence check.

        Returns:
            List of check results
        """
        results = []

        for competitor in self.competitors:
            result = self.check_competitor(competitor)
            results.append(result)

        self._save_history()
        return results

    def generate_report(self, results: list[dict]) -> str:
        """Generate human-readable report."""
        lines = [
            "=" * 60,
            f"COMPETITIVE INTELLIGENCE REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 60,
            ""
        ]

        changes_detected = []

        for result in results:
            status = "✓" if result["success"] else "✗"
            lines.append(f"{status} {result['name']}")
            lines.append(f"  URL: {result['url']}")

            if result["success"]:
                if result.get("changed"):
                    lines.append(f"  ⚠️  CHANGES DETECTED")
                    changes_detected.append(result)
                else:
                    lines.append(f"  No changes since last check")
            else:
                lines.append(f"  Error: {result.get('error', 'Unknown')}")

            lines.append("")

        lines.append("-" * 60)
        lines.append(f"SUMMARY: {len(changes_detected)} competitors with changes")

        if changes_detected:
            lines.append("\nCHANGES REQUIRING ATTENTION:")
            for c in changes_detected:
                lines.append(f"  • {c['name']}")

        return "\n".join(lines)


def main():
    # Example competitor list
    competitors = [
        {
            "name": "Competitor A",
            "url": "https://competitor-a.com/pricing",
            "track": "pricing tiers and feature lists"
        },
        {
            "name": "Competitor B",
            "url": "https://competitor-b.com",
            "track": "main product features and pricing"
        },
        {
            "name": "Competitor C",
            "url": "https://competitor-c.com/features",
            "track": "feature comparison table"
        }
    ]

    print("Competitive Intelligence Monitor")
    print("=" * 40)

    monitor = CompetitorMonitor(competitors)
    results = monitor.run_check()

    report = monitor.generate_report(results)
    print("\n" + report)

    # Save detailed results
    with open("competitor_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDetailed report saved to competitor_report.json")


if __name__ == "__main__":
    main()
