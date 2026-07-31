from pathlib import Path

import yaml

from scripts.validate_profile import collect_errors

ROOT = Path(__file__).resolve().parents[1]


def test_repository_profile_is_valid():
    assert collect_errors(ROOT) == []


def test_public_manifest_contains_only_explicit_public_entries():
    manifest = yaml.safe_load((ROOT / "profile" / "projects.yml").read_text())
    assert manifest["projects"]
    assert all(project["public"] is True for project in manifest["projects"])


def test_current_orbit_is_small_and_allowlisted():
    manifest = yaml.safe_load((ROOT / "profile" / "projects.yml").read_text())
    projects = {project["id"]: project for project in manifest["projects"]}
    current = manifest["current_orbit"]
    assert len(current) <= 3
    assert all(projects[item]["public"] and projects[item]["featured"] for item in current)


def test_dexter_approval_is_not_assigned_casually():
    manifest = yaml.safe_load((ROOT / "profile" / "projects.yml").read_text())
    approved = [project for project in manifest["projects"] if project["status"] == "dexter-approved"]
    for project in approved:
        assert project.get("release_url")
        assert project["verification"] in {"ci-and-local", "ci-and-e2e", "ci-and-release"}
