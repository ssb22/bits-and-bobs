#!/bin/bash

# Script to set up vysheng's telegram-cli
# tested on gcc 14.2 on Raspbian 13
# Silas S. Brown 2025 - public domain, no warranty

# (Upstream Git repository currently does not accept Issues
# and does not appear to be looking at Pull requests, so I'm
# not currently able to feed these changes back upstream)

set -e
git clone --recursive https://github.com/vysheng/tg.git
cd tg
sudo apt install libreadline-dev libconfig-dev libssl-dev libgcrypt-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython3-dev
./configure --disable-openssl # need libssl-dev for headers even though disabling it in favour of libgcrypt due to compile issues
sed -i tgl/tl-parser/tl-parser.c -e 's/static char s\[20\]/static char s[21]/'
sed -i main.c -e 's/, 18/, 17/'
sed -i loop.c -e 's/^int verbosity/extern int verbosity/' -e 's/^int wait_dialog_list/extern int wait_dialog_list/' -e 's/^int register_mode/extern int register_mode/'
sed -i interface.c -e 's/^int msg_num_mode/extern int msg_num_mode/' -e 's/^int readline_active/extern int readline_active/' -e 's/^int disable_colors/extern int disable_colors/' -e 's/^int permanent_peer_id_mode/extern int permanent_peer_id_mode/' -e 's/^int permanent_msg_id_mode/extern int permanent_msg_id_mode/' -e 's/^int disable_auto_accept/extern int disable_auto_accept/'
make CPFLAGS="-Wno-error=cast-function-type -Wno-error=return-type"
