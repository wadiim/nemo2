# Nemo2

Nemo2 is a command-line program for learning foreign languages.

## Usage

``` shell
nemo2.py [options] [file...]
```

It reads any number of word lists and tests your knowledge of them. If no file is specified then `nemo2.py` reads from the standard input.

### Options

Option | Meaning |
--- | ---
`-h`, `--help` | Show help message and exit.
`-n NUM`, `--lines NUM` | Specify how many lines to load. If the value is greater than or equal to the total number of lines, all lines are loaded.
`-o TYPE`, `--order TYPE` | Specify in which order the lines will be loaded. Possible values are `random` and `file`. The latter loads lines in order in which they appear in the file(s).

### Syntax

To separate text from its translation(s) use `-`. Translations can be separated using `|` character.
```
elite - leet | l33t | 1337 | 31337
```
To make a part of translation optional, enclose it in parentheses.
```
own - pwn(age)
```
If the translations are mostly overlapping, merge them into one translation, enclose in square brackets the part of it which varies and separate alternations by `|`.
```
hacks - h[a|4]x
```
To turn off special meaning of `-`, `|`, `(` and `)` characters, precede them by backslash. When there are multiple non escaped hyphens, only the first one is treated specially.
```
hacker - H4X0R3r | \|-\|4x0.-
```
Whitespaces around `-` and `|` have no effect. Also leading and trailing whitespaces are ignored. Multiple spaces are treated as a single one.

## License

[MIT](https://github.com/wadiim/nemo2/blob/master/LICENSE)
