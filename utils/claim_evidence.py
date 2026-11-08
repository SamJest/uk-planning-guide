"""Claim-scoped evidence inside the existing source registry; no legal inference."""
from datetime import date
import hashlib
import json
import re
from urllib.parse import urlsplit

from core.paths import ROOT
from utils.content_contracts import ContractError

NATIONS = {'england', 'wales', 'scotland', 'northern-ireland'}
KINDS = {'service_information', 'planning_scope', 'historical_context',
         'national_rule', 'local_policy', 'article4_applicability', 'unresolved_check'}
IDENTIFIER = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
MEASUREMENT = re.compile(r'\d+(?:\.\d+)?\s*(?:metres?|meters?|m²|m2|mm\b|m\b|%|occupiers?|households?)', re.I)
POLICY_PATH = ROOT / 'data/canary/wave1-corpus.json'


def _fail(message):
    raise ContractError(message)


def _object(value, label):
    if not isinstance(value, dict):
        _fail(f'{label} must be an object')


def _date(value, label, nullable=False):
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        _fail(f'{label} must be an ISO date')
    try:
        return date.fromisoformat(value)
    except ValueError:
        _fail(f'{label} must be an ISO date')


def _ids(values, label):
    if not isinstance(values, list) or any(not isinstance(v, str) or not IDENTIFIER.fullmatch(v) for v in values):
        _fail(f'{label} must contain normalized identifiers')
    if len(values) != len(set(values)):
        _fail(f'{label} contains duplicate identifiers')


def _primary_url(value):
    parsed = urlsplit(str(value or ''))
    host = parsed.hostname or ''
    return (parsed.scheme == 'https' and not parsed.username and not parsed.password
            and (host in {'gov.uk', 'gov.wales', 'gov.scot'}
                 or host.endswith(('.gov.uk', '.gov.wales', '.gov.scot'))))


