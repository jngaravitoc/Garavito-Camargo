---
layout: page
title: Research
permalink: /research/
nav_order: 2
---

I am interested in understanding what the structure and dynamics of galaxies can tell us about the properties of dark matter. To do this, I develop N-body simulations and analysis methods to identify observables that can inform us about the distribution and nature of dark matter. All my publications can be found through [ADS](https://ui.adsabs.harvard.edu/search/p_=0&q=%20%20author%3A%22garavito-camargo%22&sort=date%20desc%2C%20bibcode%20desc). Below I summarize the main research projects I have led or worked on with collaborators.

## The ongoing merger between the Milky Way and the LMC

With a mass of about 10–20% of that of the Milky Way, the LMC has just passed its first pericentric approach around the Galaxy. Its gravitational field is inducing perturbations in the Milky Way, opening an exciting opportunity to study how the galaxy’s dark matter behaves during a merger. As part of this response, the LMC induces a dark-matter wake in the Milky Way’s halo that trails the LMC. Such a wake is visible as an overdensity of Milky Way stars following the LMC. One of the first predictions of the properties of such a wake was presented in [Hunting for the Dark Matter Wake induced by the Large Magellanic Cloud](https://ui.adsabs.harvard.edu/abs/2019arXiv190205089G/abstract).

An illustration below shows the response of the Milky Way’s dark matter to the LMC as measured by Gaia and WISE. The dark matter halo is shown in purple, and the wake trailing the LMC is visible.

![All-sky view of the Milky Way-LMC interaction and associated wake]({{ site.baseurl }}/images/lmc-mw/PIA24571_fig2.jpg)

<p class="figure-source">Image credit: NASA/ESA/JPL-Caltech/Conroy et al., 2021</p>

## Observational characterization of the Milky Way's response to the LMC's passage

This work motivated the search for the stellar wake in Gaia data and other surveys. I have contributed to several such measurements in [Conroy et al. 2021](https://ui.adsabs.harvard.edu/abs/2021Natur.592..534C/abstract) and [Cavieres et al. 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...983...83C/abstract).

The gravitational torques from the LMC on the Milky Way also induce an apparent motion of halo stars with respect to the disk, known as reflex motion. This motion has been detected in Gaia data, and it has also been measured by surveys such as SDSS-V ([Chandra et al. 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...988..156C/abstract)).

The perturbations from the LMC on the Milky Way are also present in the circumgalactic medium, as studied by Chris Carr ([Carr et al. 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...982..188H/abstract)), and in the disk of the Milky Way, as discussed by collaborator [Chervin Laporte](https://sites.google.com/view/chervinfplaporte/home). See also [Laporte et al. 2018a](https://ui.adsabs.harvard.edu/abs/2018MNRAS.481..286L/abstract), [Laporte et al. 2018b](https://ui.adsabs.harvard.edu/abs/2018MNRAS.473.1218L/abstract), and [Stelea et al. 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...977..252S/abstract). 

These observational and theoretical studies have therefore put forward a new picture in which the Milky Way is in a state of disequilibrium.

## Constraining the nature of dark matter with the MW-LMC interaction

Excitingly, the disequilibrium state of the Milky Way offers a unique opportunity to study how dark matter behaves out of equilibrium. This includes the properties of the dark matter wake ([Foote et al., 2023](https://ui.adsabs.harvard.edu/abs/2023ApJ...954..163F/abstract)) and the distribution and kinematics of solar-neighborhood particles as studied by [Gurtina Besla](https://sites.google.com/view/thebeslagroup/home%20) in [Besla et al., 2019](https://ui.adsabs.harvard.edu/abs/2019JCAP...11..013B/abstract) and in [Smith-Orlik et al., 2023](https://ui.adsabs.harvard.edu/abs/2023JCAP...10..070S/abstract), which could potentially be detected through direct-detection methods.

The LMC also brings its own population of subhalos with different kinematics from those of the Milky Way. With [Arpit Arora](https://arpitarora.space/), we characterized the kinematical properties of LMC subhalos and predicted potential signatures in the Milky Way stellar stream population ([Arora et al., 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...974..286A/abstract)).

## Orbits of stellar tracers in a time-dependent Milky Way potential

The response of the Milky Way to the LMC has consequences for interpreting the dynamics of objects orbiting in the stellar halo of the Milky Way. Below I list a few examples of such consequences:

- Stellar streams: [Richard Brooks](https://dc-broo3.github.io/richardbrooks.github.io/) quantified the effect of the LMC on a large population of simulated streams. The perturbations induced by the LMC have also been linked to a range of dynamical consequences in [Brooks et al., 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...978...79B/abstract).
- Orbits of satellite galaxies: [Ekta Patel](https://www.ektapatelastro.com) led the study to reconstruct the orbits of Milky Way satellites, including perturbations from the LMC ([Patel et al., 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...893..121P/abstract)).
- Angular-momentum directions of halo tracers ([Garavito-Camargo et al., 2021b](https://ui.adsabs.harvard.edu/abs/2024ApJ...975..100G/abstract)).
- Measuring the mass of the Local Group using the timing argument ([Chamberlain et al., 2023](https://ui.adsabs.harvard.edu/abs/2023ApJ...942...18C/abstract)).
- Finding the origin of hyper-velocity stars ([Han et al., 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...982..188H/abstract)).

![Orbital poles clustering from LMC]({{ site.baseurl }}/images/LMC_sims_vpos_half.png)
<p class="figure-source">The apparent orbital poles clustering of halo particles induced by the LMC. Image credit: Garavito-Camargo et. al., 2021b</p>

## Methods to characterize galaxies in disequilibrium

I have developed and implemented new methods to characterize and interpret the degree of dynamical disequilibrium in galaxies. To do this, I use [Basis Function Expansions](https://ui.adsabs.harvard.edu/abs/2022MNRAS.510.6201P/abstract) (BFE). The animation below illustrates such decomposition in one of the dark matter halos of the MW-est suite of simulations. The response of the halo (left panel) to an external perturber is characterized and decomposed as a function of time using BFE. The evolution of harmonic modes of the expansion is shown in the right-hand panels.

![BFE decomposition of Halo340]({{ site.baseurl }}/images/lmc-mw/BFE_decomposition_Halo340_proj_XY.gif)
<p class="figure-source">Image credit: Darragh-Ford et al., 2026</p>

Such methods have allowed us to characterize the dark matter halo response to LMC-like satellites in the velocity fields of idealized simulations as shown by [Emily Cunningham](https://www.ecunningham-astro.com/) [Cunningham et al., 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...898....4C/abstract); and in the density field as shown in [Garavito-Camargo et al., 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...919..109G/abstract) and in cosmological simulations ([Arora et al., 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...988..190A/abstract); [Darragh-Ford et al., 2026](https://ui.adsabs.harvard.edu/abs/2025arXiv251102031D/abstract)).

## Beyond the Milky Way–LMC interaction
 
- The evolution of the M31-M33 barycenter [Patel et. al., 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...985..121P/abstract)
- The Segue 2 collision with the Cetus–Paca stream [Foote et. al., 2025](https://ui.adsabs.harvard.edu/abs/2025ApJ...979..171F/abstract)
- The origin of loopsided galaxies in the Illustris-TNG simulation [Varela et. al., 2023](https://ui.adsabs.harvard.edu/abs/2023MNRAS.523.5853V/abstract)
- Vertical perturbations in stellar disks by satellite galaxies [Garc\'ia-Codnde et. al., 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...683A..47G/abstract)
- Measuring the dark matter distribution in external galaxies [de Isidio et. al., 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...971...69D/abstract)
- The effect of M31 on the dark matter distriburion of the solar neighborhood [DeBrae et. al., 2025](https://ui.adsabs.harvard.edu/abs/2025arXiv250217565D/abstract)