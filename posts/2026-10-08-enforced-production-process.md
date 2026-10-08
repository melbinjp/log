---
title: From a project manual to an enforced production process
description: What a conductor's development records establish, which production stages remain to be enforced, and how the next build can prove them.
date: 2026-10-08
slug: enforced-production-process
---

Jules Prompts' conductor defines how a project should move from an idea to an accepted result.
Its development records also show a remaining gap: written requirements can be skipped, and
passing repository checks does not establish that a product or continuing duty meets its
acceptance conditions.

This account draws on an Antigravity analysis dated 7 October 2026, checked against
project records and primary sources. The development observations come from dated internal
reviews. Their raw evidence is private, so readers cannot independently rerun those episodes.

## What the conductor currently supplies

The conductor is a multi-file Agent Skill: an entry point, focused guidance and templates.
It covers objectives, acceptance, planning, ownership, dependencies, execution, verification,
change and handover. It works through the project's existing records rather than requiring
a new project-management service.

The repository also contains executable checks for packaging, references, generated copies,
fixture integrity, schedule-source rules and other bounded properties. These checks are real
capabilities. Their coverage does not extend to enforcing the complete production process.

The project's [vision record](https://github.com/melbinjp/jules-prompts/blob/main/docs/VISION.md)
documents the distinction. Trials included missing work-item owners, an incomplete handover
and printing before a booking was confirmed, despite instructions requiring those prerequisites.
The record also acknowledges variation between runs and limited evidence from real delivery.

## The production stages named in the analysis

The analysis explicitly lists seventeen stages:

```text
1. Requirement extraction
-> 2. Domain modeling
-> 3. Schema design
-> 4. Auth & session architecture
-> 5. State management
-> 6. API design
-> 7. Business logic
-> 8. Error handling
-> 9. Payment integration
-> 10. Third-party webhooks
-> 11. Security hardening
-> 12. Responsive UI design
-> 13. Accessibility
-> 14. Performance/caching
-> 15. Migration safety
-> 16. Deployment pipeline
-> 17. Telemetry & monitoring
```

This list is the starting inventory for the next build. It is not a universal count of
everything production requires. A project without payments or webhooks needs a justified
disposition for those stages. Other projects can require additional stages. Dependencies
can also require returning to an earlier decision.

The required progression is explicit:

```text
Evaluate stage -> Verify evidence -> Advance when prerequisites pass
       |
       +-> Failure or missing evidence: stop, fix, verify independently, re-evaluate.
```

Each stage needs an input, a responsible actor, concrete acceptance and evidence from the
actual result. The verifier must be independent of its author. A failed or unverified
prerequisite must prevent advancement. These are proposed acceptance requirements, not a
claim that the complete sequence already runs.

## What the development records establish

### Written rules were not always applied

The conductor already required native work authority, independent review and inspection of
actual user journeys. In one software-directory project, a goals ledger was mistaken for
active tracking, and acceptance missed customer-facing environment explanations and a
purchase promotion nested inside an already sponsored card.

The records distinguish a failure to follow an existing requirement from a missing concrete
gate. Adding clearer guidance does not retroactively verify the project. Adoption needs an
operator who can find and execute the next ready package, with its prerequisites, acceptance
and evidence, in the project's actual work authority.

### Browser checks missed realistic interface behaviour

A 1 October review records that earlier browser checks missed the effect of long
submitted descriptions on card layout. The owner found the visual defect. Passing checks
had not established the intended experience with representative content.

Subsequent inspections identified customer-facing staging copy, repeated refund explanations and
competing purchase actions. On 7 October, a staged correction was recorded with one concise
refund consequence, linked terms and one tool-opening action. That receipt describes the
staged correction; it does not establish production release or owner acceptance of the
whole product.

The practical acceptance condition follows from these observations: inspect actual default,
loading, failure, recovery and expanded states at supported sizes, using realistic content.
Keep the task and material consequences clear in the default view, with supporting detail
available when needed.

