#!/bin/bash
# This file copies the master participant list to a local table
#
# Run as ./db_copy_from_master.sh
#
# Author: Ari Kahn

# ------- CHANGE THIS LINE TO THE NAME OF YOUR TABLE ------
mytable=participants_js
# ------- Don't edit anything below -------

echo "Updating table ${mytable} from master\n"
# Copy all new participants into the master list
heroku pg:psql <<EOF
\set ECHO all
INSERT INTO ${mytable}
SELECT * FROM participants_master
WHERE uniqueid NOT IN (SELECT uniqueid FROM ${mytable});
EOF

