ln -s $(readlink -f .)/sanic tests/sanic

pytest
