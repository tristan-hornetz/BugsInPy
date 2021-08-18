
pip install pytest-xdist Cython
python -mpip install -ve . -I
ln -s $(readlink -f WrapClass.py) lib/WrapClass.py
ln -s $(readlink -f TestWrapper) lib/TestWrapper
pytest -n 8
