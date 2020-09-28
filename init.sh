sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo rm -rf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

sudo ln -sf /home/box/etc/hello.py  /etc/gunicorn.d/hello.py

sudo gunicorn -c /etc/gunicorn.d/hello.py hello:application

