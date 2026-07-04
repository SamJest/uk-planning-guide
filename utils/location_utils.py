from typing import List, Dict


def county_name_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def build_master_town_index(councils_by_county):

    towns = []

    for county_slug, councils in councils_by_county.items():

        county_name = county_name_from_slug(county_slug)

        for council in councils:

            towns.append(
                {
                    "county_slug": county_slug,
                    "county_name": county_name,
                    "town_slug": council["town_slug"],
                    "town_name": council["town_name"],
                }
            )

    towns.sort(key=lambda x: (x["county_name"], x["town_name"]))

    return towns