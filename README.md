# Flowchart-Lang (FCL)

**Flowchart-Lang (FCL)** is a simple, experimental programming language designed to mimic the sequential and conditional logic of flowcharts. It's interpreted by a Python script and is intended for learning basic programming concepts.

## Getting Started

To run FCL programs, you'll need the FCL interpreter, a package manager, and a simple batch file wrapper (for Windows).

### 1. Prerequisites

* **Python 3**: Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/). Make sure it's added to your system's `PATH` during installation.

* **Requests Library**: The package manager requires the `requests` library to download files. Install it by running:
     `pip install requests`

### 2. Setup

#### Save the Interpreter

* Save the interpreter code (typically named `flowchart.py`) to a directory, for example:

  * `C:\FlowchartLang\flowchart.py`

#### Create the Launchers (Windows)

* In the same directory as `flowchart.py`, create two new batch files: `flowchart.bat` and `fpm.bat`.

* Open `flowchart.bat` with a text editor and add the following content:

```
@echo off
python "%~dp0flowchart.py" %*

```

* Open `fpm.bat` with a text editor and add this content:

```
@echo off
python "%~dp0package-manager.py" %*

```

These batch files allow you to run your FCL programs and the FCL Package Manager directly from the command line.

## FCL Package Manager (`fpm`)

The FCL Package Manager (`fpm`) is a command-line tool for installing new libraries from the official FCL library repository.

### Commands

* **Install a Library**: Use the `-i` or `--install` flag followed by the library's name. The package manager will download the Python file and place it in your local `libs/` directory.

   CMD: `fpm -i library_name    `

### Example

To install the `math` library, you would run:

   CMD: `fpm -i math    `

## How to Code in FCL

FCL programs are plain text files with the `.fcl` extension. Each command typically occupies its own line.

### Basic Structure

Every FCL program must begin with `START` and end with `END`:

```
START
    -- Your FCL commands go here --
END

```

### Comments

* Lines starting with `--` are treated as comments and ignored by the interpreter.

## Commands & Extending FCL

### `START`

* **Purpose**: Marks the beginning of your program.

* **Usage**:

  `fcl   START   `

### `END`

* **Purpose**: Marks the end of your program. The interpreter will stop execution when it reaches this command.

* **Usage**:

  `fcl   END   `

### `PRINT`

* **Purpose**: Displays text or the value of a variable to the console.

* **Usage**:

  `fcl   PRINT "Your text"   PRINT variableName   PRINT "Text " + variableName   `

* **Examples**:

  `fcl   PRINT "Hello, World!"   PRINT myVariable   PRINT "My name is: " + userName   `

### `SET`

* **Purpose**: Assigns a value to a variable.

* **Usage**:

  `fcl   SET variableName = value   `

* **Examples**:

  `fcl   SET message = "Welcome!"   SET age = 30   SET userAge = age   `

### `INPUT`

* **Purpose**: Reads a line of text entered by the user and stores it in the specified variable.

* **Usage**:

  `fcl   INPUT variableName   `

* **Example**:

  `fcl   PRINT "What is your favorite color?"   INPUT favoriteColor   PRINT "You like " + favoriteColor + "!"   `

### `IF / ELSE / ENDIF`

* **Purpose**: Implements conditional logic.

* **Supported Operators**: `==` (equals), `!=` (not equals)

* **Usage**:

  `fcl   IF variable == value       -- Code to execute if condition is true --   ELSE       -- Code to execute if condition is false (optional) --   ENDIF   `

* **Examples**:

  \`\`\`fcl
  IF userName == "Alice"
      PRINT "Hello, Alice!"
  ELSE
      PRINT "You're not Alice."
  ENDIF

  SET score = 95
  IF score != 100
      PRINT "Not a perfect score."
  ENDIF
  \`\`\`

### `WHILE / ENDWHILE`

* **Purpose**: Implements a loop that repeats as long as the condition is true.

* **Supported Operators**: `==`, `!=`

* **Usage**:

  `fcl   WHILE variable != value       -- Code to execute in the loop --   ENDWHILE   `

* **Example**:

  `fcl   SET count = 0   WHILE count != 5       PRINT "Count is: " + count       INCREMENT count   ENDWHILE   `

### `INCREMENT`

* **Purpose**: Increases the value of a numeric variable by 1.

* **Usage**:

  `fcl   INCREMENT variableName   `

* **Example**:

  `fcl   INCREMENT count   `

### Extending FCL with Libraries

FCL supports custom commands via Python libraries. The FCL Package Manager (`fpm`) is the recommended way to install and manage these libraries. Once a library is installed, you can use its commands in your FCL programs.

#### Example: `math` Library

Install the `math` library using `fpm -i math`. It adds an `ADD` command:

```
ADD result = a + b

```

#### Example: `random` Library

Install the `random` library using `fpm -i random`. It adds a `RANDOM` command to generate a random integer within a range:

```
RANDOM result = 1, 10

```

## Running an FCL Program

Once you have `flowchart.py`, `flowchart.bat`, and `fpm.bat` set up, and an `.fcl` program file (e.g., `myprogram.fcl`), you can run it from your Command Prompt:

### Steps

1. Open **Command Prompt**.

2. Navigate to your FCL program's directory:

   `cmd    cd C:\Path\To\Your\FCL\Files    `
3. Execute your program:

   `cmd    flowchart -r myprogram.fcl    `

## Example FCL Programs

### Basic Example

```
START
PRINT "Welcome to your first FCL application!"
PRINT "Please enter your name:"
INPUT userName
PRINT "Hello, " + userName + "!"

IF userName == "Alice"
    PRINT "Hello, Alice!"
ELSE
    PRINT "That's a nice name too!"
ENDIF

SET favoriteNumber = 42
PRINT "Your favorite number is: " + favoriteNumber

IF favoriteNumber != 100
    PRINT "That's not 100!"
ELSE
    PRINT "Wow, 100 is a great number!"
ENDIF

PRINT "This is a simple application with conditional logic."
END

```

### Advanced Example: Fibonacci Sequence

This example uses the `ADD` command from the math library:

```
START
-- This program calculates and prints the Fibonacci sequence.
SET a = 0
SET b = 1
SET n = 10
SET counter = 0
-- The 'IMPORT math' command is optional as all libs are pre-loaded
PRINT "Starting Fibonacci sequence generation..."
WHILE counter != n
    PRINT a
    ADD next_fib = a + b
    SET a = b
    SET b = next_fib
    INCREMENT counter
ENDWHILE
PRINT "Fibonacci sequence finished!"
END

```

## Error Handling

* The interpreter will display an error message and exit if you use an undefined variable, invalid syntax, or mismatched control blocks (e.g., missing `ENDIF` or `ENDWHILE`).

* Custom libraries can also print errors if their commands are used incorrectly.

## Creating Your Own Library

To add new commands, create a Python file in the `libs/` folder. Each library must define a `commands` dictionary mapping FCL command names to Python functions.
