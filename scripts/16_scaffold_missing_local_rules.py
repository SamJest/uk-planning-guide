import json
from pathlib import Path
import sys


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from core.paths import DATA_FOLDER  # noqa: E402
from data.loaders import load_councils, load_projects  # noqa: E402
from utils.country_utils import get_country_name, get_householder_label, get_system_label  # noqa: E402


LAST_VERIFIED = "2026-03"
TARGET_PROJECTS = {
    "garages",
    "hard-surfaces",
    "heat-pumps",
    "hmos",
    "solar-panels",
    "windows-and-doors",
}

COASTAL_COUNTIES = {
    "cornwall",
    "devon",
    "dorset",
    "east-sussex",
    "west-sussex",
    "hampshire",
    "kent",
    "norfolk",
    "northumberland",
    "wales",
}

RURAL_COUNTIES = {
    "cumbria",
    "herefordshire",
    "lincolnshire",
    "shropshire",
    "somerset",
    "wiltshire",
}


PROJECT_COPY = {
    "garages": {
        "defaults_pd": "Across {county_name}, detached domestic garages are usually easiest on the planning permission route when they stay clearly secondary to the house, respect height and boundary relationships, and avoid creating a more dominant frontage or access arrangement.",
        "defaults_rules": {
            "height_rules": "Garage proposals across {county_name} are normally judged first on overall height, eaves height and whether the roof form keeps the building subordinate to the main house.",
            "depth_rules": "Footprint and siting matter because a garage that consumes too much of the plot or pushes into the front part of the site will usually face a closer planning review.",
            "boundary_rules": "Boundary siting, neighbour relationship and vehicle access are the recurring pressure points for garages in {county_name}, especially where a new crossover or tight turning arrangement is involved.",
            "roof_rules": "Low-profile garage roofs are generally easier than taller roof forms that create storage volume, apparent accommodation or a more dominant outbuilding shape.",
            "materials_rules": "Garages are normally easiest to support when the materials, door treatment and overall appearance sit comfortably with the house and local street scene.",
        },
        "local_pd": "In {council_name}, a detached garage is usually easiest to keep off the formal planning permission route when it remains clearly secondary to the house, sits comfortably within the plot and does not create a more dominant frontage or access arrangement.",
        "local_rules": {
            "height_rules": "In {council_name}, garage height is usually the first measurement to sense-check, especially where the building sits close to a boundary or uses a taller pitched roof.",
            "depth_rules": "A garage in {council_name} is more likely to need a closer review if the footprint starts to dominate the garden or front part of the site rather than sitting as a modest supporting structure.",
            "boundary_rules": "Boundary siting, neighbour impact and highway practicality all matter in {council_name}, particularly if the garage depends on a new or altered vehicle access.",
            "roof_rules": "Garage roofs in {council_name} are usually easiest where they stay low-profile and do not suggest loft storage, accommodation or a second-storey form.",
            "materials_rules": "Materials and frontage treatment should help the garage read as a subordinate domestic building in {council_name}, not as a visually dominant addition to the property.",
        },
        "restrictions": {
            "conservation_area": "Garages in conservation areas within {council_name} often receive a closer design review where they affect the character of a visible frontage or the wider street scene.",
            "listed_building": "Garages affecting a listed building or its setting in {council_name} usually need a more careful planning and heritage consent check.",
        },
    },
    "hard-surfaces": {
        "defaults_pd": "Across {county_name}, hard surfacing is usually lowest risk on the planning permission route when drainage is handled properly, level changes stay modest and the work does not turn a soft frontage into a dominant engineered parking area.",
        "defaults_rules": {
            "height_rules": "Raised surfacing, retaining features and height or level changes can matter as much as the paving finish itself when councils assess hard-surface schemes in {county_name}.",
            "depth_rules": "Surface coverage, front garden drainage and overall project extent are usually the deciding issues for hard surfacing across {county_name}, especially where large impermeable areas are proposed.",
            "boundary_rules": "Frontage position, highway relationship and any linked access changes are often what make a hard-surfacing scheme more sensitive in {county_name}.",
            "roof_rules": "For hard-surface projects, the design equivalent of a roof check is usually the drainage fall and discharge strategy rather than any vertical structure.",
            "materials_rules": "Permeable, visually restrained finishes are usually easier to justify than broad impermeable paving that removes planting and dominates the frontage.",
        },
        "local_pd": "In {council_name}, hard surfacing is usually easiest to keep off the planning permission route where drainage is clear, levels stay sensible and the work does not turn the frontage into an over-engineered parking layout.",
        "local_rules": {
            "height_rules": "In {council_name}, even paving work can move into a closer review if it relies on raised height changes, retaining edges or platforms that materially change the site.",
            "depth_rules": "Large impermeable areas in {council_name} usually deserve the earliest drainage check, particularly where the work affects the front garden or main parking area.",
            "boundary_rules": "Boundary treatment, highway relationship and crossover changes often shape the hard-surfacing answer in {council_name} more than the paving material alone.",
            "roof_rules": "For hard surfacing in {council_name}, the key technical design question is usually where water goes and whether the falls avoid creating problems for neighbours or the highway.",
            "materials_rules": "Permeable finishes and a softer overall frontage usually work better in {council_name} than extensive impermeable paving with little visual relief.",
        },
        "restrictions": {
            "conservation_area": "Hard surfacing in conservation areas within {council_name} often faces a closer review where it changes the look of a visible frontage or removes established soft landscaping.",
            "listed_building": "Works to the setting of a listed building in {council_name}, including resurfacing and level changes, can need a more careful planning and heritage review.",
        },
    },
    "heat-pumps": {
        "defaults_pd": "Across {county_name}, domestic heat pumps are usually easiest on the planning permission route when the unit stays compact, sits discreetly, and can show a clean noise and neighbour-amenity story under the {system_label}.",
        "defaults_rules": {
            "height_rules": "Bulky housings, stacked equipment or extra height and visual prominence can make a heat pump feel more like external plant than a modest domestic installation.",
            "depth_rules": "Projection from the wall or building line matters because exposed units and screens can quickly look more intrusive than a tighter, building-hugging installation.",
            "boundary_rules": "Boundary siting and noise are usually the first planning pressure points for heat pumps across {county_name}, especially where the unit sits near neighbours or a quiet garden edge.",
            "roof_rules": "Pipe runs, housings and ancillary kit should be treated as part of the overall design package rather than as afterthoughts added to the building later.",
            "materials_rules": "Well-scaled screening and restrained finishes usually work better than oversized housings that create a second visual problem around the plant.",
        },
        "local_pd": "In {council_name}, a domestic heat pump is usually easiest to keep off the formal planning permission route when it stays compact, sits discreetly and can demonstrate a comfortable noise and amenity position for neighbours.",
        "local_rules": {
            "height_rules": "In {council_name}, heat pump proposals are usually easier where the unit and any housing remain modest in height and visually subordinate to the house rather than reading as prominent external plant.",
            "depth_rules": "Projection matters in {council_name} because exposed wall-mounted units or freestanding equipment can look much more intrusive than a tighter installation close to the building.",
            "boundary_rules": "Noise, vibration and boundary relationship are the earliest issues to check in {council_name}, especially where the unit sits close to neighbouring gardens or quiet amenity space.",
            "roof_rules": "Associated pipework, screens and ancillary kit should be designed as one package in {council_name} so the installation looks intentional rather than retrofitted piecemeal.",
            "materials_rules": "Restrained screening and a tidy finish usually help a heat pump scheme in {council_name} far more than heavy enclosures that add visual bulk.",
        },
        "restrictions": {
            "conservation_area": "Heat pumps in conservation areas within {council_name} often face a closer review where the unit or its screening is visible from public viewpoints.",
            "listed_building": "Heat pump installations on or around listed buildings in {council_name} usually need a more careful planning and heritage consent assessment.",
        },
    },
    "hmos": {
        "defaults_pd": "Across {county_name}, HMO proposals usually need an early planning permission check because local policy, shared-housing concentration and Article 4 coverage often matter more than any simple fallback route.",
        "defaults_rules": {
            "height_rules": "For HMOs, the planning issue is usually intensity of occupation and local policy rather than building height alone, although physical enlargement can add a second planning layer.",
            "depth_rules": "Layout, garden amenity space, refuse storage and any extension or conversion project linked to the HMO can all change the planning route across {county_name}.",
            "boundary_rules": "Neighbour amenity, parking pressure, servicing and local shared-housing concentration are recurring pressure points for HMO proposals in {county_name}.",
            "roof_rules": "Roof rooms, dormers and upper-floor reconfiguration often need to be reviewed alongside the change of use rather than as a separate afterthought.",
            "materials_rules": "Frontage appearance, cycle storage, bin arrangements and entrance treatment can influence how an HMO proposal is judged even where the main use change sits inside the building.",
        },
        "local_pd": "In {council_name}, an HMO proposal usually needs an early planning permission check because local policy, concentration and any Article 4 coverage often matter more than a simple fallback route.",
        "local_rules": {
            "height_rules": "In {council_name}, HMO proposals are normally judged on intensity of occupation, bedroom mix and policy context rather than height alone, unless the building is also being enlarged.",
            "depth_rules": "Layout quality, garden amenity space and the supporting project works needed to make the HMO function properly are often central planning issues in {council_name}.",
            "boundary_rules": "Neighbour amenity, parking, refuse and the wider concentration of HMOs are usually the first local pressure points to review in {council_name}.",
            "roof_rules": "Roof rooms, dormers or enlarged upper floors linked to an HMO in {council_name} usually need to be checked as part of one joined-up planning package.",
            "materials_rules": "Frontage appearance, bin stores and entrance arrangements should be handled carefully in {council_name} so the scheme looks managed rather than visually disruptive.",
        },
        "restrictions": {
            "conservation_area": "HMO proposals in conservation areas within {council_name} can face an added design review where external changes, refuse storage or frontage alterations are proposed.",
            "listed_building": "Listed buildings in {council_name} usually need a more careful heritage and consent review before physical works linked to an HMO scheme are assumed to be acceptable.",
            "article4_notes": "Article 4 directions are one of the first checks for HMO proposals in {council_name}, because they can remove the simpler fallback route for change of use.",
        },
    },
    "solar-panels": {
        "defaults_pd": "Across {county_name}, domestic solar panels are usually easiest on the planning permission route when they sit close to the roof or wall, stay visually secondary to the building and avoid awkward heritage or frontage impacts.",
        "defaults_rules": {
            "height_rules": "Solar panels are usually lowest risk when the array and mounting system do not add noticeable height or make the building visually bulkier.",
            "depth_rules": "Projection from the roof or wall matters because deeper frames and freestanding equipment can quickly move the installation away from a routine domestic appearance.",
            "boundary_rules": "Boundary-facing arrays, visible side elevations and garden-based equipment usually deserve a closer amenity and visual check across {county_name}.",
            "roof_rules": "The easiest solar schemes usually follow the roof plane cleanly and avoid sensitive, highly visible or heritage-affected roof slopes.",
            "materials_rules": "Panels, inverters and associated equipment should be designed as one tidy appearance-led package rather than as separate add-ons scattered around the building.",
        },
        "local_pd": "In {council_name}, solar panels are usually easiest to keep off the formal planning permission route when they sit close to the roof or wall, stay visually secondary to the building and avoid awkward heritage or frontage impacts.",
        "local_rules": {
            "height_rules": "In {council_name}, the planning route usually gets harder where solar panels rely on raised frames, extra height, freestanding arrays or associated equipment that makes the installation feel noticeably bulkier.",
            "depth_rules": "Projection from the roof or wall matters in {council_name} because deeper frames and freestanding arrays are usually more visually sensitive than a tight roof-mounted scheme.",
            "boundary_rules": "Boundary-facing arrays, side elevations and garden equipment often deserve the earliest visual and neighbour check in {council_name}.",
            "roof_rules": "Roof-mounted panels in {council_name} are usually easiest where they follow the roof slope cleanly and avoid highly visible or heritage-sensitive roof surfaces.",
            "materials_rules": "A tidy appearance and finish for panels and ancillary kit usually helps a solar scheme in {council_name} far more than visibly cluttered cabling, boxes or mismatched equipment.",
        },
        "restrictions": {
            "conservation_area": "Solar panels in conservation areas within {council_name} often need a closer design review where they affect visible roof slopes, walls or the wider character of the area.",
            "listed_building": "Solar works to listed buildings or buildings in their curtilage in {council_name} usually need a more careful planning and heritage consent check.",
        },
    },
    "windows-and-doors": {
        "defaults_pd": "Across {county_name}, window and door work is usually simplest on the planning permission route when it stays close to like-for-like replacement and does not materially alter the size, position, appearance or privacy impact of existing openings.",
        "defaults_rules": {
            "height_rules": "Changing the height of openings or creating new upper-level windows is usually much more sensitive than routine replacement joinery.",
            "depth_rules": "Projection, reveal depth and grouped opening changes can affect whether the work still reads as simple replacement rather than an elevation redesign.",
            "boundary_rules": "Side-facing upper-floor windows, new front openings and privacy impacts often become the key local pressure points for this kind of work.",
            "roof_rules": "If the project includes rooflights or roof-facing windows, it should be checked against the separate roof alteration route rather than treated as standard joinery replacement.",
            "materials_rules": "Frame profile, colour, material and detailing can all matter where the building has a stronger architectural rhythm or a more sensitive setting.",
        },
        "local_pd": "In {council_name}, window and door work is usually easiest to keep off the formal planning permission route when it stays close to like-for-like replacement and avoids new openings, stronger privacy impacts or a material change to the elevation.",
        "local_rules": {
            "height_rules": "In {council_name}, new or enlarged openings that change the height of windows and doors are usually more sensitive than straightforward replacement joinery, especially at upper levels or on visible elevations.",
            "depth_rules": "Projection, bay-style build-outs and grouped opening changes can make window and door work in {council_name} feel more like an elevation redesign than a simple replacement.",
            "boundary_rules": "Privacy, side-facing upper-floor windows and visually assertive front-elevation changes are common local pressure points in {council_name}.",
            "roof_rules": "Rooflights or roof-facing openings linked to a joinery project in {council_name} should usually be checked against the separate roof alteration route as well.",
            "materials_rules": "Frame proportions, colour, material choice and overall appearance usually matter most in {council_name} where the building or street has a stronger character that the new joinery should still respect.",
        },
        "restrictions": {
            "conservation_area": "Window and door changes in conservation areas within {council_name} often face tighter design control where they affect visible elevations or traditional detailing.",
            "listed_building": "Listed buildings in {council_name} usually need listed building consent or a more careful heritage review before window and door changes are assumed to be straightforward.",
            "article4_notes": "Article 4 directions can matter for visible joinery changes in some areas, particularly where character-based controls remove the simpler fallback route.",
        },
    },
}

