
pip install -r test/units/requirements.txt
pip install pytest-xdist
source hacking/env-setup
ansible-test units --local
