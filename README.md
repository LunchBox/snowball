hello

```
$ pip install virtualenv
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Jupyter Notebook

```
(venv) $ jupyter notebook
```

Setup VirtualEnv for Jupyter Notebook Kernel (first time only)

```
# install the venv as kernel into the notebook
(venv) $ python -m ipykernel install --user --name=venv
```

incase for remove kernel

```
(venv) $ jupyter-kernelspec uninstall venv 
```

place the custom.css for better jupyter layout

```
$ cp custom.css ~/.jupyter/custom/custom.css
```