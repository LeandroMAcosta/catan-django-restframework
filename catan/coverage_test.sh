echo "..........Run migrate.sh.......... \n"
echo ""

./migrate.sh

echo ""

coverage erase
rm -fr htmlcov

echo ""
echo "..........Testing all test.........."
echo ""

coverage run --source='.' manage.py test .

echo ""
echo "..........Create HTML test.........."
echo ""

general=*/__init__.py,*/migrations/*
api=api/*
python_files=*/apps.py,*/urls.py,*/wsgi.py,*/serializers.py

coverage html --omit=$general,$api,$python_files

echo ""
echo "..........OPEN HTML test.........."
echo ""

chmod -R 777 ./htmlcov/index.html
nohup xdg-open ./htmlcov/index.html

echo ""
