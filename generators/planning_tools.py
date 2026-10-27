import shutil
from pathlib import Path

from components.seo import build_software_application_schema, build_tool_metadata, build_tools_index_metadata
from components.tool_pages import (
    assemble_tool_page,
    build_tool_faq_links,
    build_tool_embedded_faq,
    build_tool_guidance_cta,
    build_guidance_links,
    build_planning_context,
    build_tool_calculator,
    build_tool_explanation,
    build_tool_hero,
    build_tool_links,
    build_tool_building_regs_handoff,
    build_tool_next_steps,
    build_tool_project_tracker,
    build_tool_search_intents,
    build_tools_index_content,
    build_trust_section,
)
from core.files import write_file
from core.build_scope import should_render_route
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base
from data.tools_data import load_tools
from utils.random_tools import get_month_year


BASE_URL = "https://ukplanningguide.co.uk"
TOOLS_FOLDER = "tools"
MAX_RELATED_TOOLS = 4
MAX_GUIDANCE_LINKS = 6


def generate_tools():
    print("Generating planning tools")

    tools_root = OUTPUT_FOLDER / TOOLS_FOLDER
    if tools_root.exists():
        shutil.rmtree(tools_root)
    tools_root.mkdir(parents=True, exist_ok=True)

    tools = load_tools()

    index_title, index_description = build_tools_index_metadata()

    index_html = inject_into_base(
        title=index_title,
        content=build_tools_index_content(tools),
        options={"breadcrumbs": [("Home", "/"), ("Tools", "")]},
        canonical_url=f"{BASE_URL}/{TOOLS_FOLDER}/",
        meta_description=index_description,
    )
    write_file(tools_root, "index.html", index_html)

    for tool in tools:
        if not should_render_route(f"/{TOOLS_FOLDER}/{tool['slug']}/"):
            continue
        folder = tools_root / tool["slug"]
        folder.mkdir(parents=True, exist_ok=True)

        content = assemble_tool_page(
            [
                build_tool_hero(tool),
                build_tool_calculator(tool),
                build_tool_next_steps(tool),
                build_tool_project_tracker(tool),
                build_tool_explanation(tool),
                build_tool_embedded_faq(tool),
                build_tool_search_intents(tool),
                build_planning_context(tool["title"]),
                build_tool_building_regs_handoff(tool),
                build_tool_guidance_cta(tool["title"]),
                build_tool_faq_links(tool),
                build_guidance_links(tool, MAX_GUIDANCE_LINKS),
                build_tool_links(tool["slug"], tools, MAX_RELATED_TOOLS),
                build_trust_section(),
                f"<div class='last-updated'>Updated {get_month_year()}</div>",
            ]
        )

        title, description = build_tool_metadata(tool)

        html = inject_into_base(
            title=title,
            content=content,
            options={
                "breadcrumbs": [("Home", "/"), ("Tools", "/tools/"), (tool["title"], "")],
                "schema": build_software_application_schema(tool, f"{BASE_URL}/{TOOLS_FOLDER}/{tool['slug']}/"),
            },
            canonical_url=f"{BASE_URL}/{TOOLS_FOLDER}/{tool['slug']}/",
            meta_description=description,
        )
        write_file(folder, "index.html", html)

    print("Planning tools generated successfully")
