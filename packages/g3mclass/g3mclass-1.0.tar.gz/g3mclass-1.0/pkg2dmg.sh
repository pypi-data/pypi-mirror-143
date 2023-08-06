#!/bin/bash

mydir=$(dirname $(realpath $0))
cd $mydir
url=g3mclass
# create macos g3mclass.app
python3 setup.py sdist
v=$(cat g3mclass/version.txt)
rm -rf dmg/ # clean up before
mkdir dmg
#mkdir -p dmg/install.app/Contents/MacOS
#mkdir -p dmg/install.app/Contents/Resources
#cp dist/g3mclass-$v.tar.gz dmg/install.app/Contents/Resources/

# create install script
cat <<EOF >dmg/install
#!/bin/sh
pexe=\$(python3 -m site --user-base)/bin/g3mclass
python3 -m pip install --user -U "$url"
ln -sf \$pexe \$HOME/Desktop/
EOF
chmod 755 dmg/install

# create uninstall script
cat >dmg/uninstall <<EOF
#!/bin/sh
python3 -m pip uninstall -y g3mclass
rm -f \$HOME/Desktop/g3mclass*
EOF
chmod 755 dmg/uninstall

# create/format a dmg
rm -f dist/g3mclass-$v.dmg
s=$(echo -e $(($(du -sk dmg | cut -f1)+10))"\n"512 | sort -n | tail -1)
dd if=/dev/zero of=dist/g3mclass-$v.dmg bs=1k count=$s status=progress
mkfs.hfsplus -v install_g3mclass-$v dist/g3mclass-$v.dmg

# copy files into image fs
mount | grep /mnt/disk && sudo umount /mnt/disk
sudo mount -o loop dist/g3mclass-$v.dmg /mnt/disk
sudo cp -av dmg/* /mnt/disk
sudo umount /mnt/disk

# compress
/usr/local/src/libdmg-hfsplus-only_what_core_needs/build/dmg/dmg dist/g3mclass-$v.dmg dist/g3mclass-$v.c.dmg && \
mv -f dist/g3mclass-$v.c.dmg dist/g3mclass-$v.dmg
