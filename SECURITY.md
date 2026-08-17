# Security policy

## Supported versions

Security fixes target the latest release on `main`.

## Reporting a vulnerability

Please do not open a public issue for secrets exposure, command injection, unsafe archive extraction, or a vulnerability that could overwrite files outside the intended pet/repository directories. Use GitHub private vulnerability reporting when enabled, or contact the repository owner privately.

## Security boundaries

- The Local Engine requires no API key and must never inspect or print `OPENAI_API_KEY`.
- The public repository and CI must not contain personal reference photos.
- Optional Studio visual generation is not a prerequisite for local pet creation.
- A built-in image-generation transport failure must not automatically escalate to credential-bearing CLI/API fallbacks.
- Pet installation is restricted to `${CODEX_HOME:-~/.codex}/pets/<pet-id>` after sanitizing the ID.
- Existing pet directories are timestamp-backed up before replacement.
- Repository publishing checks the active GitHub CLI identity before pushing and never force-pushes by default.
- Skill runtime dependencies are isolated under the installed skill's `.venv`.
