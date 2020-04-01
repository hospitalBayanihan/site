# site: hospitalbayanihan

Getting Started:
1. Setup virtual environment 
  virtualenv --python=/usr/bin/python3.7 <virtualenv name>
2. Activate your virtual env
3. Create a folder you want to store the git repo
4. on this folder.. git clone https://github.com/hospitalBayanihan/site.git
5. pip install -r requirements.txt
6. run Djang
  python manage.py runserver
7. Go to http://localhost:8000/ using any browser

Adding columns to db:
1. go to main/models.py
2. make necessary modifications. Add new database, add new features etc.
3. go to git root
4. do 'python manage.py makemigrations" - This will convert the changes in the
   models.py into SQL commands.
5. do 'python manage.py manage" - This will execute the SQL command. At this
   point, you should see the changes in db.sqlite. Try to open the db.sqlite
   using any sqlite viewer, to investigate.
6. Modify main/views.py to receive the data from the POST command.
7. Modify the main/templates/index.html to modify the front end that will
   serve as the form. Make sure the names matches the declarations in
   main/views.py

Herlan Branch notes:
1. models.py in main was edited to include all columns from airtable.
2. refresh view was added to update database based from airtable data.
3. I may have screwed up the migrations for main due to having many tries.

