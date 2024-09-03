from termcolor import colored
import sys
sys.dont_write_bytecode = True
banner = """
 ______  _    _   ______   ______   ______  _______  _    _
| |     | |  | | | |  | | | | ____ | |  | |   | |   | |  | |
| |     | |--| | | |__| | | |  | | | |__| |   | |   | |--| |
|_|____ |_|  |_| |_|  |_| |_|__|_| |_|  |_|   |_|   |_|  |_|
"""
def print_banner():
    print(colored(banner, 'light_magenta'))
    print(colored("""             
===========================================
|            My Pentest Framework          |
|       Author: zed                |
|       Description: A framework for       |
|       network scanning and privilege     |
|       escalation.                        |
===========================================
""", 'red'))