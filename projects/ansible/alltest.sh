
pip install -r test/units/requirements.txt
pip install pytest-xdist mock pytest-mock
source hacking/env-setup
ln -s $(readlink -f TestWrapper) ./lib/TestWrapper
ln -s $(readlink -f WrapClass.py) ./lib/WrapClass.py
pytest -n 8 test $(python TestWrapper/get_failing_test_ids.py) --ignore-glob=*TestWrapper* --continue-on-collection-errors
