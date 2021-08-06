
pip install -r requirements-dev.txt
pip install pytest==5.0.1 pytest-xdist==1.21
sed -i 's/-n 4/-n 8/g' test_fast.sh
./test_fast.sh
