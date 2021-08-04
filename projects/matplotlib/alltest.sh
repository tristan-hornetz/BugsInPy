
pip install pytest-xdist
ln -s $(readlink -f WrapClass.py) lib/WrapClass.py
ln -s $(readlink -f TestWrapper) lib/TestWrapper
pytest -n 10
