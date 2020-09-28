sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo rm -rf /etc/nginx/sites-enabled/default

sudo ln -sf /home/box/etc/hello.py  /etc/gunicorn.d/hello.py

sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/nginx restart
