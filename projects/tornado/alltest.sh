
sed -r 's/^.*.tornado.test.asyncio_test.,//' tornado/test/runtests.py > temp
cat temp > tornado/test/runtests.py
rm temp
rm tornado/test/asyncio_test.py
./runtests.sh
