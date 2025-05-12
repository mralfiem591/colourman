# ColourMan

ColourMan is a Python library that allows you to print text with ANSI color codes, making it easy to add color and formatting to your terminal output.

## Installation

To use ColourMan, simply copy the `colourman.py` file into your project directory.

## Usage

Here are the main methods provided by the `ColourSyntax` class:

### `print_file(filename, use_colours=True, encoding='utf-8')`

Prints the contents of a file with ANSI color codes.

### `print_text(text, use_colours=True)`

Prints a string with ANSI color codes.

### `input_tags(text, use_colours=True, parse_input=True)`

Prompts the user for input with ANSI color codes.

### `parse(text)`

Parses a string with ANSI color codes and returns the formatted text.

### `tags()`

Returns a string containing all available tags and their corresponding ANSI codes.

## API

The `ColourSyntax` class provides the following attributes and methods:

- `print_file()`, `print_text()`, `input_tags()`, `parse()`, `tags()`: See the usage section above.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/mralfiem591/colourman).

## License

This project is licensed under the [MIT License](LICENSE).
