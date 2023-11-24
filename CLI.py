import os
import argparse

INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .wav file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

def validate_file(file_name):
    if not valid_path(file_name):
        print(INVALID_PATH_MSG%(file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG%(file_name))
        quit()
    return
     
def valid_filetype(file_name):
    return file_name.endswith('.wav')
 
def valid_path(path):
    return os.path.exists(path)

def hide_lsb(args):
	print(args.hide_lsb)
	
def extract_lsb(args):
	print(args.extract_lsb)
	
def hide_phase_coding(args):
	print(args.hide_phase_coding)
	
def extract_phase_coding(args):
	print(args.extract_phase_coding)
	
def show(args):
    dir_path = args.show[0]
     
    if not valid_path(dir_path):
        print("Error: No such directory found.")
        exit()
 
    # get wav files in directory
    files = [f for f in os.listdir(dir_path) if valid_filetype(f)]
    print("{} wav files found.".format(len(files)))
    print('\n'.join(f for f in files))
	
def main():
	# create parser object
	parser = argparse.ArgumentParser(description = "Steganography methods manager")

	# defining arguments for parser object
	parser.add_argument("-hl", "--hide-lsb", action='store_true', default = None,
						help = "Opens and reads the specified text file.")
	
	parser.add_argument("-el", "--extract-lsb", action='store_true', default = None,
					    help = "Opens and reads the specified text file.")
	
	parser.add_argument("-hp", "--hide-phase-coding", action='store_true', default = None,
					    help = "Opens and reads the specified text file.")
	
	parser.add_argument("-ep", "--extract-phase-coding", action='store_true', default = None,
					    help = "Opens and reads the specified text file.")
	
	parser.add_argument("-f", "--file", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified text file.")
	
	parser.add_argument("-s", "--show", type = str, nargs = 1,
						metavar = "path", default = None,
						help = "Shows all the text files on specified directory path.\
						Type '.' for current directory.")

	args = parser.parse_args()
	
	if args.show != None:
		show(args)
	elif args.hide_lsb != None:
		hide_lsb(args)
	elif args.extract_lsb != None:
		extract_lsb(args)
	elif args.hide_phase_coding != None:
		hide_phase_coding(args)
	elif args.extract_phase_coding != None:
		extract_phase_coding(args)


if __name__ == "__main__":
	main()
	