COUNTY_PROFILE_PD_SUFFIXES = {
    "garages": {
        "metro": "On tighter urban plots, frontage dominance and vehicle access often become the real planning pressure points before garage floor area does.",
        "coastal": "Visible frontages and more open plots can make roof form, materials and street impact more sensitive than a simple garage sketch suggests.",
        "rural": "Larger plots can still create planning issues if a garage starts to read as a second building rather than a clearly subordinate domestic outbuilding.",
        "standard": "The planning route is usually strongest when the garage looks like a subordinate domestic building rather than a second focal point on the plot.",
    },
    "hard-surfaces": {
        "metro": "Smaller front gardens and tighter highway relationships usually make drainage, crossover design and visual dominance more important in denser streets.",
        "coastal": "Frontage character and exposed plots can make drainage detail and surface appearance more visible than homeowners often expect.",
        "rural": "Level changes, runoff and the shift from soft landscaping to engineered parking space often matter more on wider plots than the paving product alone.",
        "standard": "The route is usually strongest where the drainage story, frontage appearance and parking layout all work together rather than being solved separately.",
    },
    "heat-pumps": {
        "metro": "In denser streets, neighbour amenity, side-passage siting and visible plant clutter usually become more important than headline unit size alone.",
        "coastal": "More exposed elevations and open views can make siting and screening feel more sensitive than a simple compact-unit assumption suggests.",
        "rural": "Open plots can still create planning pressure where sound travel, long views or visually exposed service runs make the installation feel less discreet.",
        "standard": "The route is usually strongest when the unit, screen and pipework read as one restrained domestic installation rather than added plant equipment.",
    },
    "hmos": {
        "metro": "In busier urban authorities, shared-housing concentration, refuse management and frontage impact often shape the answer as much as the internal layout.",
        "coastal": "Mixed residential and visitor-heavy areas can make neighbour amenity, servicing and concentration questions more locally sensitive than they first appear.",
        "rural": "Quieter residential streets can still react strongly to parking, refuse and comings-and-goings, so neighbour impact often matters earlier than expected.",
        "standard": "The strongest HMO route usually comes from treating policy, concentration, amenity and the supporting physical works as one joined-up planning question.",
    },
    "solar-panels": {
        "metro": "In denser streets, visible roof slopes, terrace rooflines and ancillary kit clutter often decide the planning route more quickly than panel count alone.",
        "coastal": "Open views and exposed roofscapes can make panel siting and visual integration feel more sensitive than a standard flush-fit assumption suggests.",
        "rural": "Open plots and wider roof visibility can make garden arrays, outbuilding roofs and ancillary equipment more important to the planning story.",
        "standard": "The route is usually strongest when the array, roof plane and supporting equipment feel integrated rather than layered onto the building afterward.",
    },
    "windows-and-doors": {
        "metro": "On denser streets, frontage rhythm, side-window privacy and visible joinery changes usually draw the earliest design scrutiny.",
        "coastal": "Prominent elevations and more exposed frontages can make appearance, detailing and visible material change matter more than a simple replacement assumption suggests.",
        "rural": "Village character, detached frontages and stronger building individuality can make proportions and detailing more important than homeowners often expect.",
        "standard": "The route is usually strongest when the joinery change still reads as part of the original elevation rather than a wider redesign of the frontage.",
    },
}

