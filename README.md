
# Hadron Assembler

Hadron Assembler is a custom assembler made to create scripts and programs
in the Hadron Assembly Language, based on [URCL](https://github.com/ModPunchtree/URCL).
This assembler creates machine code and schematics designed for custom Minecraft CPUs.  
This assembler is written in Python, and is designed for a personal usage.

## Table of Contents

- [Hadron Assembler](#hadron-assembler)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command line syntax](#command-line-syntax)
    - [Positional arguments](#positional-arguments)
    - [Optional arguments](#optional-arguments)
  - [Assembly language syntax](#assembly-language-syntax)
  - [Progress](#progress)
    - [Side projects](#side-projects)
  - [Examples](#examples)
    - [Source code](#source-code)
    - [Compiled result](#compiled-result)
  - [Documentation](#documentation)
  - [License](#license)

## Installation

Clone the git repository or download the source code as a `.zip`, and extract it in a folder.
You can clone the repository with the following command:

```bash
git clone https://github.com/Enderdodo974/hadron-assembler.git
```

## Usage

```bash
python3 hadron-assembler.py [-h] [-o OUTPUT] [-s SCHEMATIC] [-v] [-q] [-d] [-V] INPUT_FILES...
```

### Command line syntax

The command line syntax and arguments can be found in the documentation.

### Positional arguments

| Argument      | Description                          |
|---------------|--------------------------------------|
| `file` | The input file or files to assemble. |

### Optional arguments

| Argument         | Description                                       |
|------------------|---------------------------------------------------|
| `-h` `--help`    | Print the help message and exit.                  |
| `-V` `--version` | Print the version number and exit.                |
| `-v` `--verbose` | Print verbose output. Can be used multiple times. |
| `-q` `--quiet`   | Don't print any output, except for errors.        |
| `-d` `--debug`   | Print debug output. Equivalent to `-vv`.          |

## Assembly language syntax

This assembler uses a custom assembly language, called Hadron Assembly Language (HASM).
The syntax is based on the URCL syntax, with some modifications.  
The assembly language syntax is detailed in the documentation.

## Progress

- [x] Set-up the project
- [x] Create the CLI
- [x] Parse source code to tokens
- [ ] Construct AST from tokens
- [ ] Preprocess source code
- [ ] Resolve labels
- [ ] Read ISA from a template (JSON/dict)
- [ ] Translate to machine code
- [ ] Add instructions translations
- [ ] Export to a schematic

### Side projects

- [ ] Create a custom CPU
  - [x] ALU
  - [x] Register file
  - [x] ROM
  - [ ] RAM
  - [ ] IO
  - [ ] Control Unit
  - [ ] other
- [x] Create a syntax highlighting extension for VSCode
- [ ] Create an emulator to test various programs
- [ ] Create a compiler from C to HASM

## Examples

The script folder contains some example programs written in HASM.
Here's a Hello World program:

### Source code

```hasm
// Hello World program
// Prints "Hello World!" to the screen

bits == 8
minreg 3
run ROM

.message
  dw "Hello World!"

.begin
  ldi r1 .message // Load the pointer to the message in r1
  .loop
    lod r2 r1     // Load the current character pointed to
    cmp r2 r0     // Test if it's the null terminator \0
    jz .end       // Break out of the loop if it is
    out %text r2  // Output the character
    inc r1 r1     // Increment the pointer
    jmp .loop     // Loop again

.end
  hlt             // Halt the CPU
```

### Compiled result

```txt

```

## Documentation

The LaTeX documentations for both the command line arguments of the compiler
and the assembly language are available in the docs folder.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
