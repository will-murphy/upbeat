pip install South

Add 'south' to INSTALLED_APPS in upbeat/settings.py

./manage.py syncdb

./manage.py convert_to_south main

./manage.py schemamigration main --auto  # just in case

./manage.py shell 
  import south