### Scheduling did not establish completion of a duty

A continuing evening review depended on one agent service. When provider access failed,
scheduled retries did not complete the review. After the executor was removed, the scheduled
process could still run without performing the intended duty.

An October 4 operating review also found a life organising system with a registered tick and
connected information sources, but no active model component or node procedures for the named
review tasks. Those are dated operating observations, not a current audit of every service.

The distinction is observable: a task invocation or clean exit is evidence of process
execution. Completion requires evidence that the intended duty happened. The operating
record needs its operator, mode, trigger, result and missed-run response.

### Replacement execution still needed demonstrated limits

The October 4 review considered a replacement coding agent. The record did not establish
that unattended outward actions would remain denied. It explicitly treated an approval
configuration as insufficient proof of that boundary.

Before unattended execution is accepted, action limits need demonstrated refusal of
unauthorised sends, publication, spending and destructive changes. The record establishes
an unfinished verification requirement, not an observed permission-bypass incident.

### Trial outcomes varied

The [trial report](https://github.com/melbinjp/jules-prompts/blob/main/docs/trials/report.md)
records differing outcomes between runs. It also records a provider quota interruption and
contradictory detailed and summary review verdicts.

These findings support repeated evaluation, explicit interruption handling and verdicts that
agree with their underlying evidence. They do not supply a measured probability that an
arbitrary future project will succeed or fail.

The current fixture inventory and historical trial coverage are different records: the
[fixture index](https://github.com/melbinjp/jules-prompts/blob/main/fixtures/index.json)
records 168 planted defects, while the historical trial scored 146. Defects added later are
not part of the earlier result. Recount the current inventory from a repository checkout:

```bash
python -c "
import json
from pathlib import Path
source = Path('fixtures/index.json')
text = source.read_text(encoding='utf-8')
index = json.loads(text)
items = index['fixtures']
counts = [x['planted'] for x in items]
print(sum(counts))
"
```

The observed output was `168`. [Release documentation](https://github.com/melbinjp/jules-prompts/blob/main/docs/RELEASE.md)
keeps the evidence and supported scope visible.

## What the research supports

[Lost in the Middle](https://arxiv.org/html/2307.03172v3) found that the position of relevant
information affected performance on multi-document question answering and key-value retrieval
for the tested models. That is a reason to test how reliably a worker uses its assigned
context. It does not establish that context length caused a particular conductor failure.

[ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) defines a product-quality model
with nine characteristics. [ISO 21502:2020](https://www.iso.org/standard/74947.html) provides
project-management guidance. [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
provides requirements for verifying application-security controls, and [SLSA](https://slsa.dev/spec/)
defines supply-chain assurance requirements.

These sources support applying explicit requirements and collecting relevant evidence.
Mentioning a standard in guidance does not establish conformity. The conductor's vision
record already acknowledges that its summaries do not certify a result and that some
regulated work requires qualified people.

## The next build task

The next goal in Jules Prompts is to make each applicable stage an enforced prerequisite.
The [README section](https://github.com/melbinjp/jules-prompts#from-an-idea-to-a-production-system-the-next-build-task)
now records the complete stage inventory and its proposed evidence requirements. Publishing
these requirements does not release a runtime that enforces them.

First, inspect the existing checks and execution tools. Map every named stage to a working
capability or a demonstrated gap. Reuse the project's native records, effective checks and
settled action authority.

Then demonstrate the smallest missing enforcement on a bounded real project:

- Fail a stage deliberately and show that dependent work cannot advance.
- Interrupt execution and show that state and standing limits survive resumption.
- Repair the defect and obtain independent verification before advancing.
- Inspect the actual user or operator journey against its acceptance conditions.
- Demonstrate handover, monitoring and failure response for any continuing duty.

A controller can enforce the transitions it is given. Its acceptance criteria still need
review, and its checks still need evidence that they detect the intended failures. This
demonstration would establish the tested capability under stated conditions. Production
acceptance remains a separate result.
