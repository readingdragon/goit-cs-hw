#!/bin/bash

sites=(https://google.com
       https://facebook.com
       https://twitter.com
       https://unavaliable.tom)

log_file = website_status.log

>"$log_file"

for site in "${sites[@]}"; do
    if curl -o /dev/null -s -L -w "%{http_code}\\n" $site -e 200
    then
    echo "<$site> is UP" >> $log_file
    else
    echo "<$site> is DOWN" >> $log_file
    fi
done

echo work done, results saved to $log_file