#!/usr/bin/env python3
"""Validate the public West Kitty profile manifest and rendered README.

The profile is allowlist-only. Repository discovery must never decide what is
safe to publish.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_STATUSES = {
    "dexter-approved",
    "under-inspection",
    "prototype",
    "maintenance",
    "paused",
    "superseded",
    "archived",
}

ALLOWED_VERIFICATION = {
    "ci-and-local",
    "build-and-tests",
    "ci-and-e2e",
    "ci-and-release",
    "build-and-targeted-tests",
    "project-verifier",
}

STRONG_APPROVAL_EVIDENCE = {
    "ci-and-local",
    "ci-and-e2e",
    "ci-and-release",
}

# Split strings keep the validator from flagging its own source while still
# detecting accidental reintroduction of the original demo identity.
PLACEHOLDER_MARKERS = {
    "Nyx" + " Orion",
    "Stellar" + " Labs",
    "galaxy" + "-dev",
    "nyx@" + "stellarlabs.dev",
    "nyx" + "orion.dev",
}

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".txt", ".svg"}
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}
REPOSITORY_LINK_RE = re.compile(r"https://github\.com/(westkitty/[A-Za-z0-9_.-]+)")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a YAML mapping")
    return data


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def collect_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    manifest_path = root / "profile" / "projects.yml"
    config_path = root / "config.yml"
    readme_path = root / "README.md"

    for required in (manifest_path, config_path, readme_path):
        if not required.exists():
            errors.append(f"missing required file: {required.relative_to(root)}")
    if errors:
        return errors

    try:
        manifest = load_yaml(manifest_path)
        config = load_yaml(config_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]

    projects = manifest.get("projects")
    if not isinstance(projects, list) or not projects:
        errors.append("profile/projects.yml must contain at least one public project")
        projects = []

    policy = manifest.get("policy", {})
    max_featured = policy.get("maximum_featured_projects", 6)
    if not isinstance(max_featured, int) or max_featured < 1:
        errors.append("policy.maximum_featured_projects must be a positive integer")
        max_featured = 6

    ids: set[str] = set()
    repos: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    featured_repos: set[str] = set()

    for index, project in enumerate(projects):
        prefix = f"projects[{index}]"
        if not isinstance(project, dict):
            errors.append(f"{prefix} must be a mapping")
            continue

        project_id = project.get("id")
        repository = project.get("repository")
        status = project.get("status")
        verification = project.get("verification")

        if not isinstance(project_id, str) or not project_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        if project_id in ids:
            errors.append(f"duplicate project id: {project_id}")
        ids.add(project_id)
        by_id[project_id] = project

        if not isinstance(repository, str) or not repository.startswith("westkitty/"):
            errors.append(f"{prefix}.repository must be a westkitty owner/name path")
        elif repository in repos:
            errors.append(f"duplicate repository: {repository}")
        else:
            repos.add(repository)

        # Private and unreleased work must be omitted, not represented with a
        # false visibility flag inside the public manifest.
        if project.get("public") is not True:
            errors.append(f"{project_id}: public manifest entries must set public: true")

        if project.get("featured") is True:
            if project.get("canonical") is not True:
                errors.append(f"{project_id}: featured projects must be canonical")
            if isinstance(repository, str):
                featured_repos.add(repository)

        if status not in ALLOWED_STATUSES:
            errors.append(f"{project_id}: unknown status {status!r}")
        if verification not in ALLOWED_VERIFICATION:
            errors.append(f"{project_id}: unknown verification label {verification!r}")

        if status == "dexter-approved":
            if verification not in STRONG_APPROVAL_EVIDENCE:
                errors.append(f"{project_id}: Dexter Approved requires strong evidence")
            if not project.get("release_url"):
                errors.append(f"{project_id}: Dexter Approved requires a release_url")

        if status == "superseded" and not project.get("successor"):
            errors.append(f"{project_id}: superseded projects require a successor")

    if len(featured_repos) > max_featured:
        errors.append(
            f"featured project count {len(featured_repos)} exceeds maximum {max_featured}"
        )

    current_orbit = manifest.get("current_orbit", [])
    if not isinstance(current_orbit, list):
        errors.append("current_orbit must be a list")
        current_orbit = []
    if len(current_orbit) > 3:
        errors.append("current_orbit may contain at most three projects")
    for project_id in current_orbit:
        project = by_id.get(project_id)
        if project is None:
            errors.append(f"current_orbit references unknown project: {project_id}")
        elif project.get("public") is not True or project.get("featured") is not True:
            errors.append(f"current_orbit project must be public and featured: {project_id}")

    config_projects = config.get("projects", [])
    if not isinstance(config_projects, list):
        errors.append("config.yml projects must be a list")
        config_projects = []
    config_repos = {
        item.get("repo")
        for item in config_projects
        if isinstance(item, dict) and isinstance(item.get("repo"), str)
    }
    if config_repos != featured_repos:
        missing = sorted(featured_repos - config_repos)
        extra = sorted(config_repos - featured_repos)
        if missing:
            errors.append(f"config.yml is missing featured repositories: {missing}")
        if extra:
            errors.append(f"config.yml contains repositories outside the public manifest: {extra}")

    readme = readme_path.read_text(encoding="utf-8")
    for required_phrase in (
        "Andrew Dolby",
        "Dexter",
        "Stinky Weasel Productions",
        "The Weasel Standard",
        "Current Orbit",
    ):
        if required_phrase not in readme:
            errors.append(f"README.md is missing required semantic text: {required_phrase}")

    if 'alt="Dexter' not in readme:
        errors.append("README.md must provide meaningful Dexter portrait alternative text")

    linked_repositories = set(REPOSITORY_LINK_RE.findall(readme))
    unlisted_links = linked_repositories - repos - {"westkitty/westkitty"}
    if unlisted_links:
        errors.append(f"README.md links repositories outside the public allowlist: {sorted(unlisted_links)}")

    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in PLACEHOLDER_MARKERS:
            if marker.lower() in text.lower():
                errors.append(
                    f"demo placeholder {marker!r} remains in {path.relative_to(root)}"
                )

    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        print("Profile validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Profile validation passed: public allowlist, evidence states, and identity checks are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
