from core import banner, commands

def main():
    banner.print_banner()
    while True:
        commands.menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            from modules import port_scan
            port_scan.port_scanner()
        elif choice == '2':
            from modules import priv_esc
            priv_esc.privilege_escalation_checker()
        elif choice == '3':
            print("Exiting the framework.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
