
if [ $1 == "help" ] ; then
  echo "Options:"
  echo "- create (creates the database)"
  echo "- drop (drops the database)"
  echo "- generate-migrate (generate migration)"
  echo "- migrate (apply the migrations to the database)"
  exit 0
fi

if [ $1 == "create" ] ; then
  python setup_db.py
  exit 0
fi
if [ $1 == "drop" ] ; then
  python setup_db.py --drop 1
  exit 0
fi
if [ $1 == "generate-migration" ] ; then
  echo "Migration name:"
  read migration_name

  echo "Generating migration..."
  alembic revision --autogenerate -m $migration_name

  exit 0
fi
if [ $1 == "migrate" ] ; then
  echo "Applying migrations..."
  alembic upgrade head
  exit 0
fi