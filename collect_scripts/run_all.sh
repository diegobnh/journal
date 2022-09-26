
#!/bin/bash

export USER=`whoami`

sudo ./start_run_default_autonuma.sh
sudo -u $USER ./generate_memory_pressures.sh
sudo ./start_run_pressure_autonuma.sh
sudo ./start_post_process.sh
sudo -u $USER ./start_mapping.sh
sudo ./start_run_static.sh
