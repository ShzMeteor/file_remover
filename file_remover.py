import os
    

def file_remover() -> str:
    # Prompt user for source and destination directory
    src_dir = input("> Source directory: ")
    des_dir = input("> Destination directory: ")

    # Store structure of source directory
    src_files = os.walk(src_dir)

    # Discover files in the source folder
    files_dict = {}
    for (root, dirs, file) in src_files:
        # Check if directory has any files
        if file != []:
            # Store file paths without src_dir path
            try:
                path = root.replace(src_dir, "")
                files_dict[path] = file
            except IndexError:
                pass      

    # Discover files in the destination folder
    discovered_files = []
    for path, files in files_dict.items():
        # Create the file's path in the destination directory
        des_path = des_dir + path + "\\"
        for file in files:
            file_path = des_path + file
            print(f"FOUND {file_path}")
            # Store file paths for later removal
            discovered_files.append(file_path)
    print(f"{len(discovered_files)} files found.\n")

    while True:
        ans = input("> Remove discovered files? [y/n] ").lower()
        # Remove files
        if ans == 'y':
            print()
            count: int = 0
            for file in discovered_files:
                try:
                    os.remove(file)
                    count += 1
                    print(f"REMOVED {file}")
                except OSError:
                    pass
            print(f"{count} files removed.")
            break
        elif ans == 'n':
            print("\nOperation terminated!")
            break
    
    while True:
        ans = input("Start over? [y/n] ").lower()
        if ans == 'y':
            os.system('cls')
            return 'y'
        elif ans == 'n':
            return 'n'


def main():
    while True:
        ans = file_remover()            
        if ans == 'n':
            break


if __name__ == "__main__":
    main()