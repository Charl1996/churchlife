
if [ $1 == "help" ] ; then
  echo "Options:"
  echo "- create (creates the database)"
  echo "- drop (drops the database)"
  echo "- migrate (generate and optionally apply the migrations to the database)"
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
if [ $1 == "migrate" ] ; then
  echo "Generate migrations"
  echo "Migration name:"
  read $migration_name
  alembic revision --autogenerate -m "$migration_name"

  echo "Apply migrations?"
  read $apply_migrations

  if [ "$apply_migrations" == "Y" ] ; then
    echo "Applying migrations"
    alembic upgrade head
  else
    echo "Oki doki! You can apply your migrations later by running:"
    echo "alembic upgrade head"
  fi
  exit 0
fi