from __future__ import annotations


BUILDING_REGS_GUIDE_BASE_URL = "https://buildingregsguide.co.uk"


BUILDING_REGS_DESTINATIONS = {
    "home": {
        "title": "BuildingRegsGuide",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/",
        "description": "Use the sister site for building control routes, inspection evidence, certificates and approved-document guidance.",
    },
    "extensions": {
        "title": "Extension building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/extensions-building-regulations/",
        "description": "Structure, insulation, drainage, fire safety, ventilation and completion evidence for extensions.",
    },
    "loft-conversions": {
        "title": "Loft conversion building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/loft-conversion-building-regulations/",
        "description": "Fire escape, stairs, structure, insulation, ventilation and roof-work evidence.",
    },
    "garage-conversions": {
        "title": "Garage conversion building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/garage-conversion-building-regulations/",
        "description": "Insulation, damp, ventilation, fire safety, structure and completion evidence for garage conversions.",
    },
    "outbuildings": {
        "title": "Outbuilding building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/outbuilding-building-regulations/",
        "description": "When an outbuilding, office or workshop moves from simple/exempt to building-control relevant.",
    },
    "garden-rooms": {
        "title": "Garden room building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/garden-room-building-regulations/",
        "description": "Garden office, services, sleeping use, size and certificate checks.",
    },
    "structural-alterations": {
        "title": "Structural alteration building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/structural-alteration-building-regulations/",
        "description": "Structural work, drawings, inspections, calculations and completion evidence.",
    },
    "windows-and-doors": {
        "title": "Windows and doors building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/windows-doors-building-regulations/",
        "description": "Glazing, thermal performance, ventilation and competent person certificate evidence.",
    },
    "electrical-work": {
        "title": "Electrical work building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/electrical-work-building-regulations/",
        "description": "Notifiable electrical work, competent person routes and certificate evidence.",
    },
    "drainage": {
        "title": "Drainage and waste building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/drainage-waste-building-regulations/",
        "description": "Drainage runs, waste, new bathrooms, kitchens, extensions and connection evidence.",
    },
    "heating": {
        "title": "Boiler and heating building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/projects/boiler-heating-building-regulations/",
        "description": "Heating work, competent person routes and completion certificate evidence.",
    },
    "regularisation": {
        "title": "Regularisation certificates",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/building-regulations/regularisation-certificate/",
        "description": "Use this when work has already happened and building regulations evidence may be missing.",
    },
    "completion-certificate": {
        "title": "Completion certificate evidence",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/building-regulations/completion-certificate/",
        "description": "What completion evidence is for and why it can matter later for sale, remortgage or proof.",
    },
    "competent-person": {
        "title": "Competent person schemes",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/building-regulations/competent-person-schemes/",
        "description": "When a registered installer can self-certify work and what certificate evidence to keep.",
    },
    "route-checker": {
        "title": "Building control route checker",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/tools/building-control-route-checker/",
        "description": "Choose whether the next conversation is full plans, building notice, competent person, regularisation or planning first.",
    },
    "planning-vs-regs": {
        "title": "Planning permission vs building regulations",
        "url": f"{BUILDING_REGS_GUIDE_BASE_URL}/building-regulations/planning-permission-vs-building-regulations/",
        "description": "Use this when the two approval systems are being mixed together.",
    },
}


PROJECT_TO_BUILDING_REGS_DESTINATION = {
    "house-extensions": "extensions",
    "single-storey-extensions": "extensions",
    "rear-extensions": "extensions",
    "side-extensions": "extensions",
    "wraparound-extensions": "extensions",
    "two-storey-extensions": "extensions",
    "loft-conversions": "loft-conversions",
    "dormer-extensions": "loft-conversions",
    "roof-lights": "loft-conversions",
    "garage-conversions": "garage-conversions",
    "outbuildings": "outbuildings",
    "garden-rooms": "garden-rooms",
    "temporary-buildings": "outbuildings",
    "windows-and-doors": "windows-and-doors",
    "hard-surfaces": "drainage",
    "driveways": "drainage",
    "dropped-kerbs": "drainage",
    "solar-panels": "electrical-work",
    "heat-pumps": "heating",
}


DOWNLOAD_TO_BUILDING_REGS_DESTINATION = {
    "planning-vs-building-regulations-checklist": "planning-vs-regs",
    "extension-planning-prep-checklist": "extensions",
    "garage-conversion-planning-checklist": "garage-conversions",
    "loft-conversion-planning-checklist": "loft-conversions",
    "outbuilding-planning-checklist": "outbuildings",
    "front-garden-driveway-planning-checklist": "drainage",
}


def destination_for_project(project_slug: str) -> dict:
    key = PROJECT_TO_BUILDING_REGS_DESTINATION.get(str(project_slug or "").strip(), "")
    return BUILDING_REGS_DESTINATIONS.get(key, {})


def destination_for_download(asset_slug: str) -> dict:
    key = DOWNLOAD_TO_BUILDING_REGS_DESTINATION.get(str(asset_slug or "").strip(), "")
    return BUILDING_REGS_DESTINATIONS.get(key, {})


def destination_by_key(key: str) -> dict:
    return BUILDING_REGS_DESTINATIONS.get(str(key or "").strip(), {})
