# Clicked 404 recovery analysis

- Missing clicked URLs: 30
- Recorded clicks: 91
- Existing same-authority parent pages: 30
- Redirects authorised: 0
- Restorations authorised: 0

Every missing URL adds a combined rule-intent segment beneath an existing project/county/authority page. The parent is a safe visible recovery destination, but it is broader than the missing intent and therefore is not automatically an equivalent redirect target.

| Missing path | Clicks | Existing recovery page | Missing intent | Decision |
|---|---:|---|---|---|
| `/annexes/greater-london/bromley/planning-permission/` | 3 | `/annexes/greater-london/bromley/` | `planning-permission` | Manual equivalence/content-contract review |
| `/annexes/greater-london/ealing/planning-permission/` | 3 | `/annexes/greater-london/ealing/` | `planning-permission` | Manual equivalence/content-contract review |
| `/annexes/greater-london/redbridge/planning-permission-depth-limits/` | 3 | `/annexes/greater-london/redbridge/` | `planning-permission-depth-limits` | Manual equivalence/content-contract review |
| `/annexes/hampshire/winchester/planning-permission-height-limits/` | 3 | `/annexes/hampshire/winchester/` | `planning-permission-height-limits` | Manual equivalence/content-contract review |
| `/annexes/lincolnshire/east-lindsey/planning-permission-article-4/` | 4 | `/annexes/lincolnshire/east-lindsey/` | `planning-permission-article-4` | Manual equivalence/content-contract review |
| `/change-of-use/cambridgeshire/huntingdonshire/boundary-rules-article-4/` | 3 | `/change-of-use/cambridgeshire/huntingdonshire/` | `boundary-rules-article-4` | Manual equivalence/content-contract review |
| `/demolition/hertfordshire/hertsmere/boundary-rules/` | 4 | `/demolition/hertfordshire/hertsmere/` | `boundary-rules` | Manual equivalence/content-contract review |
| `/driveways/yorkshire/leeds/planning-permission-permitted-development/` | 3 | `/driveways/yorkshire/leeds/` | `planning-permission-permitted-development` | Manual equivalence/content-contract review |
| `/driveways/yorkshire/north-yorkshire/planning-permission-boundary-rules/` | 3 | `/driveways/yorkshire/north-yorkshire/` | `planning-permission-boundary-rules` | Manual equivalence/content-contract review |
| `/fences-and-walls/greater-london/harrow/distance-from-boundary/` | 3 | `/fences-and-walls/greater-london/harrow/` | `distance-from-boundary` | Manual equivalence/content-contract review |
| `/fences-and-walls/surrey/elmbridge/height-limits-depth-limits/` | 3 | `/fences-and-walls/surrey/elmbridge/` | `height-limits-depth-limits` | Manual equivalence/content-contract review |
| `/garage-conversions/greater-london/brent/article-4/` | 3 | `/garage-conversions/greater-london/brent/` | `article-4` | Manual equivalence/content-contract review |
| `/garage-conversions/greater-london/waltham-forest/article-4/` | 3 | `/garage-conversions/greater-london/waltham-forest/` | `article-4` | Manual equivalence/content-contract review |
| `/garage-conversions/hampshire/basingstoke-and-deane/article-4/` | 4 | `/garage-conversions/hampshire/basingstoke-and-deane/` | `article-4` | Manual equivalence/content-contract review |
| `/garage-conversions/hampshire/gosport/maximum-height/` | 3 | `/garage-conversions/hampshire/gosport/` | `maximum-height` | Manual equivalence/content-contract review |
| `/garden-rooms/greater-london/lewisham/permitted-development-depth-limits/` | 3 | `/garden-rooms/greater-london/lewisham/` | `permitted-development-depth-limits` | Manual equivalence/content-contract review |
| `/house-extensions/greater-london/bexley/planning-permission-boundary-rules/` | 2 | `/house-extensions/greater-london/bexley/` | `planning-permission-boundary-rules` | Manual equivalence/content-contract review |
| `/house-extensions/greater-london/hillingdon/height-limits-distance-from-boundary/` | 2 | `/house-extensions/greater-london/hillingdon/` | `height-limits-distance-from-boundary` | Manual equivalence/content-contract review |
| `/house-extensions/greater-london/hillingdon/height-limits/` | 3 | `/house-extensions/greater-london/hillingdon/` | `height-limits` | Manual equivalence/content-contract review |
| `/house-extensions/hampshire/hart/boundary-rules-permitted-development/` | 3 | `/house-extensions/hampshire/hart/` | `boundary-rules-permitted-development` | Manual equivalence/content-contract review |
| `/outbuildings/buckinghamshire/buckinghamshire/article-4/` | 4 | `/outbuildings/buckinghamshire/buckinghamshire/` | `article-4` | Manual equivalence/content-contract review |
| `/outbuildings/greater-london/barking-and-dagenham/permitted-development-listed-buildings/` | 3 | `/outbuildings/greater-london/barking-and-dagenham/` | `permitted-development-listed-buildings` | Manual equivalence/content-contract review |
| `/outbuildings/greater-london/lewisham/article-4/` | 2 | `/outbuildings/greater-london/lewisham/` | `article-4` | Manual equivalence/content-contract review |
| `/outbuildings/surrey/woking/article-4/` | 3 | `/outbuildings/surrey/woking/` | `article-4` | Manual equivalence/content-contract review |
| `/outbuildings/worcestershire/bromsgrove/article-4/` | 3 | `/outbuildings/worcestershire/bromsgrove/` | `article-4` | Manual equivalence/content-contract review |
| `/porches/essex/basildon/article-4/` | 3 | `/porches/essex/basildon/` | `article-4` | Manual equivalence/content-contract review |
| `/porches/essex/colchester/permitted-development-boundary-rules/` | 3 | `/porches/essex/colchester/` | `permitted-development-boundary-rules` | Manual equivalence/content-contract review |
| `/porches/greater-london/barking-and-dagenham/boundary-rules-roof-alterations/` | 3 | `/porches/greater-london/barking-and-dagenham/` | `boundary-rules-roof-alterations` | Manual equivalence/content-contract review |
| `/side-extensions/greater-london/hillingdon/permitted-development-article-4/` | 3 | `/side-extensions/greater-london/hillingdon/` | `permitted-development-article-4` | Manual equivalence/content-contract review |
| `/single-storey-extensions/dorset/bournemouth-christchurch-and-poole/height-limits-permitted-development/` | 3 | `/single-storey-extensions/dorset/bournemouth-christchurch-and-poole/` | `height-limits-permitted-development` | Manual equivalence/content-contract review |

## Safe next decision

For each row, choose one of two evidence-backed treatments: prove the parent is a true substitute and implement a real HTTP redirect on a supporting host, or restore the exact URL from a reviewed content contract with authority/rule sources. Until then, keep the genuine 404 response and offer the parent as navigation. Do not use a client-side meta-refresh bridge as a substitute for an HTTP redirect.
