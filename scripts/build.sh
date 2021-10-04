#!/bin/bash
# activate venv
source /home/sven/Nextcloud_Sven/Schreibtisch/git_sh-edraft_de/sh_cpl/cpl-env/bin/activate

# CPL
cd /home/sven/Nextcloud_Sven/Schreibtisch/git_sh-edraft_de/sh_cpl/src/cpl_core
cpl build

# CLI
cd /home/sven/Nextcloud_Sven/Schreibtisch/git_sh-edraft_de/sh_cpl/src/cpl_cli
cpl build

# CPL Query
cd /home/sven/Nextcloud_Sven/Schreibtisch/git_sh-edraft_de/sh_cpl/src/cpl_query
cpl build