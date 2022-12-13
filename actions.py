from colorama import Fore, Back, Style

## This is for searching the results of the analyze function
## Currently if the video has two video streams the app crashes here. It's useful because it's a good reminder to delete the timecode track, but crashing the app is never good. I have to understand what happens and fix it in future versions.
def search(list_of_keywords, where_search, where_save):
    for keyword in list_of_keywords:
        # This is to avoid rewritting. Important with the ffprobe code. This way we avoid the audio data (because it comes later) rewritting the video data.
        # It's very importat to know the given outpout in order to make this work.
        if keyword in where_search:
            if where_search != "codec_type = data":
                if keyword in where_save.keys():
                    where_save[f'{keyword}_copy'] = where_search
                else:
                    where_save[keyword] = where_search
            else:
                where_save['timecode_track'] = True
                break



def print_results(printables, dict, has_space):
    print(f"\n{Fore.CYAN}These are the values for {Back.CYAN}{Fore.BLACK} {dict['name']}: {Style.RESET_ALL}\n")
    for element in printables:
        if has_space == True:
            prefix = element[1].removesuffix('_copy') + ' = '
        else:
            prefix = element[1].removesuffix('_copy') + '='

        print(f"\t{element[0]}: {Fore.CYAN}{dict[element[1]].removeprefix(prefix)}{Style.RESET_ALL}")
    print("\n")



def input_validator(question, *options):
    while True:
        variable = input(f"\n{question}\n").lower()
        if variable in options:
            if variable == 'y':
                choice = True
                return choice
            elif variable == 'n':
                choice = False
                return choice
            else:
                return variable

        else:
            print(f"Sorry, I did not understand use one of these commands {options}")


def print_todos(string, action):
    return (f'\n\t{Fore.CYAN}{string}:{Style.RESET_ALL} {action}')

