
python setup.py build_ext --inplace -j 8
pip install pytest-xdist
pytest -n 8 --pyargs spacy
