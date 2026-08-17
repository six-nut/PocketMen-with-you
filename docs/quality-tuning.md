# Quality tuning

## Best input references

For a single subject, 2–3 complementary references work best:

- one clear front or three-quarter head/face view;
- one full-body or near-full-body view;
- optional side view or a shot that clearly shows important accessories/markings.

Avoid using several nearly identical blurry images. Do not include unrelated people/animals if cleaner references exist.

## Identity notes

Use concise visible facts, for example:

`young man; swept black hair; narrow oval face; silver hoop earrings; black turtleneck; slim athletic build; white-gray running shoes`

or:

`black short-haired cat; round body; large upright ears; amber-gold irises with green inner tones; pale pink cord collar with wooden beads and silver bells`

Identity notes should describe stable appearance, not private/sensitive attributes.

## Style

For real pets, start with `soft-real`.

For people who should become a premium cartoon avatar, use `hero-chibi`.

For an original collectible toy look, use `plush`.

## If one state drifts

1. improve the identity notes;
2. remove weak/conflicting reference images;
3. rerun with `--quality max`;
4. switch to `qwen-image-edit-2511` when compatible;
5. keep the same seed when comparing changes.

## If VRAM is tight

Keep CPU offload enabled. Use `balanced` or `draft`. Close other GPU-heavy applications. If neural inference still fails, allow deterministic fallback.
