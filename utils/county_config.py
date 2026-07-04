from data.scenario_data import select_scenarios


def load_scenarios():
    return select_scenarios(
        [
            "planning-permission",
            "depth-limits",
            "height-limits",
            "boundary-rules",
            "permitted-development",
            "article-4",
            "conservation-areas",
            "listed-buildings",
        ]
    )
