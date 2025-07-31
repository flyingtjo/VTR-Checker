import os
import datetime
import sys
import re
import shutil
import time

source_directory_folder = "/Users/tyleroldano/Documents/CitrusImports"
destination_directory_folder = "/Users/tyleroldano/Documents/CitrusExports"

def get_citrus_date():
    x = datetime.datetime.now()
    ordered_list = [f"{x.month:02}", f"{x.day:02}", x.year % 100]
    citrus_date = f"{int("".join(map(str, ordered_list))):06}"
    return citrus_date

def get_show_type():
    day_of_week = datetime.datetime.now().isoweekday()
    match day_of_week:
        case 1:
            news_day = "MONNEWS"
        case 2:
            news_day = "TUESNEWS"
        case 3:
            news_day = "WEDNEWS"
        case 4:
            news_day = "THURSNEWS"
        case 5:
            news_day = "FRINEWS"
        case _:
            sys.exit("You appear to be trying to import a pkg on a non-news day. We currently don't support importing pkg's ahead of time (sorry JJ) Please try again on a valid day.")
    return news_day

def get_file_type():
    segment_check = input("Please type in the segment in all caps (VO, SOT, PKG, etc) and press 'enter': ")
    match segment_check:
        case "VO":
            file_end = "VO.mp4"
        case "PKG":
            file_end = "PKG.mp4"
        case "SOT":
            file_end = "SOT.mp4"
        case _:
            sys.exit("You've entered an invalid input, please run the program again and choose either 'VO, SOT, or PKG,'")
    return file_end

future_mode = input("Welcome to the CitrusTV File Naming System. Are you uploading a file for today's show? y/n: ")
time.sleep(0.25)

match future_mode:
    case "y":
        date_matters = 0
    case "n":
        date_matters = 1
    case _:
        sys.exit("Invalid answer detected. Please run the program again")

source_folder_list = os.listdir(source_directory_folder)
print("Understood. Here is a list of all the files in the import folder" , os.listdir(source_directory_folder))
time.sleep(0.25)
option_list_number = int(input("Which entry do you want to process? Type: (1,2,3...)")) - 1
time.sleep(0.25)
print("you selected " , source_folder_list[option_list_number])
original_name = source_folder_list[option_list_number]

pattern = r"(MON|TUES|WED|THURS|FRI)NEWS_\d{6}(?:_[A-Z_]+)?_(SOT|VO|PKG)\.mp4"

file_name_valid = re.search(pattern, original_name)

show_type = get_show_type()

date_int = get_citrus_date()

bad_name = 0

if file_name_valid:
    print("Surface check passed.")
    if date_matters == 0:
        original_name_parsed = original_name.split("_")
        match original_name_parsed[0]:
            case str(date_int):
                print("Show check passed")
                final_name_output = "_".join(original_name_parsed)
            case "_":
                print("Show check failed.")
                bad_name = 1
        match original_name_parsed[1]:
            case str(show_type):
                print("date check passed")
                final_name_output = "_".join(original_name_parsed)
            case "_":
                print("date check failed")
                bad_name = 1
    else:
        print("You're checking a file not airing on tonight's show. We are unable to check the date and show accuracy, but all other elements are valid.")
        time.sleep(0.25)
        print("Please double check that the show and date are correct.")
        time.sleep(0.25)
        print(original_name)
        time.sleep(0.25)
        input("press enter if you're sure this name is correct. If not, close the program, change the name, and run it again.")
        final_name_output = original_name
else:
    print("This file name is not correct.")
    bad_name = 1
if bad_name == 1:
    print("The checker has found one or more errors with the file's original name. Launching VTR re-namer.")
    print("This is the CitrusTV VTR re-namer")
    slug = input("Please type in your ENPS slug in all caps and press 'enter': ")
    element_list = [get_citrus_date() , get_show_type() , str(slug) , get_file_type()]
    final_name_output = "_".join(element_list)
time.sleep(0.25)
os.rename((source_directory_folder + "/" + original_name), (destination_directory_folder + "/" + final_name_output))
time.sleep(0.25)
input("The file has been reformated for VTR (if needed). Press enter, and your file will be moved to the playback folder")
try:
    shutil.move((source_directory_folder + "/" + original_name), (destination_directory_folder + "/" + final_name_output))
    print(f"File '{source_directory_folder}' moved to '{destination_directory_folder}'.")
except FileNotFoundError:
    print(f"Error: Source file '{source_directory_folder}' not found.")
except shutil.Error as e:
    print(f"Error moving file: {e}")

print("Here is a list of all the files in the export folder" , os.listdir(destination_directory_folder))