---
layout: post
title: "Environmental Data Science Jupyter book"
author: "Mario"
date: 2023-07-01
---

Recently, I have been thinking more and more about collecting all the bits and bobs,the tools and the snippets of code I have assembled over the years, and to put it all into a single document.
I have seen other people putting their lecture material online in the form of a [jupyter book](https://jupyterbook.org/en/stable/intro.html), for example [Ryan Abernathy's Earth and Environmental Data Science](https://earth-env-data-science.github.io/intro.html) or [Brian Rose's Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook/home.html).

What I like about jupyter books, in particular, is that you can integrate your code snippets and the output will be automatically rendered as HTML content. A nice little side effect of it is that you will know whether your code works or not. A little bit like unit testing in software development.

jupyter {book} feature list:
- [Support](https://jupyterbook.org/en/stable/file-types/index.html#allowed-content-types) for [Markdown files](https://jupyterbook.org/en/stable/file-types/markdown.html), [Jupyer notebooks](https://jupyterbook.org/en/stable/file-types/notebooks.html), and [MyST Markdown notebooks](https://jupyterbook.org/en/stable/file-types/myst-notebooks.html) (Markdown files that will be converted to a notebook and excecuted 🤩)
- [Preview your content](https://jupyterbook.org/en/stable/start/build.html#preview-your-built-html)
- [Build a PDF](https://jupyterbook.org/en/stable/advanced/pdf.html)
- [Citations and bibliographies](https://jupyterbook.org/en/stable/content/citations.html)
- [Math and equation support](https://jupyterbook.org/en/stable/content/math.html)
- [Interactive data visualizations](https://jupyterbook.org/en/stable/interactive/interactive.html)

What I haven't figured out, yet, is how to integrate the HTML content into [Jekyll, a framework that GitHub Pages uses](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll) for turning Markdown files into a website (like this one). I would like to have that content on a subdomain.

Wait and see.