LOCAL_PD_VARIANTS = {
    "garages": [
        "The answer usually gets harder when the garage is pushed forward in the plot and starts to compete with the house on the street frontage.",
        "Boundary-hugging siting and a new crossover are often the two details most likely to pull a straightforward garage into a fuller review.",
        "Schemes are usually safer where the roof stays low and the access arrangement still feels practical and visually calm from the road.",
    ],
    "hard-surfaces": [
        "The route normally gets harder when a small front garden is turned into a broad parking surface without a convincing drainage and planting strategy.",
        "Schemes are usually safer where runoff, crossover detail and surface appearance have all been thought through together from the start.",
        "The planning pressure often rises when the frontage starts to read more like engineered parking than simple domestic surfacing.",
    ],
    "heat-pumps": [
        "The route normally gets harder when the unit is squeezed into a narrow side passage or ends up too close to the neighbour’s quieter garden space.",
        "Schemes are usually safer where screening, airflow and maintenance access have all been designed together rather than added one by one.",
        "A heat pump can look routine on paper but still struggle if the frontage position or noise story feels weak once the council sees the exact siting.",
    ],
    "hmos": [
        "The route usually gets harder when refuse, bike storage and comings-and-goings have clearly been left as afterthoughts rather than planned parts of the scheme.",
        "Schemes are normally safer where the council can see a coherent story on layout quality, neighbour amenity and how the property will actually operate day to day.",
        "The hardest cases often combine a change of use with extra rooms, pressure on parking and no convincing response to local concentration concerns.",
    ],
    "solar-panels": [
        "The route usually gets harder where the most efficient panel layout is also the most visually exposed roof slope or frontage.",
        "Schemes are generally safer where the mounting depth, cabling and inverter positions all support a clean overall appearance.",
        "A roof-mounted array can still raise planning issues if the visible roofline, ancillary kit or nearby heritage setting makes the installation feel more assertive than expected.",
    ],
    "windows-and-doors": [
        "The route usually gets harder when one joinery change becomes a wider redesign of the frontage or introduces a new overlooking point toward neighbours.",
        "Schemes are normally safer where proportions, frame profile and visible elevations are treated as one appearance question rather than separate product choices.",
        "A like-for-like replacement rarely causes the same planning pressure as grouped opening changes, taller glazing or a visibly reworked entrance arrangement.",
    ],
}


