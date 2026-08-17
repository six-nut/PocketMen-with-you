# Style presets

## soft-real

Use for real pets and identity-faithful people. Neural mode asks the local editor for natural fur/hair/skin, faithful eye colors and accessories, and neutral studio light. Deterministic fallback preserves source pixels with mild enhancement.

## hero-chibi

Use for a handsome/cute premium avatar. Neural mode requests a polished 3D toy-like chibi around 2.7–3 heads tall while preserving face, hair, markings and fixed accessories. Deterministic fallback uses only a conservative proportion warp and should not be described as equivalent quality.

## plush

Use for collectible plush aesthetics. Neural mode generates real material/fiber detail and new poses; deterministic mode smooths and rounds the supplied cutout.

## capsule-creature

Use for original pocket-companion creatures. PocketMen's red/yellow Companion Capsule is original project branding; never request or reproduce third-party capture-ball trademarks.

## auto

The agent should infer the safest style from the user's intent. For real animals without an explicit cartoon request, prefer `soft-real`. For people explicitly asking for cute/cool cartoon treatment, prefer `hero-chibi`.
