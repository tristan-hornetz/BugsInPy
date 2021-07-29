
ln -s "$(readlink -f httpie)" tests/httpie

ln -s "$(readlink -f httpie)" tests/httpie

if [[ "$buggy_commit" == "16df8848e81eefac830f407e4b985f42b52970da" ]]; then
  echo "Different test setup"
  echo "from TestWrapper.WrapperBase import pytest_runtest_call, pytest_sessionfin" >> tests/conftest.py
  ln -s $(readlink -f TestWrapper) tests/TestWrapper
  pytest tests/*
else
  pytest
fi
