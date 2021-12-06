# Script to paste into Termux after installing on a new device

pkg up &&
pkg install openssh wget mosh expect perl exa joe lynx netcat-openbsd &&
# might want: clang git make nodejs python2 python tracepath
echo alias ls=exa >.bash_profile &&
cd /data/data/com.termux/files/usr/bin &&
wget -O ds https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/ds &&
chmod +x ds &&
ln -s ds ds1 &&
ln -s ds ds2 &&
cd &&
ssh-keygen &&
cat .ssh/id_rsa.pub &&
echo Copy the above into non-ds authorized_keys &&
echo Add .ssh/config and .ssh/ds, and ssh manually to accept server keys first
