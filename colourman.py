import re
from typing import LiteralString
import argparse
import datetime
from os import system, name
import sys
from time import sleep

class _Colours:
    def __init__(self):
        self.colours_normal = {
            'BLACK': '\033[30m',
            'RED': '\033[31m',
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'WHITE': '\033[37m',
            'ORANGE': '\033[38;5;208m',
            'PURPLE': '\033[38;5;129m',
            'PINK': '\033[38;5;205m',
            'BROWN': '\033[38;5;94m',
            'LIME': '\033[38;5;154m',
            'NAVY': '\033[38;5;18m',
            'GREY': '\033[38;5;245m',
            'TEAL': '\033[38;5;30m',
            'GOLD': '\033[38;5;220m',
            'SKYBLUE': '\033[38;5;117m',
            'VIOLET': '\033[38;5;92m'
        }
        self.colours_bright = {
            'BLACK': '\033[90m',
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'ORANGE': '\033[38;5;214m',
            'PURPLE': '\033[38;5;135m',
            'PINK': '\033[38;5;212m',
            'BROWN': '\033[38;5;130m',
            'LIME': '\033[38;5;154m', # (Same as normal)
            'NAVY': '\033[38;5;20m',
            'GREY': '\033[38;5;250m',
            'TEAL': '\033[38;5;37m',
            'GOLD': '\033[38;5;226m',
            'SKYBLUE': '\033[38;5;123m',
            'VIOLET': '\033[38;5;98m',


        }
        self.colours_background = {
            'BGBLACK': '\033[40m',
            'BGRED': '\033[41m',
            'BGGREEN': '\033[42m',
            'BGYELLOW': '\033[43m',
            'BGBLUE': '\033[44m',
            'BGMAGENTA': '\033[45m',
            'BGCYAN': '\033[46m',
            'BGWHITE': '\033[47m',
            'BGORANGE': '\033[48;5;208m',
            'BGPURPLE': '\033[48;5;129m',
            'BGPINK': '\033[48;5;205m',
            'BGBROWN': '\033[48;5;94m',
            'BGLIME': '\033[48;5;118m',
            'BGNAVY': '\033[48;5;18m',
            'BGGREY': '\033[48;5;245m',
            'BGTEAL': '\033[48;5;30m',
            'BGGOLD': '\033[48;5;220m',
            'BGSKYBLUE': '\033[48;5;117m',
            'BGVIOLET': '\033[48;5;92m'


        }
        self.styles = {
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'DUNDERLINE': '\033[21m',
            'ITALIC': '\033[3m',
            'INVERTED': '\033[7m',
            'INVISIBLE': '\033[8m',
            'STRIKETHROUGH': '\033[9m',
            'OVERLINE': '\033[53m',
            'BLINK': '\033[5m'
        }
        self.presets = {
            'HIGHLIGHT': self.colours_background['BGGOLD'] + self.colours_normal['BLACK'] + self.styles['BOLD'],
            'ERROR': self.colours_background['BGRED'] + self.colours_normal['WHITE'] + self.styles['BOLD'],
            'SUCCESS': self.colours_background['BGGREEN'] + self.colours_normal['WHITE'] + self.styles['BOLD'],
            'INFO': self.colours_background['BGBLUE'] + self.colours_normal['WHITE'] + self.styles['BOLD'],
            'EMPHASIS': self.colours_normal['CYAN'] + self.styles['BOLD'] + self.styles['UNDERLINE'],
            'EXTRAEMPHASIS': self.colours_normal['CYAN'] + self.styles['BOLD'] + self.styles['DUNDERLINE'],
            'WARNING': self.colours_background['BGYELLOW'] + self.colours_normal['BLACK'] + self.styles['BOLD'],
        }
        self._style_utils = {
            'DARK': '\033[2m',
            'RESET': '\033[0m'
        }

_colours = _Colours()

