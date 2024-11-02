import os
import argparse

def stitch_files(directory, output_file, base_filename=None):
    """
    Stitch together file parts into a single file, either for a specific base filename 
    or for all files in the directory that follow the part naming pattern.
    
    :param directory: Directory where the file parts are stored.
    :param output_file: The name of the output file to create (only used if base_filename is specified).
    :param base_filename: The base name of the file parts to stitch together. If None, stitches all files in the directory.
    """
    # Ensure the directory ends with a slash
    if not directory.endswith(os.path.sep):
        directory += os.path.sep

    # Get a list of all files in the directory
    all_files = os.listdir(directory)

    # If a specific base_filename is provided, stitch only those parts
    if base_filename:
        stitch_single_file(directory, output_file, base_filename, all_files)
    else:
        # Automatically detect base filenames and stitch each group of parts
        base_filenames = detect_base_filenames(all_files)
        for base in base_filenames:
            stitch_single_file(directory, f"{base}_stitched_output.file", base, all_files)

def detect_base_filenames(files):
    """
    Detects unique base filenames from a list of files.
    
    :param files: List of filenames.
    :return: A set of unique base filenames (e.g., if 'file.part1' and 'file.part2' are present, returns 'file').
    """
    base_filenames = set()
    for filename in files:
        if '.part' in filename:
            base_name = filename.split('.part')[0]
            base_filenames.add(base_name)
    return base_filenames

def stitch_single_file(directory, output_file, base_filename, all_files):
    """
    Stitches parts for a single base filename.
    
    :param directory: Directory where the file parts are stored.
    :param output_file: The name of the output file to create.
    :param base_filename: The base name of the file parts to stitch together.
    :param all_files: List of all files in the directory.
    """
    # Filter out parts matching the base filename
    parts = [filename for filename in all_files if filename.startswith(base_filename) and '.part' in filename]

    # Sort parts by their part number
    parts.sort(key=lambda x: int(x.split('.part')[-1]))

    # Open the output file in write-binary mode and stitch parts together
    with open(directory + output_file, 'wb') as output:
        for part in parts:
            with open(directory + part, 'rb') as f:
                output.write(f.read())

    print(f"Stitched {len(parts)} parts into {output_file}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Stitch file parts together")
    parser.add_argument("-d", "--directory", default=".", help="Directory where the file parts are stored (default is current directory)")
    parser.add_argument("-o", "--output_file", help="Name of the output file (used only if base_filename is specified)")
    parser.add_argument("-b", "--base_filename", help="The base filename for the parts to stitch (if not specified, stitches all found files)")

    args = parser.parse_args()

    # Call the function with command-line arguments
    stitch_files(args.directory, args.output_file, args.base_filename)
