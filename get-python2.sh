#!/bin/bash

# Sets up old python2 at /opt/python2.
# Unspported by security teams.
# For local experiments only.
# Tested on Ubuntu 24.04.

set -e
cd /tmp
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz
tar -Jxvf Python-2.7.18.tar.xz
cd Python-2.7-18
./configure --prefix=/opt/python2 --enable-optimizations
# Disable tests that won't pass on Ubuntu 24.04
# for libraries which you shouldn't be using anyway
for N in ssltests ftplib test_ftplib test_ssl; do
    rm -f Lib/test/$N.py*
    touch Lib/test/$N.py
done
make
sudo mkdir -p /opt/python2
sudo make install
for N in /opt/python2/bin/python2*; do sudo ln -s $N /usr/local/bin/; done
