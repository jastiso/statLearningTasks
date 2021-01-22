#!/bin/bash
# This script copies all new participant entries to a shared
# table, preserving all data.
#
# Run as ./db_copy_to_master.sh
#
# Author: Ari Kahn

# ------- CHANGE THIS LINE TO THE NAME OF YOUR TABLE ------
mytable="participants_js"
# ------- Don't edit anything below -------

echo "Backing up table ${mytable} to master\n"
# Copy all new participants into the master list
heroku pg:psql <<EOF
\set ECHO all
INSERT INTO participants_master
SELECT * FROM ${mytable}
WHERE uniqueid NOT IN (SELECT uniqueid FROM participants_master);
EOF

