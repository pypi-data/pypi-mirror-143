# nbv

Read-only Jupyter Notebook viewing using `nbconvert`.

Invoking
```
nbv notebook.ipynb
```
converts the notebook to HTML[^1] and opens this HTML file in the default web browser.

You can get a similar result with just
```
nbconvert notebook.ipynb --to html --post serve
```
Note that this (and `nbv`) doesn't require a full Jupyter installation (e.g. JupyterLab) in order to run.
But `nbv` has additional benefits[^2]:
* doesn't pollute the notebook location with HTML (unlike the above)
* no server, just open the HTML file in browser
* simple CLI, exposing only a few nbconvert options

---

**Note**: currently requires `jupyter-nbconvert` available on PATH[^3]. Maybe later will update to use the `nbconvert` library directly instead.



[^1]: Inside the OS temporary directory by default.
[^2]: Also I wanted to try [Typer](https://typer.tiangolo.com).
[^3]: Since a `pipx` install of `nbv` doesn't give this, I have removed `nbconvert` from the dependencies for now.
