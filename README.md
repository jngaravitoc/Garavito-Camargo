Garavito-Camargo
==========================

Security and Maintenance
------------------------

This repository uses a hardened automation posture for GitHub Actions:

- Workflow actions are pinned to immutable commit SHAs in [.github/workflows/update-recent-pubs.yml](.github/workflows/update-recent-pubs.yml) and [.github/workflows/site-ci.yml](.github/workflows/site-ci.yml).
- Dependabot is enabled via [.github/dependabot.yml](.github/dependabot.yml) for weekly updates to GitHub Actions, Bundler, and pip dependencies.
- Site CI validates the Jekyll build and runs checks for the ADS updater script before automation changes are merged.

Design Authoring Guide
----------------------

Page TOC behavior

- Long pages using the standard page layout auto-generate an "On This Page" table of contents from `h2` and `h3` headings.
- TOC appears automatically when at least two section headings are present.

Figure markup pattern

Use framed figures with caption metadata for research visuals:

```html
<figure class="figure-frame">
	<img src="{{ site.baseurl }}/images/lmc-mw/PIA24571_fig2.jpg" alt="All-sky projection showing perturbations induced by the LMC.">
	<figcaption>
		Milky Way-LMC interaction map.
		<span class="figure-source">Source: Conroy et al. data products.</span>
		<span class="figure-takeaway">Takeaway: the perturbation pattern is coherent across halo tracers.</span>
	</figcaption>
</figure>
```

Optional full-width media wrapper

```html
<div class="full-width-media">
	<figure>
		<img src="..." alt="...">
		<figcaption>...</figcaption>
	</figure>
</div>
```
