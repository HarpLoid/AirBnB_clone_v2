#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

HTML_TEXT="<html><head></head><body>Holberton School</body></html>"
CONFIG="\\n\tlocation \/hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tadd_header X-Served-By '$HOSTNAME';\n\t}"

if ! [ -x "$(command -v nginx)" ];
then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}

sudo touch /data/web_static/releases/test/index.html

echo $HTML_TEXT | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default;
then
    sudo sed -i "30i\ $CONFIG" /etc/nginx/sites-available/default
fi

sudo service nginx restart
