
ln -s "$(readlink -f httpie)" tests/httpie
pytest
