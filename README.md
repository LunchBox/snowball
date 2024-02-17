hello

```
$ pip install virtualenv
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Jupyterlab

```
# check jupyter, should be /path/to/current/folder/venv/bin/jupyter
(venv) $ which jupyter

(venv) $ jupyter lab
```

Convert jupyter notebook .ipynb file to python .py file, saved to ./scripts folder

```
(venv) $ chmod +x to_py.sh
(venv) $ ./to_py.sh {NOTEBOOK}.ipynb
```