def _format_text(template: str, council_name: str, county_name: str, county_slug: str) -> str:
    return template.format(
        council_name=council_name,
        county_name=county_name,
        country_name=get_country_name(county_slug),
        householder_label=get_householder_label(county_slug),
        system_label=get_system_label(county_slug),
    )


def _append_sentence(base: str, extra: str) -> str:
    clean_base = " ".join(str(base or "").split()).strip()
    clean_extra = " ".join(str(extra or "").split()).strip()
    if not clean_extra:
        return clean_base
    return f"{clean_base} {clean_extra}"


def _stable_index(seed: str, total: int) -> int:
    if total <= 0:
        return 0
    return sum(ord(char) for char in (seed or "")) % total


def _county_profile(county_slug: str) -> str:
    if county_slug == "greater-london":
        return "metro"
    if county_slug in COASTAL_COUNTIES:
        return "coastal"
    if county_slug in RURAL_COUNTIES:
        return "rural"
    return "standard"


def _build_defaults(project_slug: str, county_name: str, county_slug: str) -> dict:
    copy = PROJECT_COPY[project_slug]
    profile = _county_profile(county_slug)
    profile_suffix = COUNTY_PROFILE_PD_SUFFIXES.get(project_slug, {}).get(profile, "")
    return {
        "last_verified": LAST_VERIFIED,
        "permitted_development": _append_sentence(
            _format_text(copy["defaults_pd"], county_name, county_name, county_slug),
            profile_suffix,
        ),
        "rules": {
            key: _format_text(value, county_name, county_name, county_slug)
            for key, value in copy["defaults_rules"].items()
        },
    }


