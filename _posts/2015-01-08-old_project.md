---
layout: post
title: New old project
date: 2015-01-08
categories: github, code, java, diploma thesis, models
---

<img src="https://cloud.githubusercontent.com/assets/5938262/5614071/46ef5958-94ed-11e4-80ce-964830fb1eb7.gif" width="30%" alt="spiral wave" align="right">
A few days ago, I uploaded a very old (almost ancient) code project to [Github](https://github.com/mkrapp/rde-solver).
It is a relic of my studies at the university (2007!) and I have used this code for my [diploma thesis](/assets/diplomarbeit_mario_krapp.pdf).
After tweaking the code quite a bit, I managed to get it running and spitting out this nice spiral wave (which makes this blog look a lot more colourful than originally I intended).

From the entire Java files I produced back than I included only the one that have a good purpose (like the one   above).
I also had to add a build file for `ant` because originally, this project was developed in [Eclipse](http://www.eclipse.org/home/index.php).
I am quite happy to see the old stuff still working.

Please, go and try yourself:

```
git clone https://github.com/mkrapp/rde-solver
```

and then

```
ant [clean,compile,jar,run]
```

To produce the actual spiral wave you have to process the created data files.
That part is not included.
If you like to see how this works, drop me an [email](mailto:mariokrapp@gmail.com).
