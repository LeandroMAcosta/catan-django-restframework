echo "Run migrate.sh"


coverage erase

echo "Testing and create html coverage"
MYVAR="api/*,"
coverage run --source='.' --omit=$MYVAR manage.py test lobby
coverage html
