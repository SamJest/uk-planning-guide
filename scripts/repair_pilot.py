"""Idempotent, narrowly scoped output repair; upstream generator is absent.

Never creates routes or edits forms/scripts. Run with --check in CI.
"""
import argparse
import re
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PILOT = {
    'planning-permission/flintshire': ('wales', 'Planning permission: choose the Welsh route',
        'This is a project-neutral starting point for Flintshire, Wales. It does not establish whether your proposal has permission or permitted development rights.',
        ['Describe the proposed building work or change of use before choosing a rule: dimensions alone do not determine the route.', 'Use the Welsh application route in the existing official-source links below; do not apply an England-only calculator result to this property.', 'Prepare the address, existing and proposed use, dimensioned sketch and planning history. Ask the authority which application or certificate route fits those facts.']),
    'maximum-height/lambeth': ('england', 'Which height are you measuring?',
        'This page cannot give one maximum height for every project in Lambeth. Select the work first; a garden building height must not be used as an extension, fence or roof limit.',
        ['Record existing ground levels, the highest proposed point and separate eaves height where relevant. Mark the measurement points on a section drawing.', 'Identify whether the question concerns a boundary enclosure, outbuilding, extension or roof alteration. Follow the matching project guide, rather than transferring a threshold between projects.', 'Check planning conditions and site constraints before relying on a national allowance. If ground slopes or the proposal is near a limit, ask the planning authority to confirm the measurement basis.']),
    'article-4/cardiff': ('wales', 'Cardiff: direction coverage is unresolved',
        'This guide has not verified a Cardiff direction, its affected development rights, mapped boundary or effective date. It cannot tell you that Article 4 applies to an address.',
        ['Give the planning authority the address and the exact proposed work or change of use.', 'Request the actual direction document, schedule of withdrawn rights, boundary map and effective date. A conservation-area label alone does not answer this question.', 'Keep the written response and map with your project records. Use Welsh rules; do not assume an English HMO use-class route applies.']),
    'article-4/milton-keynes': ('england', 'Milton Keynes: check the direction and the address',
        'No direction boundary or effective date has been verified for this page. A council-wide Article 4 search result is not evidence that a particular property or development right is affected.',
        ['Specify whether the proposal is a change of use, external work or another development: directions can withdraw different rights.', 'Ask for the signed direction, affected rights, effective date and address-level boundary map. Compare the property with the map, not just a town name.', 'For an HMO proposal, ask planning and licensing separately. Record the existing lawful use, proposed occupancy and any relevant conditions.']),
    'hmos/staffordshire/tamworth/article-4': ('england', 'Tamworth HMO: establish use and direction scope first',
        'The relevant question is the proposed HMO use and whether an applicable Article 4 direction removes the right being relied on. This page has not verified a Tamworth direction or property boundary.',
        ['Record the existing lawful use and proposed number of occupiers and households. Ask the authority to establish the applicable use classification and planning route.', 'Ask whether the proposal relies on a C3-to-C4 permitted development right and whether any direction actually withdraws that right at this address. Obtain the direction, map and effective date before drawing a conclusion.', 'Check HMO licensing separately from planning. A licence does not establish planning permission, and a planning decision does not settle licensing. Conservation or listed-building controls may be additional checks, not a substitute for the HMO use question.']),
}

def render(nation, title, answer, steps):
    return ('\n<section id="intent-research-pilot" data-evidence-status="unverified" data-jurisdiction="'+nation+'">\n'
        '<h2>'+escape(title)+'</h2><p><strong>Quick answer:</strong> '+escape(answer)+'</p>\n'
        '<h3>Prepare a useful authority enquiry</h3><ol>'+''.join('<li>'+escape(s)+'</li>' for s in steps)+'</ol>\n'
        '<p>Independent information from UK Planning Guide. This is not official council advice or confirmation of a lawful development right. Editorial correction: 27 October 2026; local source verification remains outstanding.</p>\n</section>\n')

def repaired(text, key, data):
    text = re.sub(r'\n<section id="intent-research-pilot".*?</section>\n', '', text, flags=re.S)
    text = re.sub(r'(</h1>\n)', lambda m: m[0]+render(*data), text, count=1)
    if key.startswith('hmos/'):
        text = text.replace('The live issue is usually conservation areas.', 'Establish the HMO use classification and any applicable Article 4 direction; local coverage is not verified here.')
        text = text.replace('Confirm whether conservation areas and listed buildings can change the route before you rely on the baseline answer.', 'Confirm the existing lawful use, proposed occupancy, direction scope and separate licensing requirements with the authority.')
    # Imported source-review dates have no supporting check record in this checkout.
    text = re.sub(r'Last reviewed \d{1,2} [A-Za-z]+ \d{4}', 'Source check date not evidenced in this checkout', text)
    return text

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    stale=[]
    for key,data in PILOT.items():
        path=ROOT/key/'index.html'
        before=path.read_text()
        after=repaired(before,key,data)
        if before != after:
            stale.append(key)
            if not args.check: path.write_text(after)
    if args.check and stale: raise SystemExit('Pilot output differs: '+', '.join(stale))
    print(f'Pilot: {len(PILOT)} pages; {len(stale)} '+('stale' if args.check else 'updated'))

if __name__ == '__main__': main()
