import os
    

# Background color for text
class txt_clr:
    white_bg = "\033[30;47;1;4m"
    red_bg = "\033[41;1;4m"
    green_bg = "\033[42;1;4m"
    reset_clr = "\033[0m"


# Discover the files in source directory
def find_src_files() -> list:
    # Prompt for source path
    src_dir = input("> Source directory: ")
    print()

    # Store structure of source directory
    src_files = os.walk(src_dir)

    # Discover files in the source folder
    file_paths: list = []
    for (root, dirs, files) in src_files:
        # Check if directory has any files
        if files == []:
            continue
        
        # Store file paths without src_dir path
        try:
            path = root.replace(src_dir, "") + "\\"
            for file in files:
                file_path = path + file
                print(f"{txt_clr.green_bg} FOUND {txt_clr.reset_clr} {file_path}")
                file_paths.append(file_path)
        except IndexError:
            pass   
    
    return file_paths


# Check destination directory for files that are marked for removal
def check_dst_files(file_paths: list) -> list:
    # Prompt for destination path
    dst_dir = input("> Destination directory: ")
    print()
    
    # Discover files in the destination folder
    discovered_files: list = []
    for path in file_paths:
        # Create the file's path in the destination directory
        file_path = dst_dir + path

        if os.path.isfile(file_path):
            # Store file paths for later removal
            discovered_files.append(file_path)
            print(f"{txt_clr.green_bg} FOUND {txt_clr.reset_clr} {file_path}")
        else:
            print(f"{txt_clr.red_bg} NOT FOUND {txt_clr.reset_clr} {file_path}")
        
    print(f"{len(discovered_files)} files found.\n")

    # Menu
    print("Remove discovered files? [y/n]")
    while True:
        ans = input(">> ").upper()
        if ans == 'Y':
            break
        elif ans == 'N':
            os.system("cls")
            return

    return discovered_files


# Remove discovered files
def remove_files(discovered_files: list):
    count: int = 0
    for file in discovered_files:
        try:
            os.remove(file)
            count += 1
            print(f"{txt_clr.green_bg} REMOVED {txt_clr.reset_clr} {file}")
        except OSError:
            print(f"{txt_clr.red_bg} NOT FOUND {txt_clr.reset_clr} {file}")

    print(f"\nRemoved {count}/{len(discovered_files)} files.\n")

    os.system("pause")
    os.system("cls")
    return


# Export a list of files that have to be removed as .txt
def save_file_paths(file_paths: list, file_name: str):
    # Check if file already exists
    if os.path.isfile(file_name) == True:
        # Overwrite or return
        print("File exists! overwrite? [y/n]")
        while True:
            ans = input(">> ").upper()
            if ans == 'Y':
                break
            elif ans == 'N':
                os.system('cls')
                return
    
    # Write to file
    output = open(file_name, 'w')

    count: int = 0 
    for path in file_paths:
        print(f"{txt_clr.white_bg} SAVING {txt_clr.reset_clr} {path}", end=" ")
        try:
            output.write(path + '\n')
            count += 1
            print(f"{txt_clr.green_bg} DONE {txt_clr.reset_clr}")
        except:
            print(f"{txt_clr.red_bg} FAILED {txt_clr.reset_clr}")

    print(f"\nSaved {count} file-paths to {file_name}.\n")

    output.close()

    os.system("pause")
    os.system("cls")
    return


# Get file-paths from .txt file
def import_txt_file() -> list:
    # Create a list of files in root directory
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]

    # Print discovered .txt files
    txt_files: list = []
    count: int = 0
    print("Select a file for import:")
    for file in root_files:
        # Only print .txt files
        if file[-3:] != 'txt':
            continue

        count += 1
        print(str(count) + ") " + file)
        txt_files.append(file)

    # Return if no text files were found
    if count == 0:
        print("No text files were found in root directory!")
        os.system("pause")
        os.system("cls")
        return 
    
    # Menu
    print("R) Return")
    while True:
        ans = input(">> ").upper()

        if ans == 'R':
            os.system("cls")
            return 

        try:
            ind = int(ans) - 1
            file_name = txt_files[ind]
            break
        except ValueError:
            continue

    # Read imported file
    with open(file_name, 'r') as in_file:
        lines = in_file.readlines()
        file_paths = [path.replace("\n", "") for path in lines]
        return file_paths


# Main
def main():
    # Accept ANSI colors
    os.system("")

    # Menu
    while True:
        print("1) Save file-paths as text\n"
              "2) Remove files by importing file-paths from text\n"
              "3) Remove files by comparing existing folders")
        ans = input(">> ")

        # Save file-paths as .txt
        if ans == '1':
            os.system("cls")
            print("SAVE AS TEXT\n")

            # discover files in source directory
            file_paths = find_src_files()

            # Prompt user for text file's name
            file_name = input("\nName of output file: ") + '.txt'
            # Reset if no name was entered
            if file_name == ".txt":
                os.system("cls")
                continue

            # Save discovered file-paths to text
            save_file_paths(file_paths, file_name)

        # Remove files from paths imported from .text file
        elif ans == '2':
            os.system("cls")
            print("IMPORT AND REMOVE\n")

            file_paths = import_txt_file()

            # Check if function has returned early
            if file_name is None:
                continue

            discovered_files = check_dst_files(file_paths)

            # Check if user has decided against removal
            if discovered_files is None:
                continue

            # Remove discovered files
            remove_files(discovered_files)

        # Remove files by comparing existing folders
        elif ans == '3':
            os.system("cls")
            print("COMPARE AND REMOVE\n")

            # Discover files in source directory
            file_paths = find_src_files()

            print()

            # Discover file_paths entries that exist in destination
            discovered_files = check_dst_files(file_paths)

            # Check if user has decided against removal
            if discovered_files is None:
                continue

            # Remove discovered files
            remove_files(discovered_files)

        os.system("cls")


if __name__ == "__main__":
    main()