#!/bin/bash

sites=(https://google.com
       https://facebook.com
       https://twitter.com
       https://unavaliable.tom)

>"website_status.log"

for site in "${sites[@]}"; do
    if curl -o /dev/null -s -L -w "%{http_code}\\n" $site -e 200
    then
    echo "<$site> is UP" >> website_status.log
    else
    echo "<$site> is DOWN" >> website_status.log
    fi
done

echo work done, results saved to website_status.log