# Security policy

## Supported versions

Security fixes target the latest release on `main`.

## Reporting a vulnerability

Please do not open a public issue for secrets exposure, command injection, unsafe archive extraction, or a vulnerability that could overwrite files outside the intended pet/repository directories. Use GitHub private vulnerability reporting when enabled, or contact the repository owner privately.

## Security boundaries

- Never print, persist, or commit API keys or GitHub tokens.
- The PocketMen skill must not call an external paid image API directly.
- External fallback generation requires explicit user confirmation.
- Pet installation is restricted to `${CODEX_HOME:-~/.codex}/pets/<pet-id>` after sanitizing the ID.
- Repository publishing checks the active GitHub CLI identity before pushing.