class _Parser:
    def _parse_text(self, art: str) -> str:
        tags = re.findall(r'<(.*?)>', art)
        LAST_DARK = False
        LAST_BRIGHT = False
        for tag in tags:
            # Split the tag into individual components (e.g., ['BOLD', 'RED'])
            components = tag.split()
            ansi_code = _colours._style_utils['RESET'] if not tag == '<CONTINUE>' else ''  # Start with the reset code
            if tag == 'RESET' or tag == 'CONTINUE':
                continue
            # Build the ANSI escape sequence for the tag
            for component in components:
                if component == 'DARK' or component == 'DIM':
                    LAST_DARK = True
                    continue
                elif component == 'BRIGHT' or component == 'LIGHT':
                    LAST_BRIGHT = True
                    continue
                elif component in _colours.colours_normal:
                    if LAST_DARK:
                        ansi_code += _colours._style_utils['DARK']
                    if LAST_BRIGHT:
                        ansi_code += _colours.colours_bright[component]
                    else:
                        ansi_code += _colours.colours_normal[component]
                elif component in _colours.colours_background:
                    ansi_code += _colours.colours_background[component]
                elif component in _colours.styles:
                    ansi_code += _colours.styles[component]
                elif component in _colours.presets:
                    if LAST_DARK:
                        ansi_code += _colours._style_utils['DARK']
                    ansi_code += _colours.presets[component]
                elif component.startswith('CODE') and component[4:].isdigit():
                    code = int(component[4:])
                    if 0 <= code <= 255:
                        ansi_code += f'\033[38;5;{code}m'
                elif component.startswith('BGCODE') and component[6:].isdigit():
                    code = int(component[6:])
                    if 0 <= code <= 255:
                        ansi_code += f'\033[48;5;{code}m'
                LAST_DARK = False
                LAST_BRIGHT = False
                if not ansi_code[len(_colours._style_utils['RESET']):] and component != 'RESET' and component != 'CONTINUE':
                    # If no ANSI code was found, set it to a placeholder
                    ansi_code = f"<INVALID COMPONENT: {component}>"

            # Replace the tag in the art with the constructed ANSI code
            art = art.replace(f'<{tag}>', ansi_code if ansi_code or tag == 'RESET' else f'<INVALID TAG>')

        # Replace <RESET> with the reset code
        art = art.replace('<RESET>', _colours._style_utils['RESET'])

        # Ensure the reset code is applied after every line to avoid lingering styles
        lines = art.splitlines()
        art = "\n".join(line + _colours._style_utils['RESET'] if not line.endswith('<CONTINUE>') else line for line in lines).replace('<CONTINUE>', '')

        return _colours._style_utils['RESET'] + art + _colours._style_utils['RESET']  # Ensure the colors are reset after printing

parser = _Parser()

class ColourSyntax:
    def print_file(self, filename: str, use_colours: bool = True, encoding: str = 'utf-8') -> None:
        with open(filename, 'r', encoding=encoding) as file:
            art = file.read()

        # Find all tags like <BOLD RED> or <UNDERLINE GREEN>
        tags = re.findall(r'<(.*?)>', art)

        if use_colours:
            # Parse the text to replace tags with ANSI codes
            art = parser._parse_text(art)

        if use_colours:
            print(_colours._style_utils['RESET'] + art + _colours._style_utils['RESET'])  # Ensure the colors are reset after printing
        else:
            print(art)

    def print_text(self, text: str, use_colours: bool = True) -> None:
        # Find all tags like <BOLD RED> or <UNDERLINE GREEN>
        tags = re.findall(r'<(.*?)>', text)

        if use_colours:
            # Parse the text to replace tags with ANSI codes
            text = parser._parse_text(text)

        if use_colours:
            print(_colours._style_utils['RESET'] + text + _colours._style_utils['RESET'])
        else:
            print(text)

    def input_tags(self, text: str, use_colours: bool = True, parse_input: bool = True) -> str:
        # Find all tags like <BOLD RED> or <UNDERLINE GREEN>
        tags = re.findall(r'<(.*?)>', text)
        if use_colours:
            # Parse the text to replace tags with ANSI codes
            text = parser._parse_text(text)
        
        if use_colours:
            if parse_input:
                return parser._parse_text(input(_colours._style_utils['RESET'] + text + _colours._style_utils['RESET']))
            else:
                return input(_colours._style_utils['RESET'] + text + _colours._style_utils['RESET'])
        else:
            if parse_input:
                return parser._parse_text(input(text))
            else:
                return input(text)


    def parse(self, text: str) -> str:
        text = parser._parse_text(text)
        return text
    
    def tags(self) -> LiteralString:
        keys = list()
        keys2 = list()
        keys.append('NORMAL CODES:\n\n')
        for i in range(0, 256):
            keys.append(f'<CODE{i}>CODE{i}')
        keys.append('\n\nBG CODES:\n\n')
        for i in range(0, 256):
            keys.append(f'<BGCODE{i}>BGCODE{i}')
        keys.append('\n\nPRESETS:\n\n')
        for key in list(_colours.colours_normal.keys()) + list(_colours.colours_background.keys()) + list(_colours.styles.keys()) + list(_colours.presets.keys()):
            if key != 'RESET':
                keys.append(f'<{key}>')
            keys.append(f'<{key}>{key}<RESET>')
        for key in keys:
            if key != 'RESET':
                keys2.append(parser._parse_text(key))
        return ", ".join(keys2).replace(', ', ' ')
    
