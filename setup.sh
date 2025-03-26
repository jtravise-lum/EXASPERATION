#!/bin/bash

set -e

# System prep
apt update && apt upgrade -y
apt install -y software-properties-common apt-transport-https ca-certificates curl wget gnupg lsb-release git vim fail2ban ufw unattended-upgrades apt-listchanges

# Install Python 3.10 and pip
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.10 python3.10-venv python3.10-dev python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Lock down SSH
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl reload sshd

# Set up UFW
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw --force enable

# Enable fail2ban with default settings
systemctl enable --now fail2ban

# Configure unattended upgrades
dpkg-reconfigure --priority=low unattended-upgrades

# Install Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
usermod -aG docker "$USER"

# Disable IPv6
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
cat <<EOF >> /etc/sysctl.conf
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
kernel.kptr_restrict = 2
EOF
sysctl -p

# Set up global Git config starter (can be customized)
git config --global init.defaultBranch main

echo "Setup complete. Reboot recommended. Log out/in for Docker group changes to apply."
# Install Caddy (official)
echo "Installing Caddy..."
apt install -y debian-keyring debian-archive-keyring
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
  | tee /etc/apt/sources.list.d/caddy-stable.list
apt update
apt install -y caddy

# Enable Caddy to start on boot
systemctl enable caddy

# Create placeholder directory for your Caddyfile
mkdir -p /etc/caddy/sites
touch /etc/caddy/Caddyfile

echo "# Drop your Caddyfile config in /etc/caddy/Caddyfile" >> /etc/caddy/Caddyfile

echo "Caddy installed. It's set to auto-start. You can now configure your reverse proxy."
