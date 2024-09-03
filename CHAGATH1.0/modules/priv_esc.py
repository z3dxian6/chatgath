import os

def check_sudo_permissions():
    print("\nChecking for sudo permissions without password:")
    sudoers = os.popen('sudo -l').read()
    if "(ALL : ALL) NOPASSWD: ALL" in sudoers:
        print("[+] User can sudo without password!")
    else:
        print("[-] No sudo permissions without password found.")

def check_world_writable_files():
    print("\nChecking for world writable files:")
    world_writable = os.popen('find / -perm -2 -type f 2>/dev/null').read()
    if world_writable:
        print("[+] World writable files found:")
        print(world_writable)
    else:
        print("[-] No world writable files found.")

def check_suid_files():
    print("\nChecking for SUID files:")
    suid_files = os.popen('find / -perm -4000 -type f 2>/dev/null').read()
    if suid_files:
        print("[+] SUID files found:")
        print(suid_files)
    else:
        print("[-] No SUID files found.")

def privilege_escalation_checker():
    check_sudo_permissions()
    check_world_writable_files()
    check_suid_files()
