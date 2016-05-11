chute-client
============

Chute client the rasberry pi machines


# Wordpress

1. git clone the repo
2. pip install -r requirements.txt
3. 




## Old

1. git clone the repo
2. pip install -r requirements.txt
3. ./manage.py register -p :project_slug | (get the :project_slug from the main app.magnificent.com/project/:project_slug)
4. ./manage.py update_playlist           | (build the local playlist.json from the remote)
4. ./manage.py runserver -h 0.0.0.0 -p 5000                 | start the server
5. go to http://localhost:5000           | load the page
6. ./manage.py worker                    | to download the media locally




# Send Event


```
./manage.py send_event -c box -e reload
./manage.py send_event -c project -e reload
./manage.py send_event -c project -e reload -d fdafds
./manage.py send_event -c project -e reload -d '{"test":"test"}'
./manage.py send_event -c project -e goto -d '{"test":"test"}'
./manage.py send_event -c project -e goto -d '{"pk":"23"}'
./manage.py send_event -c project -e goto -d '{"pk":"http://digitalhardcore.de/?p=1"}'
./manage.py send_event -c project -e goto -d '{"pk":"http://digitalhardcore.de/?p=12"}'
./manage.py send_event -c project -e goto -d '{"pk":"http://digitalhardcore.de/?p=4"}'
./manage.py send_event -c project -e next -d '{"pk":"http://digitalhardcore.de/?p=4"}'
./manage.py send_event -c project -e previous
./manage.py send_event -c project -e next
 ```