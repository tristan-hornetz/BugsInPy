
pip install -r requirements-dev.txt
sed -i 's/-n 4/-n 8/g' test_fast.sh
./test_fast.sh
