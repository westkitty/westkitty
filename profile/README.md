# Public profile manifest

`projects.yml` is an explicit public allowlist for the West Kitty GitHub profile.

Absence is the default. A repository is not eligible for the public profile merely because it exists, is active, or is visible to an authenticated workflow. It must be deliberately listed with `public: true`, a canonical repository, an honest state, and a verification label.

The profile generator must never discover account repositories and publish them automatically. This prevents private, unreleased, internal, duplicate, or superseded work from leaking through statistics, project cards, configuration examples, or generated output.

`Dexter Approved` is a manual evidence judgement. Recency, stars, build success, or confident README prose cannot assign it automatically.
