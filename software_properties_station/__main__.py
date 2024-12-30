import os
import sys

def main():
    # Check if the current user is root
    if os.geteuid() != 0:
        print("This application must be run as root. Please use sudo.")
        sys.exit(1)
    
    # Your existing code here

if __name__ == "__main__":
    main()
