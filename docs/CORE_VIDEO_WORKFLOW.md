# Core production gates

These gates apply automatically to new short requests through the repository's
AGENTS.md, before the selected HyperFrames workflow plans shots and after it
renders. No repeated user instructions or approval questions are required.
This is an agent-driven workflow: scripts prepare evidence and validate records;
they do not claim to understand footage without actual agent review.

## General library before planning

Discovery order: `AMARILLO_LIBRARY_DIR`, `data/library`, then a single accessible
general-library path in earlier manifests. Relative paths resolve from the repo.
Explicit invalid/reserved paths fail instead of silently selecting another library.
Phase 2's `references/human-realism` and symlink aliases are rejected.

This workspace's gitignored `data/library` symlink points to:

`/Users/joydimapilis/Desktop/untitled folder/Startup Launch Videos`

Verified on 2026-09-23: 11 accessible MP4s. Earlier production records describe
347 files; that larger collection is not present at this path. Use the accessible
general references honestly; do not substitute movement research or claim all
347 were inspected. Other workspaces must configure their own path.

For each new request, the agent inventories this library, chooses relevant
filename terms, writes a JSON list such as
`[{"term":"Motion-5-","genre":"software_walkthrough"}]`, and runs:

```sh
.venv/bin/python scripts/inspect_library_slice.py --out videos/<name>/references --terms <terms.json>
```

Inspect the actual selected footage chronologically, including relevant scene
joins and pacing, with sheets as supporting evidence. Write
`videos/<name>/reference-review.json` with this shape (replace example findings
with actual observations; do not copy them as a completed review):

```json
{
  "library": "/absolute/path/to/general/library",
  "references": [
    {
      "source": "/absolute/path/to/general/library/example.mp4",
      "footage_reviewed": true,
      "relevance": "Why this reference fits the request",
      "pacing": "Observed timing and scene joins, with source timestamps",
      "techniques": "Observed useful visual or editorial techniques",
      "application": "How the new video will apply those principles"
    }
  ]
}
```

```sh
.venv/bin/python scripts/verify_reference_review.py videos/<name>/reference-review.json
```

Only then write the shot plan. The legacy `amarillo compose-brief` also requires
`--reference-review <record.json>` and validates it before writing a plan.
Missing media or incomplete findings do not pass. Selection/extraction alone
never sets `footage_reviewed` automatically.

## Reusable evidence

```sh
.venv/bin/python scripts/learn_from_loops.py --route interview --reference --audio
```

`selected`, `accepted`, and `approved` now work alongside `accept` and
`provisional`. Original decision labels, rejected prompts, errors, costs and
revision hypotheses are retained. Unverified, unscored, rejected, superseded,
unknown and segment-only selections cannot become whole-take model endorsements.
Recommendations return compatible successes/failures as `lessons` so the next
prompt can address known problems; scores remain subjective.

`latest.json` retains all recorded history; its previous bytes are archived under
`artifacts/learning/history/<sha256>.json` before refresh. Rows whose ledgers are
unavailable remain historical-only and cannot supply a verified recommendation.
`core.json` contains core-production runs and prompt memory only. Phase 2 computer
movement research stays in its existing ledgers and historical archive, excluded
from core recommendations even when an older combined snapshot is supplied.
Do not edit or delete the research clips/reviews to achieve this separation.

## One reverse-engineering document per MP4

After rendering, author one JSON production record for each final MP4. Keep the
record in the editable project. Required fields are nonempty Markdown strings:

| Field | Required content |
| --- | --- |
| `video` | Exact individual MP4 filename, including extension |
| `title` | Optional title |
| `structure` | Timed shots, purpose, source ranges, joins, audio/captions and ending |
| `prompts` | Actual source-image/video/audio prompts by shot; for deterministic work, the creative brief and relevant code entry points |
| `models_methods` | Endpoints/models/settings or deterministic tools and editable source paths |
| `routing_decisions` | Why each route was chosen, reference/learning evidence and alternatives |
| `revisions` | What changed, why, take IDs and selected ranges |
| `failed_attempts` | Rejected/failed attempts, findings, cost impact; explicit none if applicable |
| `final_learnings` | Reusable conclusions, limitations, verification evidence and cost summary |

Do not fill unknown facts with guesses. State what is unavailable and link the
surviving evidence. Include prompts inline, with source links for provenance.
Each record describes its own video even when it references shared experiments.

```sh
.venv/bin/python scripts/reverse_engineering.py write artifacts/final_outcome/demo/demo-a.mp4 videos/demo/demo-a.production.json
.venv/bin/python scripts/reverse_engineering.py write artifacts/final_outcome/demo/demo-b.mp4 videos/demo/demo-b.production.json
.venv/bin/python scripts/reverse_engineering.py write artifacts/final_outcome/demo/demo-c.mp4 videos/demo/demo-c.production.json
# Run the applicable encoded-video, audio, composition and perceptual checks.
.venv/bin/python scripts/reverse_engineering.py check artifacts/final_outcome/demo/demo-a.mp4 artifacts/final_outcome/demo/demo-b.mp4 artifacts/final_outcome/demo/demo-c.mp4
```

This produces `demo-a.reverse-engineering.md`, `demo-b.reverse-engineering.md`
and `demo-c.reverse-engineering.md` alongside the videos. Each has one MP4 identity
and its SHA-256. A different render invalidates the old document. The gate fails
on missing sections, unfinished placeholders, shared symlinks, another video's
document, or a mismatched hash. It verifies structure and identity, not the truth
of creative judgments; internal production review remains mandatory.

Existing core finalizers/verifiers call this gate before writing successful
verification or delivery records, including individual members of multi-video
batches. New finalizers must do the same. Persist its returned document path/hash
in the corresponding delivery manifest. A missing document means incomplete,
even when the render/decode succeeded. Re-finalizing an older video also requires
its individual document; this workflow update does not fabricate historical
documents or regenerate missing old media.
