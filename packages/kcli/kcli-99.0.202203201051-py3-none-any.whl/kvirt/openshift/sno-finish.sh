#!/usr/bin/env bash

echo -e "#!/bin/sh\n exit 0" > /usr/local/bin/install-to-disk.sh
echo "Waiting for /opt/openshift/.bootkube.done"
until ls /opt/openshift/.bootkube.done; do
  sleep 5
done

{% if sno_dns  %}
IP=$(hostname -I | cut -d" " -f1)
sed -i "s/None/$IP/" /root/Corefile
COREDNS="$(cat /root/coredns.yml | base64 -w0)"
COREFILE="$(cat /root/Corefile | base64 -w0)"
FORCEDNS="$(cat /root/99-forcedns | base64 -w0)"
cat /opt/openshift/master.ign | jq ".storage.files |= . + [{\"filesystem\": \"root\", \"mode\": 420, \"path\": \"/etc/kubernetes/manifests/coredns.yml\", \"contents\": {\"source\": \"data:text/plain;charset=utf-8;base64,$COREDNS\", \"verification\": {}}},{\"filesystem\": \"root\", \"mode\": 420, \"path\": \"/etc/kubernetes/Corefile\", \"contents\": {\"source\":\"data:text/plain;charset=utf-8;base64,$COREFILE\",\"verification\": {}}},{\"filesystem\": \"root\", \"mode\": 448, \"path\": \"/etc/NetworkManager/dispatcher.d/99-forcedns\", \"contents\": {\"source\":\"data:text/plain;charset=utf-8;base64,$FORCEDNS\",\"verification\": {}}}]" > /root/master.ign
{% else %}
cp /opt/openshift/master.ign /root
{% endif %}

{% if api_ip != None %}
KEEPALIVEDYML="$(cat /root/keepalived.yml | base64 -w0)"
KEEPALIVEDCONF="$(cat /root/keepalived.conf | base64 -w0)"
cp /root/master.ign /root/master.ign.ori
cat /root/master.ign.ori | jq ".storage.files |= . + [{\"filesystem\": \"root\", \"mode\": 420, \"path\": \"/etc/kubernetes/manifests/keepalived.yml\", \"contents\": {\"source\": \"data:text/plain;charset=utf-8;base64,$KEEPALIVEDYML\", \"verification\": {}}},{\"filesystem\": \"root\", \"mode\": 420, \"path\": \"/etc/kubernetes/keepalived.conf\", \"contents\": {\"source\":\"data:text/plain;charset=utf-8;base64,$KEEPALIVEDCONF\",\"verification\": {}}}]" > /root/master.ign
{% endif %}

for vg in $(vgs -o name --noheadings) ; do vgremove -y $vg ; done
for pv in $(pvs -o name --noheadings) ; do pvremove -y $pv ; done
{% if sno_disk != None %}
install_device='/dev/{{ sno_disk | basename }}'
{% else %}
install_device=/dev/$(lsblk | grep disk | head -1 | cut -d" " -f1)
if [ "$install_device" == "/dev/" ]; then
  echo "Can't find appropriate device to install to"
  exit 1
fi
{% endif %}

firstboot_args='console=tty0 rd.neednet=1 {{ extra_args|default("") }}'
echo "Executing coreos-installer with ignition file /root/master.ign and device $install_device"
coreos-installer install --firstboot-args="${firstboot_args}" --ignition=/root/master.ign $install_device && shutdown -r now "Bootstrap completed, restarting node"
