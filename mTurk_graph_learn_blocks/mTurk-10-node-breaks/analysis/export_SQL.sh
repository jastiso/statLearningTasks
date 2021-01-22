#!/bin/bash
# This file copies the sql data to local CSVs
#
# Run as ./export_SQL.sh
#
# Author: Jeni Stiso

cd ../experiment/data/raw/

heroku pg:psql << EOF
\copy (SELECT * FROM walkdata_js) TO walkdata_1.csv CSV DELIMITER ',' HEADER;
\copy (SELECT * FROM participants_js) TO participants_1.csv CSV DELIMITER ',' HEADER;
\copy (SELECT * FROM exp_js) TO experiment_1.csv CSV DELIMITER ',' HEADER;
EOF

gzip walkdata_1.csv
gzip participants_1.csv
gzip experiment_1.csv
