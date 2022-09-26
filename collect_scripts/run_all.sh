
#!/bin/bash

sudo ./start_run_default_autonuma.sh

./generate_memory_pressures.sh

sudo ./start_run_pressure_autonuma.sh

sudo ./start_post_process.sh

./start_mapping.sh

./start_static_mapping.sh
