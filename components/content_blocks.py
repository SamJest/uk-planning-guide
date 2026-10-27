# ------------------------------------------------
# content_blocks.py
# Reusable HTML content blocks
# ------------------------------------------------

from components.scenario_tool import render_scenario_tool


def hero(title, subtitle=""):
    return f"""
    <section class="hero">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </section>
    """


def info_card(title, text):
    return f"""
    <div class="card">
        <h3>{title}</h3>
        <p>{text}</p>
    </div>
    """


def example_block(text):
    return f"""
    <div class="example">
        <p>{text}</p>
    </div>
    """


def build_scenario_calculator(scenario_slug: str) -> str:
    return render_scenario_tool(scenario_slug)
