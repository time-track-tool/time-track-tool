#!/bin/bash

folders=("detectors" "html" "lib" "utils")

for f in "${folders[@]}"
do
  app_directory="$TRACKER_HOME/$f"
  git_directory="/opt/timetracker/time-track-tool/$f"
  if [ -L $app_directory ]
  then
    rm $app_directory
  else
    rm -rf $app_directory
  fi
  echo "Link $git_directory to $app_directory"
  ln -s $git_directory $app_directory
done
ls -l
make --directory $TRACKER_HOME/html
chown -R 51784:50000 $TRACKER_HOME/html/userlist.html
chmod 644 $TRACKER_HOME/html/userlist.html