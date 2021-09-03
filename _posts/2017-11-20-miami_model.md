---
layout: post
title: Net Primary Productivity and the Miami Model
date: 2017-11-20
categories: models
use_math: true
---

I haven't been posting for a while as I now realise.
So here a new post about a fairly simple and/but old model to calculate the <a href="https://en.wikipedia.org/wiki/Primary_production#Gross_primary_production_and_net_primary_production" target="_blank">net primary productivity</a> (NPP), the so called *Miami Model* ([Lieth, 1973][1]):

\begin{align}
NPP(T) &= 3000\(1+\exp(1.315-0.119 T)) \\
NPP(P) &= 3000 (1-\exp(-0.000664 P)) \\
NPP &= \min(NPP(T),NPP(P))
\end{align}

After reading through the more recent literature, it turns out that the Miami-Model is still regarded as useful proxy for annual NPP.
Global NPP observations are available, for example the <a href="https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod17a3" target="_blank">Terra/MODIS Net Primary Production Yearly L4 Global 1km</a>.
But these are currently not available as *global* data set.
Instead you can download all tiles (i.e., chunks of 1km by 1km tiles).
I have no idea why, but apparently, nobody is interested in compiling it from the available tile data.
(Maybe a topic for another blog post?).
Anyways, here is what the annual NPP looks like for a present-day climatology, i.e. the <a href="https://crudata.uea.ac.uk/cru/data/hrg/tmc/" target="_blank">Ten Minute Climatology</a>.

![Annual Net Primary Productivity from 10' climatology temperature and precipitation](/assets/npp_10min.png)

Here is a simple Python implementation:
```python
import numpy as np
def miami_model(temp,prec,a=3000.,b=1.315,c=0.119,d=0.000664):
    npp_temp = a/(1.+np.exp(b-c*temp))
    npp_prec = a*(1.-np.exp(-d*prec))
    return np.fmin(npp_temp,npp_prec)
```


[1]: https://link.springer.com/article/10.1007%2FBF01536729 "Lieth, H. (1973), Primary production: Terrestrial ecosystems, Human Ecol., 1, 303–332."
