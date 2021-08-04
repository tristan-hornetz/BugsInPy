
pip install pytest python_toolbox
echo "from python_toolbox import sys_tools as mini_toolbox" >> ./tests/__init__.py
pytest
