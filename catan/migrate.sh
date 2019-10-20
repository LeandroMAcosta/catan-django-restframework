
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

rm db.sqlite3

newapps=()
    apps=$(ls -d ./catan/*/ 2>&1)
    for key in $apps
    do
        app=$( basename $key )
        if [ $app != "catan" ] && [ $app != "tests" ] && [ $app != "seeder" ] && [ $app != "__pycache__" ]
        then
            newapps+=$app" "
        fi
    done

python manage.py makemigrations 
python manage.py makemigrations $newapps
python manage.py makemigrations player card resource lobby game board settlement
python manage.py migrate

echo "yes" | python manage.py flush

echo $'\n--------------------------------------'
echo "-- Creando usuario Admin:"
echo "-- User: admin"
echo "-- password: admin123"
echo "--------------------------------------"

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

python manage.py loaddata catan/seeder/initial_data.json
