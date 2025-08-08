#!/usr/bin/env python3
# flowchart-lang/package-manager.py

import os
import sys
import argparse
import requests

# The base URL for the Flowchart-lang library repository
GITHUB_LIB_REPO = "https://raw.githubusercontent.com/Flowchart-lang/fcl-lib/main/libs/"

def install_library(library_name):
    """
    Downloads a specified library from the GitHub repository and saves it
    to the local 'libs' directory.
    """
    print(f"Attempting to download library '{library_name}'...")

    # Construct the full URL for the library file
    download_url = f"{GITHUB_LIB_REPO}{library_name}.py"
    
    try:
        # Make a GET request to the URL
        response = requests.get(download_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the path to the local 'libs' directory
            libs_dir = os.path.join(script_dir, "libs")
            
            # Create the 'libs' directory if it doesn't exist
            os.makedirs(libs_dir, exist_ok=True)
            
            # Construct the full path for the new library file
            file_path = os.path.join(libs_dir, f"{library_name}.py")
            
            # Write the downloaded content to the file
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            print(f"Success: Library '{library_name}' downloaded and saved to '{file_path}'.")
            
        elif response.status_code == 404:
            print(f"Error: Library '{library_name}' not found in the repository. Please check the name.")
            sys.exit(1)
        else:
            print(f"Error: An unexpected HTTP error occurred. Status code: {response.status_code}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred while trying to download the library. Details: {e}")
        sys.exit(1)

def main():
    """
    Main function to parse command-line arguments and run the package manager.
    """
    parser = argparse.ArgumentParser(
        prog='fpm',
        description='Flowchart-lang Package Manager (FPM)',
        epilog='Example: fpm -i math'
    )
    
    # Define an argument for installing a library
    parser.add_argument(
        '-i', '--install',
        type=str,
        metavar='<lib_name>',
        help='Install a library by its name.'
    )
    
    args = parser.parse_args()
    
    if args.install:
        install_library(args.install)
    else:
        # If no valid command is given, show help message
        parser.print_help()

if __name__ == "__main__":
    main()

