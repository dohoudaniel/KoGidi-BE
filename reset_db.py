import os
import django
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kogidi.settings')
django.setup()

# Get cursor
cursor = connection.cursor()

# Drop all tables
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("SHOW TABLES;")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    print(f"Dropping table {table}")
    cursor.execute(f"DROP TABLE IF EXISTS `{table}`;")

cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
print("All tables dropped successfully.")
