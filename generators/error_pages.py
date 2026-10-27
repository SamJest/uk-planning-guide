from core.files import write_file
from core.paths import OUTPUT_FOLDER
from core.render import inject_into_base


def build_not_found_content() -> str:
    return """
<section class="hero" data-not-found-page="true">
<span class="badge">Page not found</span>
<h1>That Planning Page Is Not Here</h1>
<p>The address may be incomplete, out of date or more specific than the guide you need. Choose the closest route below instead of guessing from a missing page.</p>
<div class="download-actions">
<a class="button" href="/tools/">Use a planning check</a>
<a class="button button-secondary" href="/">Return to the homepage</a>
</div>
</section>

<section aria-labelledby="not-found-start">
<span class="eyebrow">Start with what you know</span>
<h2 id="not-found-start">Find A Useful Route Back Into The Guide</h2>
<div class="grid">
<a class="card" href="/tools/"><div class="card-kicker">Planning route</div><h3>Check the likely route</h3><p>Start with the project and the main constraint, then follow the relevant guide or formal-check route.</p><span class="cta">Open planning tools</span></a>
<a class="card" href="/councils/"><div class="card-kicker">Local context</div><h3>Find the council layer</h3><p>Use the authority index when a conservation area, Article 4 direction or local process may change the answer.</p><span class="cta">Browse councils</span></a>
<a class="card" href="/workflows/"><div class="card-kicker">Project journey</div><h3>Follow a project workflow</h3><p>Work through the likely checks, evidence and next actions for common home improvement projects.</p><span class="cta">Browse workflows</span></a>
<a class="card" href="/my-planning-project/"><div class="card-kicker">Saved work</div><h3>Return to your project</h3><p>Open guides and tool results saved in this browser without creating an account.</p><span class="cta">Open My Planning Project</span></a>
</div>
</section>

<section>
<span class="eyebrow">Still looking?</span>
<h2>Use The Broad Guide Before The Exact Local Page</h2>
<p>If an old link named a project, council and several rule topics at once, begin with the main project guide or council page. Confirm the exact property against official council information before spending money or relying on a planning exemption.</p>
</section>
"""


def render_not_found_page() -> str:
    return inject_into_base(
        title="Page Not Found | UK Planning Guide",
        content=build_not_found_content(),
        options={
            "breadcrumbs": [("Home", "/"), ("Page not found", "")],
            "meta_robots": "noindex, follow",
            "include_canonical": False,
        },
        canonical_url="",
        meta_description="The requested UK Planning Guide page could not be found. Use the project, council and planning-tool routes to continue.",
    )


def generate_error_pages() -> None:
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    write_file(OUTPUT_FOLDER, "404.html", render_not_found_page())
