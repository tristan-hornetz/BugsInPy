
pip install -r test/units/requirements.txt
pip install pytest-xdist mock pytest-mock
source hacking/env-setup
ansible-test units --local
