from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.search_demand_priorities import (
    GSC_CLUSTER_HUBS,
    GSC_EXPANSION_CANDIDATES_2026_06_08,
    GSC_EXPANSION_RELEASE_LIMITS,
)


def _score(item: dict) -> float:
    impressions = item.get("impressions")
    position = item.get("position")
    priority = int(item.get("priority") or 999)
    if impressions and position:
        return float(impressions) / max(float(position), 1.0) + (1000 - priority)
    return 1000 - priority


def main() -> None:
    candidates = sorted(GSC_EXPANSION_CANDIDATES_2026_06_08, key=_score, reverse=True)
    by_cluster: dict[str, list[dict]] = defaultdict(list)
    for item in candidates:
        by_cluster[item["cluster"]].append(item)

    print("Second-stage GSC expansion candidates")
    print(f"Release: {GSC_EXPANSION_RELEASE_LIMITS['release']}")
    print(f"Candidate pages: {len(candidates)}")
    print(f"Hub pages: {len(GSC_CLUSTER_HUBS)}")
    print(
        "Release cap: "
        f"{GSC_EXPANSION_RELEASE_LIMITS['min_pages']}-{GSC_EXPANSION_RELEASE_LIMITS['max_pages']} local-search pages"
    )
    print()

    for cluster, items in sorted(by_cluster.items(), key=lambda row: row[0]):
        hub = GSC_CLUSTER_HUBS.get(cluster, {})
        hub_label = f" -> hub /local-search/{hub['slug']}/" if hub else ""
        print(f"{cluster}: {len(items)} candidates{hub_label}")
        for item in sorted(items, key=lambda row: (int(row.get("priority") or 999), row["slug"]))[:10]:
            metrics = ""
            if item.get("impressions") is not None:
                metrics = f" | {item['impressions']} impressions"
                if item.get("position") is not None:
                    metrics += f" | pos {item['position']}"
            print(f"  {item['priority']:>2}. /local-search/{item['slug']}/ -> {item['target_route']}{metrics}")
        if len(items) > 10:
            print(f"  ... {len(items) - 10} more")
        print()


if __name__ == "__main__":
    main()
