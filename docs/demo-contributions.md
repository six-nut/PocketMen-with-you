# Privacy-safe demo contributions

Public demos should make PocketMen easy to evaluate without exposing personal reference images or
shipping assets that contributors cannot redistribute.

## Allowed source material

Use one of the following:

- synthetic references created specifically for the demo;
- original artwork or photography owned by the contributor;
- public-domain material; or
- material with an explicit license that permits redistribution and transformation.

Do not submit private photos, generated pets derived from private photos, local Codex configuration,
credentials, or protected character assets without documented permission.

## Evidence to include

A reviewable demo should contain:

1. at least two permitted reference views;
2. a short provenance and license note;
3. the identity-lock summary and selected style preset;
4. the canonical base image;
5. the final contact sheet;
6. one directional preview and one `running` (working) preview; and
7. the validator JSON produced without external generation calls in CI.

## Suggested directory layout

```text
examples/demos/<demo-id>/
  README.md
  manifest.json
  references/
  canonical-base.png
  contact-sheet.png
  previews/
  validation.json
```

The demo README should explain the source rights, generation choices, and any limitations. The
manifest format is intentionally provisional until the schema proposed in Issue #3 is agreed.

## Review checklist

- Every input and output is safe to redistribute.
- No personal or secret-bearing files are present.
- The companion identity and motion are understandable from the included evidence.
- Unused atlas cells are transparent and deterministic validation passes.
- CI uses only checked-in synthetic fixtures and spends no image-generation credits.

When rights or privacy are unclear, leave the media out of the pull request and ask a maintainer
before publishing it.
