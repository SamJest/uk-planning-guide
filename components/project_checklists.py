"""Practical evidence preparation, not a determination of planning entitlement."""
from html import escape
from urllib.parse import urlsplit

CHECKLISTS = {
    'fences-and-walls': ('Fence or wall survey', [
        ('Draw a section', 'Show existing ground on both sides, the proposed top of the enclosure and any retaining structure. Record the maximum height, not just a nominal panel size.'),
        ('Mark the road relationship', 'On a plan, mark the enclosure, road, pavement and access points. Take photographs showing visibility at entrances; ask the authority which highway-related controls need checking.'),
        ('Separate permissions', 'Record boundary ownership, any shared structure and relevant conditions or heritage controls. Ask separate questions about planning and private boundary rights.'),
        ('Worked preparation example', 'For a sloping frontage, provide a section at the highest and lowest ground points and a photograph towards the access. A panel catalogue height alone leaves the site relationship unanswered.')]),
    'driveways': ('Driveway drainage and access survey', [
        ('Measure the surface', 'Draw the existing and proposed area, materials and gradient. Mark where rainwater goes now and where it would go after the work.'),
        ('Trace the drainage route', 'Show permeable layers, planted areas or any proposed drain on the sketch. Do not assume a product labelled permeable proves that the complete construction drains correctly.'),
        ('Check access separately', 'Record whether the vehicle crossing already exists and whether widening or a new dropped kerb is proposed. Ask the highway authority about its crossover process separately from the planning enquiry.'),
        ('Worked preparation example', 'For a front garden falling towards the pavement, show the fall arrows and proposed runoff interception. Ask about the complete drainage design rather than sending only the paving specification.')]),
    'solar-panels': ('Solar installation survey', [
        ('Describe the installation', 'State whether panels are roof-mounted, wall-mounted or freestanding. Record the number of panels, array dimensions, projection and highest point.'),
        ('Show the setting', 'Provide roof elevations or a site plan, photographs from public viewpoints and the proposed mounting details. Record known heritage designations without assuming their boundaries.'),
        ('Separate the checks', 'Ask which planning route applies to this installation and nation. Keep structural assessment, electrical installation and any grid or ownership permissions as separate enquiries.'),
        ('Worked preparation example', 'For an array on an outbuilding, identify that building and its use explicitly; a house-roof example does not describe a freestanding array or a different building.')]),
    'garden-rooms': ('Garden room use and measurement survey', [
        ('Describe the intended use', 'State the activities, frequency of use and whether sleeping, cooking, independent occupation or business visitors are proposed. Do not describe a residential annexe simply as a garden room.'),
        ('Measure the whole proposal', 'Record overall and eaves heights, footprint, boundary distances and ground levels. Include decking, platforms and existing outbuildings on the plan.'),
        ('Check the site history', 'Gather relevant permissions and conditions, known designations and the original house/site information available. Ask which national rule and property-specific controls apply.'),
        ('Worked preparation example', 'For a home office with occasional guests, disclose both intended uses and show facilities on the plan. A drawing labelled office does not explain proposed sleeping or independent occupation.')]),
}

def render_checklist(slug):
    title, items = CHECKLISTS[slug]
    return ('\n<section id="project-evidence-checklist" aria-labelledby="project-evidence-heading">'
        '<h2 id="project-evidence-heading">'+escape(title)+'</h2>'
        '<p>Prepare these facts before choosing a rule or asking the authority. Start by identifying England, Wales, Scotland or Northern Ireland: this checklist supplies no cross-UK permission threshold.</p>'
        '<dl>'+''.join('<dt><strong>'+escape(label)+'</strong></dt><dd>'+escape(text)+'</dd>' for label,text in items)+'</dl>'
        '<p><a href="/downloads/'+slug+'-survey.txt" download>Download the reusable survey checklist (text)</a></p>'
        '<p>Preparation guidance added 27 October 2026. It does not confirm permission, title rights or property-specific designations.</p></section>\n')

def checklist_for_url(url):
    path=urlsplit(url).path.strip('/')
    return render_checklist(path) if path in CHECKLISTS else ''

def download_text(slug):
    title,items=CHECKLISTS[slug]
    return title+'\n\nNation:\nAddress / planning authority:\nExisting use:\nProposed work:\n\n'+'\n\n'.join(label+'\n'+text+'\nNotes: ' for label,text in items)+'\n\nAuthority response, source document and date:\nOutstanding checks:\n\nPreparation aid only; no permission or designation determination.\n'
