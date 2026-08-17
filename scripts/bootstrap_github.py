from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION = "Create high-fidelity Codex companions from 2+ photos with local open-weight neural editing and no OpenAI API key."
TOPICS = [
    "codex", "openai-codex", "agent-skill", "codex-skill", "desktop-pet", "ai-pet",
    "spritesheet", "image-generation", "multimodal", "character-consistency", "pet-animation",
    "python", "open-source", "offline-first", "computer-vision",
    "local-ai", "flux2", "qwen-image", "image-editing", "neural-rendering",
]
REMOVED_TOPICS = ["companion", "creative-coding", "opencv"]
LABELS = [
    ("bug", "D73A4A", "Something is not working"),
    ("enhancement", "A2EEEF", "New feature or improvement"),
    ("good first issue", "7057FF", "Friendly entry point for new contributors"),
    ("help wanted", "008672", "Maintainers would welcome help"),
    ("design", "F9D0C4", "Visual identity, UX or style preset"),
    ("pet-quality", "FBCB0A", "Identity, motion or atlas quality"),
    ("skill", "1D76DB", "Codex skill behavior"),
    ("documentation", "0075CA", "Documentation improvement"),
]


def run(*args: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(args))
    return subprocess.run(args, cwd=ROOT, check=check, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def output(*args: str) -> str:
    cp = run(*args, capture=True)
    return cp.stdout.strip()


def ensure_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required tool not found: {name}")


def repo_exists(full: str) -> bool:
    cp = subprocess.run(["gh", "repo", "view", full, "--json", "name"], cwd=ROOT,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return cp.returncode == 0


def git_has_commit() -> bool:
    cp = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return cp.returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Safely publish PocketMen with You to GitHub")
    ap.add_argument("--owner", default="six-nut")
    ap.add_argument("--repo", default="PocketMen-with-you")
    ap.add_argument("--public", action="store_true")
    ap.add_argument("--confirm-public", action="store_true")
    ap.add_argument("--release", default="")
    ap.add_argument("--allow-existing", action="store_true")
    args = ap.parse_args()

    if args.public and not args.confirm_public:
        raise SystemExit("Refusing public publication without --confirm-public")

    ensure_tool("git")
    ensure_tool("gh")
    run("gh", "auth", "status")
    login = output("gh", "api", "user", "--jq", ".login")
    if login != args.owner:
        raise SystemExit(f"GitHub CLI active account is {login!r}, expected {args.owner!r}. Use `gh auth switch --user {args.owner}`.")

    full = f"{args.owner}/{args.repo}"
    existing = repo_exists(full)
    if existing and not args.allow_existing:
        raise SystemExit(f"Repository {full} already exists. Re-run with --allow-existing only after inspecting it; this script never force-pushes.")

    if not (ROOT / ".git").exists():
        run("git", "init", "-b", "main")
    run("git", "config", "user.name", args.owner, check=False)
    # Do not overwrite an existing user.email; only set a repo-local noreply fallback when missing.
    cp = subprocess.run(
        ["git", "config", "user.email"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        check=False,
    )
    if not cp.stdout.strip():
        run("git", "config", "user.email", f"{args.owner}@users.noreply.github.com")
    run("git", "add", ".")
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=False)
    if diff.returncode != 0:
        run("git", "commit", "-m", "feat: launch PocketMen with You")
    elif not git_has_commit():
        raise SystemExit("Nothing staged and no existing commit; repository is unexpectedly empty")

    if not existing:
        create = ["gh", "repo", "create", full, "--source=.", "--remote=origin", "--push", "--description", DESCRIPTION, "--disable-wiki"]
        create.append("--public" if args.public else "--private")
        run(*create)
    else:
        # Existing repo: push normally, never force.
        remotes = output("git", "remote")
        if "origin" not in remotes.splitlines():
            run("git", "remote", "add", "origin", f"https://github.com/{full}.git")
        run("git", "push", "-u", "origin", "main")

    edit = ["gh", "repo", "edit", full, "--description", DESCRIPTION,
            "--enable-issues=true", "--enable-projects=true", "--delete-branch-on-merge=true"]
    for topic in REMOVED_TOPICS:
        edit.extend(["--remove-topic", topic])
    for topic in TOPICS:
        edit.extend(["--add-topic", topic])
    run(*edit)

    for name, color, description in LABELS:
        run("gh", "label", "create", name, "--repo", full, "--color", color,
            "--description", description, "--force")

    if args.release:
        # Create only if not already present.
        cp = subprocess.run(["gh", "release", "view", args.release, "--repo", full], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if cp.returncode != 0:
            run("gh", "release", "create", args.release, "--repo", full, "--generate-notes", "--title", f"PocketMen with You {args.release}")

    print("\nPublished/configured:", f"https://github.com/{full}")
    print("Manual finishing step: upload assets/social-preview.png in GitHub Settings → Social preview.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