def _build_local_entry(project_slug: str, county_name: str, county_slug: str, council: dict) -> dict:
    copy = PROJECT_COPY[project_slug]
    council_name = council["town_name"]
    variant_list = LOCAL_PD_VARIANTS.get(project_slug, [])
    variant = ""
    if variant_list:
        variant = variant_list[_stable_index(council["town_slug"], len(variant_list))]
    restrictions = {
        key: _format_text(value, council_name, county_name, county_slug)
        for key, value in copy["restrictions"].items()
    }
    entry = {
        "town_slug": council["town_slug"],
        "last_verified": LAST_VERIFIED,
        "permitted_development": _append_sentence(
            _format_text(copy["local_pd"], council_name, county_name, county_slug),
            variant,
        ),
        "rules": {
            key: _format_text(value, council_name, county_name, county_slug)
            for key, value in copy["local_rules"].items()
        },
        "restrictions": restrictions,
    }
    return entry


def main():
    projects = {project["slug"]: project for project in load_projects() if project["slug"] in TARGET_PROJECTS}
    councils_by_county = load_councils()

    generated_files = 0
    generated_entries = 0

    for project_slug in sorted(projects):
        project_dir = DATA_FOLDER / "rules" / project_slug
        project_dir.mkdir(parents=True, exist_ok=True)

        for county_slug, councils in councils_by_county.items():
            county_name = councils[0].get("county_name", county_slug.replace("-", " ").title()) if councils else county_slug.replace("-", " ").title()
            payload = {
                "defaults": _build_defaults(project_slug, county_name, county_slug),
                "rules": [
                    _build_local_entry(project_slug, county_name, county_slug, council)
                    for council in councils
                ],
            }

            output_path = project_dir / f"{county_slug}.json"
            output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            generated_files += 1
            generated_entries += len(councils)

    print(f"Generated county rule files: {generated_files}")
    print(f"Generated local rule entries: {generated_entries}")


if __name__ == "__main__":
    main()
