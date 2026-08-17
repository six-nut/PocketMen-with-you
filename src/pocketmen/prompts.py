from __future__ import annotations

STYLE_TEXT = {
    "soft-real": (
        "high-fidelity photorealistic companion portrait, natural material response, realistic fur/hair/skin, "
        "clean studio lighting, faithful anatomy and proportions"
    ),
    "hero-chibi": (
        "premium 3D toy-like chibi character, approximately 2.7 to 3 heads tall, handsome/cute balance, "
        "soft physically based materials, crisp silhouette, expressive but identity-faithful face"
    ),
    "plush": (
        "premium collectible plush interpretation, soft fibers, rounded proportions, warm tactile materials, "
        "still clearly recognizable as the same subject"
    ),
    "capsule-creature": (
        "polished original pocket-companion creature design, compact playful proportions, high-end 3D collectible finish"
    ),
    "auto": "identity-faithful polished companion character",
}

GENERIC_ACTIONS = {
    "idle": "calm neutral full-body pose, relaxed and friendly, facing mostly forward",
    "running-right": "dynamic natural running pose toward the right, full body visible, believable limb motion",
    "running-left": "dynamic natural running pose toward the left, full body visible, believable limb motion",
    "waving": "friendly greeting pose directed toward the viewer",
    "jumping": "compact energetic vertical jump, whole body airborne and readable",
    "failed": "gentle humorous disappointed pose, slightly slumped but still warm and endearing",
    "waiting": "attentive waiting pose, slight forward lean, expectant but calm",
    "running": "actively working on a compact plain laptop, focused task-execution pose; this is not physical running",
    "review": "carefully reviewing a plain sheet or blueprint, thoughtful checking pose",
}

PERSON_ACTIONS = {
    **GENERIC_ACTIONS,
    "waving": "friendly greeting pose, one hand clearly waving toward the viewer",
    "failed": "gentle humorous disappointed pose, slight crouch or hand-to-head gesture, ready to try again",
}

ANIMAL_ACTIONS = {
    **GENERIC_ACTIONS,
    "waving": "cute natural greeting pose, one front paw raised toward the viewer without human-like anatomy",
    "running": "sitting or crouching beside a compact plain laptop with one paw near it, focused companion-at-work pose",
    "review": "leaning attentively over a plain sheet or blueprint as if inspecting it, natural animal anatomy",
}


def action_for(state: str, subject_type: str) -> str:
    if subject_type == "person":
        return PERSON_ACTIONS[state]
    if subject_type == "animal":
        return ANIMAL_ACTIONS[state]
    return GENERIC_ACTIONS[state]


def _identity(identity_notes: str | None) -> str:
    notes = (identity_notes or "").strip()
    if not notes:
        return "Preserve the exact identity, face/head structure, markings, colors, proportions, and fixed accessories from the references."
    return (
        "Identity lock — these details must remain unchanged across every output: "
        + notes
        + ". Preserve them exactly; do not redesign them."
    )


def canonical_prompt(*, style: str, subject_type: str, identity_notes: str | None, chroma_hex: str) -> str:
    return f"""Purpose: create the canonical master asset for a tiny animated desktop companion.
Subject: use the supplied reference images as identity evidence for the same {subject_type if subject_type != 'auto' else 'subject'}.
Identity: {_identity(identity_notes)}
Look: {STYLE_TEXT[style]}.
Composition: one complete subject only, centered, whole body visible, generous empty margin, no crop, no scene.
Background: perfectly flat opaque {chroma_hex} studio chroma background, uniform corner-to-corner, with no gradient and no floor horizon.
Lighting: soft neutral studio light; keep important eye/fur/hair/accessory colors faithful to the references.
Constraints: no text, no logos, no watermark, no border, no UI, no speech bubble, no floating decoration, no ground shadow, no extra person/animal/limb/object. Do not change identity."""


def state_prompt(
    state: str,
    *,
    style: str,
    subject_type: str,
    identity_notes: str | None,
    chroma_hex: str,
) -> str:
    action = action_for(state, subject_type)
    return f"""Purpose: create one animation key pose for the same Codex desktop companion.
Subject: the exact same subject as the supplied canonical/reference images.
Identity: {_identity(identity_notes)}
Required action: {action}.
Look: keep exactly the same visual style as the canonical image: {STYLE_TEXT[style]}.
Consistency: preserve face/head, hair/fur, eye color, markings, body scale, clothing, collar/jewelry and all fixed accessories; do not add or remove identity-defining details.
Composition: one complete subject only, centered, full body inside frame, readable silhouette at small size, generous empty margin.
Background: perfectly flat opaque {chroma_hex}, uniform corner-to-corner, no floor, no gradient.
Constraints: no text, logo, watermark, border, UI, speed lines, glow halo, detached effects, scenery, extra subject, duplicated limbs, cropped ears/hands/paws/feet/tail. Do not redesign the character."""


NEGATIVE_PROMPT = (
    "different identity, different face, different fur pattern, different eye color, missing accessories, extra accessories, "
    "extra limbs, duplicated body, cropped body, text, logo, watermark, UI, scenery, complex background, shadow, blur"
)
