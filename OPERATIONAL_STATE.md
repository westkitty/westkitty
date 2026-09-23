# Operational State: West Kitty Profile System

<!-- operational-state:metadata
{
  "schema_version": 1,
  "project_id": "westkitty-profile",
  "project_name": "West Kitty Profile System",
  "project_root": ".",
  "artifact_path": "site/index.html",
  "state_revision": 2,
  "last_updated": "2026-09-23T01:34:54Z",
  "current_baseline": {
    "identity": "westkitty/westkitty main before interactive profile delivery: bfea984bbd2fad2b216896bf386029edb6bbe6de",
    "state": "current-baseline",
    "last_verified": "2026-09-22T16:11:53Z"
  },
  "scope_boundaries": [
    "GitHub profile composition and generated-profile configuration in westkitty/westkitty",
    "Interactive public profile source in site/",
    "Published mirror at westkitty.github.io/westkitty/"
  ],
  "linked_parent_state": null
}
-->

## 1. Project Identity and Scope

- **Project ID:** `westkitty-profile`
- **Purpose:** Present West Kitty / Stinky Weasel Productions as a deliberately authored public workbench while preserving the existing galaxy identity and SVG generator.
- **Project type:** GitHub profile repository plus static interactive Pages surface.
- **Primary artifact:** `site/index.html`
- **Target:** Modern desktop/mobile browsers, GitHub profile README, GitHub Pages.
- **Canonical authority:** Explicit user instruction, repository-local config, generated assets, and verified browser behavior.
- **Governed:** `README.md`, `README.profile.md`, `config.yml`, `site/`, and `/westkitty/` deploy mirror.
- **Not governed:** Existing root content of `westkitty/westkitty.github.io`, private repos, unrelated repos.

## 2. Current Baseline

- Existing generated galaxy profile remains the GitHub-facing visual layer.
- New canonical interactive source lives under `site/`.
- Baseline inspected at `bfea984bbd2fad2b216896bf386029edb6bbe6de`.
- Profile README points to `https://westkitty.github.io/westkitty/`.
- Direct Pages on `westkitty/westkitty` is disabled; isolated user-Pages mirror is the delivery route.

## 3. Artifact Contract

Two coordinated surfaces: a lightweight GitHub README using generated galaxy SVGs, and a dependency-free static site using semantic HTML, responsive CSS, vanilla JS, and 2D canvas. The site includes pointer-reactive motion, live public-repo telemetry with a truthful static fallback, quiet/reduced-motion behavior, keyboard-operable controls, and a debug overlay. The mirror may only occupy `westkitty.github.io/westkitty/`; the root Pages site must remain untouched.

## 4. Active Invariants

- **INV-001 — Preserve galaxy identity:** `Build / Make / Ship`, deep-space palette, and the generated SVG system remain recognizable across README and site.
- **INV-002 — Protect root Pages:** no root file in `westkitty.github.io` may be replaced for this project.
- **INV-003 — Expression cannot block content:** canvas, motion, and network data are enhancements; reading, navigation, and repository access must remain available without them.

## 5. Verified Working Behavior

- **VER-001 — Responsive rendering:** exact staged source rendered at 1440x1000 and 390x844 in headless Chromium with no horizontal overflow and no page/console JS errors.
- **VER-002 — Core controls:** quiet mode toggles and reports state; principle tabs switch content; `D` toggles debug overlay; degraded GitHub-network path renders static repository fallback.
- **VER-003 — Copy/authorship gates:** public copy lint passed for site and README; web-authorship audit passed, with only intentional non-blocking notes for loading-state pulse and galaxy gradients.

## 6. Known Not Working

No confirmed in-scope source failure is open.

## 7. Implemented but Unverified

- **UNV-001 — Live GitHub telemetry:** implementation exists; isolated browser QA blocks external GitHub API access. Validate on deployed public origin.
- **UNV-002 — Public Pages route:** publishable mirror prepared; validate after the Pages-host commit is delivered.

## 8. Unknown or Evidence-Stale State

Native Pages enablement for `westkitty/westkitty` remains disabled. The available GitHub connector does not expose the repository Pages administration mutation. This does not block the isolated mirror route.

## 9. Pending Work

- **PND-001 — Optional native project Pages:** low priority, non-blocking. Only revisit if the user later wants to replace the isolated mirror architecture.

## 10. Active Decisions, Defaults, and Prohibitions

- **DEC-001 — Dependency-free surface:** semantic HTML, CSS, vanilla JS, 2D canvas. Do not add a framework/effects dependency without a concrete need.
- **DEC-002 — Canonical vs mirror:** canonical source is `westkitty/westkitty/site/`; deploy mirror is `westkitty/westkitty.github.io/westkitty/`.
- **DEC-003 — Telemetry truthfulness:** public repository total comes from the GitHub profile endpoint; activity/language mix is explicitly labeled as based on the latest 100 repos.

## 11. Validation and Evidence Matrix

| ID | Claim | State | Evidence | Recheck trigger |
|---|---|---|---|---|
| INV-001 | Galaxy / Build-Make-Ship identity preserved | requested | Existing config/generated assets + staged site | Brand/config change |
| INV-002 | Root Pages site remains untouched | requested | Existing root site inspected | Hosting/deploy change |
| VER-001 | Desktop/mobile layout has no horizontal overflow | verified | Chromium assertions | HTML/CSS/JS change |
| VER-002 | Core controls and degraded fallback operate | verified | Chromium interaction assertions | Interaction/feed change |
| VER-003 | Public copy and authorship gates pass | verified | Deterministic lint/audit | Public-copy/style change |
| UNV-001 | Live GitHub API telemetry works on public origin | implemented-unverified | Source path present | Fetch/API change |
| UNV-002 | Pages route is publicly served | implemented-unverified | Mirror prepared | Deploy change |

## 12. Current Change Scope and Impact Radius

- **Allowed:** profile README composition, profile config, interactive `site/`, isolated `/westkitty/` mirror.
- **Must remain unchanged:** generator implementation, tests, existing workflow, license, unrelated repo content, private repos, root user Pages site.
- **Potential impact:** generated SVG appearance after config change; README presentation; mirror route.
- **Mandatory checks:** YAML parse, JS syntax, copy lint, authorship audit, desktop/mobile browser QA, path-scoped Git diff, public-route check.
- **Repair class:** bounded profile-system upgrade.

## 13. Compact Revision Log

### Revision 2 — 2026-09-23

- Established coordinated README + interactive Pages architecture.
- Protected the existing user-Pages root.
- Verified responsive layout and core interaction paths.
- Kept live GitHub telemetry and public deployment explicitly unverified until post-delivery checks.