def validate_source_propositions(source):
    if 'propositions' not in source:
        return
    if not isinstance(source['propositions'], list):
        _fail('Source propositions must be a list')
    seen = set()
    for proposition in source['propositions']:
        _object(proposition, 'Source proposition')
        required = {'proposition_id', 'text', 'kind', 'scope', 'checked_at', 'as_of',
                    'effective_from', 'effective_to', 'locator', 'checked_by',
                    'verification_status', 'capture_kind', 'capture_sha256'}
        if required - proposition.keys():
            _fail('Source proposition lacks provenance fields')
        if proposition.keys() - required - {'property_scope'}:
            _fail('Source proposition has unsupported attribution/metadata fields')
        pid = proposition['proposition_id']
        if not isinstance(pid, str) or not IDENTIFIER.fullmatch(pid) or pid in seen:
            _fail('Source proposition ID is invalid or duplicated')
        seen.add(pid)
        if proposition['kind'] not in KINDS - {'unresolved_check'}:
            _fail(f'{pid}: unsupported proposition kind')
        if not isinstance(proposition['text'], str) or not proposition['text'].strip():
            _fail(f'{pid}: proposition needs text')
        scope = proposition['scope']
        _object(scope, f'{pid} scope')
        if {'jurisdiction', 'authority_id', 'project_ids', 'rule_ids'} - scope.keys():
            _fail(f'{pid}: incomplete scope')
        if scope.keys() - {'jurisdiction', 'authority_id', 'project_ids', 'rule_ids'}:
            _fail(f'{pid}: unsupported scope fields')
        if scope['jurisdiction'] not in NATIONS or scope['jurisdiction'] != source['jurisdiction']:
            _fail(f'{pid}: a proposition needs one matching nation; UK is not a legal fallback')
        if scope['authority_id'] != source['authority_id']:
            _fail(f'{pid}: proposition authority differs from its source')
        _ids(scope['project_ids'], f'{pid} projects')
        _ids(scope['rule_ids'], f'{pid} rules')
        checked = _date(proposition['checked_at'], f'{pid} checked_at')
        if checked > date.today() or checked > _date(source['last_checked_at'], 'Source last_checked_at'):
            _fail(f'{pid}: invented or future source-check date')
        as_of = _date(proposition['as_of'], f'{pid} as_of', nullable=True)
        start = _date(proposition['effective_from'], f'{pid} effective_from', nullable=True)
        end = _date(proposition['effective_to'], f'{pid} effective_to', nullable=True)
        if as_of and as_of > checked or start and end and end < start:
            _fail(f'{pid}: inconsistent evidence dates')
        if proposition['kind'] == 'historical_context' and (not as_of or str(as_of.year) not in proposition['text']):
            _fail(f'{pid}: historical evidence must retain its date qualification')
        if proposition['checked_by'] != 'codex-source-check':
            _fail(f'{pid}: unsupported reviewer attribution; no professional sign-off is recorded')
        if proposition['capture_kind'] not in {'web-read-bundle', 'http-body'}:
            _fail(f'{pid}: unsupported evidence capture')
        if not isinstance(proposition['capture_sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', proposition['capture_sha256']):
            _fail(f'{pid}: invalid capture digest')
        if not isinstance(proposition['locator'], str) or not proposition['locator'].strip():
            _fail(f'{pid}: an exact source locator is required')
        if proposition['verification_status'] not in {'verified', 'unverified'}:
            _fail(f'{pid}: unsupported evidence status')
        if proposition['verification_status'] == 'verified' and not _primary_url(source['url']):
            _fail(f'{pid}: verified claims require an official primary source')
        if MEASUREMENT.search(proposition['text']) and proposition['kind'] not in {'national_rule', 'local_policy', 'article4_applicability'}:
            _fail(f'{pid}: a numeric permission answer needs a rule proposition')
        if proposition['kind'] == 'national_rule' and not scope['project_ids']:
            _fail(f'{pid}: numeric/national rules require an explicit project')
        if proposition['kind'] == 'article4_applicability' and proposition['verification_status'] == 'verified':
            property_scope = proposition.get('property_scope', {})
            if (source['source_type'] != 'article_4' or not scope['authority_id'] or not start
                    or start > checked or end and end < checked
                    or property_scope.get('status') != 'verified'
                    or not _primary_url(property_scope.get('direction_url'))
                    or not _primary_url(property_scope.get('map_url'))
                    or not property_scope.get('withdrawn_rights')
                    or not property_scope.get('match_record_id')):
                _fail(f'{pid}: Article 4 applicability needs a signed direction, map, rights, effective date and verified property match')


def validate_page_evidence_shape(page):
    if page.get('evidence_version') != 1:
        return
    checked = _date(page.get('evidence_checked_at'), 'Page evidence_checked_at')
    if checked > date.today():
        _fail('Page evidence date cannot be in the future')
    if page.get('jurisdiction_support') not in {'scoped', 'unsupported'}:
        _fail('Evidence record must declare jurisdiction support')
    if page.get('verification_scope') != 'authority_context':
        _fail('This canary does not establish property-specific planning rights')
    if any(page.get(key) for key in ('reviewer', 'reviewed_by', 'reviewer_name', 'reviewer_credentials')):
        _fail('No independent reviewer attribution is evidenced for this canary')
    prefix = page['route_path'].strip('/').split('/')[0]
    if prefix in NATIONS and prefix != page['jurisdiction']:
        _fail('Route and record have different jurisdictions')
    assertions = page['claims'] + page['unique_local_facts']
    for assertion in assertions:
        _object(assertion, 'Evidence assertion')
        if assertion.get('kind') not in KINDS or assertion.get('evidence_status') not in {'verified', 'unverified'}:
            _fail('Assertion needs a typed kind and evidence status')
        refs = assertion.get('evidence_refs')
        if not isinstance(refs, list):
            _fail('Assertion evidence_refs must be a list')
        seen = set()
        for ref in refs:
            _object(ref, 'Evidence reference')
            if set(ref) != {'source_id', 'proposition_id'}:
                _fail('Evidence reference needs source_id and proposition_id only')
            _ids([ref['source_id']], 'Evidence source')
            _ids([ref['proposition_id']], 'Evidence proposition')
            pair = (ref['source_id'], ref['proposition_id'])
            if pair in seen:
                _fail('Duplicate claim evidence reference')
            seen.add(pair)
        text = assertion.get('text', assertion.get('fact', ''))
        if not isinstance(text, str) or not text.strip():
            _fail('Evidence assertion needs text')
        if assertion['evidence_status'] == 'unverified':
            if assertion['kind'] != 'unresolved_check' or refs or MEASUREMENT.search(text):
                _fail('Unverified assertions must remain unresolved, without numeric answers or verified bindings')
            if not any(marker in text.lower() for marker in ('not verified', 'not checked', 'unknown', 'unresolved')):
                _fail('An unresolved assertion must explicitly state what is unknown')
        elif not refs or assertion['kind'] == 'unresolved_check':
            _fail('Verified assertions need proposition references')
        if page['jurisdiction_support'] == 'unsupported' and assertion['evidence_status'] != 'unverified':
            _fail('Unsupported jurisdictions cannot emit verified planning answers')
    if page['jurisdiction_support'] == 'unsupported' and (page['index_status'] != 'noindex' or page['verified_at'] is not None):
        _fail('Unsupported fixture cannot be published as a verified/indexable guide')
    if page['verified_at'] is not None and (page['verified_at'] != page['evidence_checked_at']
            or not assertions or any(a['evidence_status'] != 'verified' for a in assertions)):
        _fail('Page verification date requires complete claim evidence from that check')


def validate_record_evidence(page, registry):
    validate_page_evidence_shape(page)
    if page.get('evidence_version') != 1:
        return
    for assertion in page['claims'] + page['unique_local_facts']:
        if assertion['evidence_status'] != 'verified':
            continue
        for ref in assertion['evidence_refs']:
            source_id = ref['source_id']
            if source_id not in page['source_ids'] or source_id not in assertion['source_ids'] or source_id not in registry:
                _fail('Claim evidence uses an undeclared/missing source')
            source = registry[source_id]
            validate_source_propositions(source)
            matches = [p for p in source.get('propositions', []) if p['proposition_id'] == ref['proposition_id']]
            if len(matches) != 1:
                _fail('Claim evidence references a missing proposition')
            proposition = matches[0]
            scope = proposition['scope']
            if proposition['verification_status'] != 'verified' or source['status'] != 'active':
                _fail('Unverified/unavailable source evidence cannot verify a claim')
            if scope['jurisdiction'] != page['jurisdiction']:
                _fail('Claim evidence has the wrong jurisdiction')
            if scope['authority_id'] is not None and scope['authority_id'] != page['authority_id']:
                _fail('Claim evidence belongs to the wrong authority')
            if 'fact' in assertion and scope['authority_id'] != page['authority_id']:
                _fail('A national source is not a verified local fact')
            if scope['project_ids'] and page['project_id'] not in scope['project_ids']:
                _fail('Claim evidence has the wrong project; a generic page cannot assume one')
            if scope['rule_ids'] and page['rule_id'] not in scope['rule_ids']:
                _fail('Claim evidence has the wrong rule topic')
            text = assertion.get('text', assertion.get('fact'))
            if ' '.join(text.split()) != ' '.join(proposition['text'].split()) or assertion['kind'] != proposition['kind']:
                _fail('Claim text/kind does not match the cited proposition')
            if proposition['checked_at'] != page['evidence_checked_at']:
                _fail('Page evidence date does not match its proposition review')


def record_fingerprint(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def validate_evidence_migration(records):
    policy = json.loads(POLICY_PATH.read_text(encoding='utf-8'))
    for record in records:
        if record.get('evidence_version') == 1:
            continue
        expected = policy['legacy_record_sha256'].get(record['route_path'])
        if not expected or record_fingerprint(record) != expected:
            _fail(f"{record['route_path']}: new or changed legacy record must migrate to evidence_version 1")
