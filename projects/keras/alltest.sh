
sed -i 's/-n 2/-n 8/g' pytest.ini

pip freeze > _temp.txt
DONE=false
until $DONE ;do
read || DONE=true
if [ "$REPLY" != "" ]; then
   if [[ "$REPLY" == "Keras==2.2.2"* ]]; then
       pip uninstall Keras-Applications tensorflow --yes
       pip install Keras-Applications==1.0.7 tensorflow==1.14.0
   fi
fi
done < "_temp.txt"
rm _temp.txt
rm -f keras/utils/conftest.py
pytest
