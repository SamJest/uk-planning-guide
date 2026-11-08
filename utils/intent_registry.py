"""Typed search jobs for contracted generation; never a legacy retirement list."""
from dataclasses import asdict, dataclass

from utils.content_contracts import ContractError, JURISDICTIONS, PAGE_FAMILIES, IDENTIFIER_PATTERN


@dataclass(frozen=True)
class IntentKey:
    jurisdiction: str
    authority_id: str | None
    project_id: str | None
    rule_topic: str | None
    user_question: str
    role: str


QUESTIONS = {
    'local_project': 'proposal-permission-route',
    'project_guide': 'proposal-permission-route',
    'local_rule': 'rule-applicability',
    'rule_guide': 'rule-applicability',
    'authority_profile': 'authority-planning-services',
    'national_guide': 'national-rule-guidance',
    'tool': 'interactive-task',
    'workflow': 'process-steps',
    'news': 'dated-news',
    'data_report': 'dataset-analysis',
}

# Stable identities for existing functions. New functional pages must declare
# their task ID; a new URL alone cannot establish a different user job.
FUNCTIONAL_IDS = {
    ('tool', '/tools/'): 'tools-directory',
    ('tool', '/england/tools/planning-route-check/'): 'planning-route-check',
    ('tool', '/my-planning-project/'): 'saved-project-workspace',
    ('workflow', '/workflows/house-extension-planning/'): 'house-extension-planning',
    ('news', '/updates/phase-0-integrity-repair/'): 'phase-zero-integrity-repair',
    ('data_report', '/england/data/council-profile-database/'): 'council-profile-evidence',
}


def intent_key(record):
    nation, role = record.get('jurisdiction'), record.get('page_family')
    if nation not in JURISDICTIONS or role not in PAGE_FAMILIES:
        raise ContractError('Intent needs an explicit supported jurisdiction and page role')
    values = [record.get(k) for k in ('authority_id', 'project_id', 'rule_id')]
    if any(v is not None and (not isinstance(v, str) or not IDENTIFIER_PATTERN.fullmatch(v)) for v in values):
        raise ContractError('Intent scope must use single normalized identifiers, not county/name guesses')
    question = QUESTIONS[role]
    if role in {'tool', 'workflow', 'news', 'data_report'}:
        task = record.get('functional_intent_id') or FUNCTIONAL_IDS.get((role, record['canonical_path']))
        if not isinstance(task, str) or not IDENTIFIER_PATTERN.fullmatch(task):
            raise ContractError('A new functional page needs a normalized functional_intent_id, not a URL-derived distinction')
        question += ':' + task
    elif not any(values):
        # Unscoped directories have route identity, not a legal-answer claim.
        question += ':' + record['canonical_path'].strip('/').replace('/', ':')
    return IntentKey(nation, *values, question, role)


def validate_new_intents(records):
    seen = {}
    for record in records:
        key = intent_key(record)
        if record['index_status'] != 'index' or record['route_path'] != record['canonical_path']:
            continue
        if key in seen:
            raise ContractError(f'Duplicate canonical intent: {seen[key]} and {record["route_path"]}')
        seen[key] = record['route_path']


def review_registry(records):
    validate_new_intents(records)
    return [dict(route_path=r['route_path'], canonical_path=r['canonical_path'],
                 index_status=r['index_status'], intent=asdict(intent_key(r)),
                 scope='contracted-generation-only; existing public pages require separate review')
            for r in sorted(records, key=lambda row: row['route_path'])]
