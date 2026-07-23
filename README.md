Garavito-Camargo
==========================

Security and Maintenance
------------------------

This repository uses a hardened automation posture for GitHub Actions:

- Workflow actions are pinned to immutable commit SHAs in [.github/workflows/update-recent-pubs.yml](.github/workflows/update-recent-pubs.yml) and [.github/workflows/site-ci.yml](.github/workflows/site-ci.yml).
- Dependabot is enabled via [.github/dependabot.yml](.github/dependabot.yml) for weekly updates to GitHub Actions, Bundler, and pip dependencies.
- Site CI validates the Jekyll build and runs checks for the ADS updater script before automation changes are merged.
