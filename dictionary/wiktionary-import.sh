#!/bin/bash
pages=/library/nexc-wiktionary-pages-articles.sql.gz

[ -e ${pages} ] || exit 0
renice -n 18 -p $$ > /dev/null 2>&1

log() {
    logger -p user.notice -t nexc-wiktionary-db -s -- "$1" 
}

log "Starting wiktionary database import"

echo "TRUNCATE TABLE text; TRUNCATE TABLE revision; TRUNCATE TABLE page;" | mysql -u wiktionary --password=wiktionary wiktionary

if zcat $pages | mysql -u wiktionary --password=wiktionary wiktionary; then
	log "Database import success"
else
	log "Import failed with code $?"
fi

rm -f $pages

