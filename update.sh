cd ~/Sprinkler
git pull
cp -R -f ./sprinkler/* /opt/Sprinkler/sprinkler/
cp -f ./wsgi.py /opt/Sprinkler/
rm -rf /opt/Sprinkler/RPi
sudo systemctl restart sprinkler
