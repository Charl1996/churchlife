import psycopg2
import argparse
from configs import (
   POSTGRES_USER,
   POSTGRES_PASSWORD,
   POSTGRES_PORT,
   POSTGRES_DATABASE,
)


def handle_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument(
      '--drop',
      default=False,
      help='Drops the database',
   )

   return parser.parse_args()


args = handle_arguments()

drop_db = False
if args.drop:
   drop_db = True


print('Getting connection......')
conn = psycopg2.connect(
   user=POSTGRES_USER,
   password=POSTGRES_PASSWORD,
   host='localhost',
   port=POSTGRES_PORT
)
print('Connected!')
conn.autocommit = True

cursor = conn.cursor()

if drop_db:
    sql = f'''DROP database {POSTGRES_DATABASE};'''
    print('Dropping database......')

    cursor.execute(sql)
    print('Database successfully dropped......')
else:
    sql = f'''CREATE database {POSTGRES_DATABASE};'''
    print('Creating database......')

    cursor.execute(sql)
    print('Database created successfully......')

conn.close()
print('Closed connection!')
