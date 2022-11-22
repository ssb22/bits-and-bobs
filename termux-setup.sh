# Script to paste into Termux after installing on a new device
# Silas S. Brown - public domain - no warranty

echo "deb https://packages-cf.termux.org/apt/termux-main stable main" > /data/data/com.termux/files/usr/etc/apt/sources.list && # replacing https://termux.astra.in.ua/apt/termux-main/
pkg up &&
pkg install openssh wget mosh-git expect perl exa joe lynx netcat-openbsd &&
# might want: clang git make nodejs python2 python tracepath man
echo alias ls=exa >.bash_profile &&
cd /data/data/com.termux/files/usr/bin &&
wget -O ds https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/ds &&
chmod +x ds &&
for N in ds1 ds2 ds-ssh ds1-ssh ds2-ssh; do ln -s ds $N; done &&
cd &&
ssh-keygen &&
cat .ssh/id_rsa.pub &&
echo Copy the above into non-ds authorized_keys &&
echo Add .ssh/config and .ssh/ds, and ssh manually to accept server keys first
