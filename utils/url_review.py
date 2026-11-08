"""Validate a review-only dossier. Never interpret it as migration approval."""
from datetime import datetime, timezone
import re
from utils.content_contracts import ContractError


def validate_review_only(card):
    if card.get('outcome') not in {'keep', 'unknown'} or card.get('actionable_migration') is not False or card.get('approval') is not None:
        raise ContractError('This dossier is review-only; no migration or retirement is authorized')
    if card.get('backlinks') != 'unknown':
        raise ContractError('No backlink assessment was supplied for this dossier')


def validate_normalization(card):
    validate_review_only(card)
    observed = card['current_http']
    checked = datetime.fromisoformat(observed['observed_at'])
    if checked.tzinfo is None or checked > datetime.now(timezone.utc):
        raise ContractError('HTTP observation needs a real, non-future timestamp with timezone')
    if not re.fullmatch('[a-f0-9]{64}', observed.get('body_sha256') or ''):
        raise ContractError('HTTP evidence needs its captured body digest')
    if card['classification'] == 'observed-trailing-slash-normalization':
        target = card['url'].rstrip('/') + '/'
        chain = observed.get('header_chain', [])
        if (observed['url'] != card['url'] or observed['method'] != 'GET' or observed['curl_exit'] != 0
                or observed['status'] != 200 or observed['redirect_count'] != 1
                or observed['effective_url'] != target or card['normalized_static_url'] != target
                or observed['body_sha256'] != card['static_lf_sha256']
                or len(chain) != 3 or not re.fullmatch(r'HTTP/\S+ 301 .+', chain[0])
                or chain[1].lower() != ('location: ' + target).lower()
                or not re.fullmatch(r'HTTP/\S+ 200 .+', chain[2])):
            raise ContractError('A canonical hint or successful final response is not proof of a direct HTTP 301 normalization')
