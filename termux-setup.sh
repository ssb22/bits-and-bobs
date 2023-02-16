# Script to paste into Termux after installing on a new device
# Silas S. Brown - public domain - no warranty

pkg up &&
pkg install openssh wget mosh-git exa joe lynx netcat-openbsd &&
# might want: clang git make nodejs python2 python tracepath man
echo alias ls=exa >.bash_profile &&
ssh-keygen &&
cat .ssh/id_rsa.pub &&
echo "Copy the above into servers' authorized_keys" &&
echo Add .ssh/config