class StyleSyntax:
    def __init__(self, spinner: list = ['|', '/', '-', '\\'], delay: float = 0.2):
        self.spinner = spinner
        self.delay = delay
        self.running = True

    def spin(self):
        while self.running:
            for frame in self.spinner:
                sys.stdout.write(f'\r{frame} ')  # Overwrite previous frame
                sys.stdout.flush()
                sleep(self.delay)
                if not self.running:
                    break  # Exit if flag is False

        sys.stdout.write('\rDone!\n')  # Clear spinner at the end


colour_syntax = ColourSyntax()
if __name__ == "__main__":
    system('cls' if name == 'nt' else 'clear')
    arg_parser = argparse.ArgumentParser(description='Print text with ANSI color codes.')
    arg_parser.add_argument('--text', type=str, help='text to print with colors', required=False)
    args = arg_parser.parse_args()
    if args.text:
        colour_syntax.print_text(args.text)
    else:
        time = datetime.datetime.now()
        print("COLOURMAN\nColourMan is a library made to help colour text by converting codes and presets into ANSI codes. Following is all the presets and codes:\n\n", colour_syntax.tags())
        colour_syntax.input_tags("<BGWHITE BLACK>Press enter to continue to the next page.")
        print(f"To use this library, you have a few options:\n\n1. Use the print_file method to print a file with ANSI color codes.\n2. Use the print_text method to print a string with ANSI color codes.\n3. Use the input_tags method to get user input with ANSI color codes.\n4. Use the parse method to parse a string with ANSI color codes.\n5. Use the tags method to get a list of all available tags and their corresponding ANSI codes.\n\nYour text tags should be in the format of `<TAG>value<TAG2>value2<RESET>`\n\nFor example:\n\n<RED>RED<RESET>\n<BGBLUE>BACKGROUND BLUE<RESET>\n<BOLD>Bold<RESET>\n<UNDERLINE>Underline<RESET>\n<DIM>Dim<RESET>\n<BRIGHT>Bright<RESET>\n{colour_syntax.parse('<RED>RED<RESET>\n<BGBLUE>BACKGROUND BLUE<RESET>\n<BOLD>Bold<RESET>\n<UNDERLINE>Underline<RESET>\n<DIM>Dim<RESET>\n<BRIGHT>Bright<RESET>\n\n')}\nYou can also use the <CODE0> to <CODE255> and <BGCODE0> to <BGCODE255> tags to set the text and background color respectively.\n\nFor example:\n\n<CODE51 BGCODE34 BOLD>Hello!\n{colour_syntax.parse('<CODE51 BGCODE34 BOLD>Hello!')}\n\nYou can also use the <RESET> tag to reset the text color and style. (This is optional, and not recommended)\n\nFor example:\n\n<RED>RED<RESET>\n<BGBLUE>BLUE<RESET>\n<BOLD>Bold<RESET>\n<UNDERLINE>Underline<RESET>\n<DIM>Dim<RESET>\n<BRIGHT>Bright<RESET>\n{colour_syntax.parse('<RED>RED<RESET>\n<BGBLUE>BLUE<RESET>\n<BOLD>Bold<RESET>\n<UNDERLINE>Underline<RESET>\n<DIM>Dim<RESET>\n<BRIGHT>Bright<RESET>\n\n')}\nYou can also use the <DARK> and <BRIGHT> tags to set the text color to dark or bright respectively.\n\nFor example:\n\n<DARK GREEN>DARK<RESET>\n<BRIGHT GREEN>BRIGHT<RESET>\n{colour_syntax.parse('\n<DARK GREEN>DARK<RESET>\n<BRIGHT GREEN>BRIGHT<RESET>')}\n(LIGHT and DARK can only be used on coloured text, and are unavailable for CODE)")
        time2 = datetime.datetime.now()
        elapsed_time = time2 - time
        colour_syntax.print_text(f"\n\n<DARK WHITE>Generated data in {elapsed_time.microseconds // 1000:04} milliseconds")