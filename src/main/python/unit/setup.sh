#!/usr/bin/env -S bash

set -xueo pipefail




dir=$(dirname $(readlink -f $0))

#yq  ".applications.python.path=\"${dir}/\"" $dir/setup.json  > /tmp/setup.json

# exit
sudo cp wsgi.py /var/log/unit/

sudo curl -X PUT --data-binary "$(cat $dir/setup.json)" \
--unix-socket /var/run/unit/control.sock http://localhost/config/

sudo systemctl restart unit

#sudo tail /var/log/unit/unit.log
#sudo curl --unix-socket /var/run/unit/control.sock t/
#curl http://localhost:8000/

