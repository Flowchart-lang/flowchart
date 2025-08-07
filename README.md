# Flowchart-Lang (FCL)

**Flowchart-Lang (FCL)** is a simple, experimental programming language designed to mimic the sequential and conditional logic of flowcharts. It's interpreted by a Python script and is intended for learning basic programming concepts.

---

## Getting Started

To run FCL programs, you'll need the FCL interpreter and a simple batch file wrapper (for Windows).

### 1. Prerequisites

* **Python 3**: Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/). Make sure it's added to your system's `PATH` during installation.

### 2. Setup

#### Save the Interpreter

* Save the interpreter code (typically named `flowchart.py`) to a directory, for example:

  * `C:\FlowchartLang\flowchart.py`

#### Create the Launcher (Windows)

* In the same directory as `flowchart.py`, create a new file named `flowchart.bat`.
* Open `flowchart.bat` with a text editor and add the following content:

```bat
@echo off
python "%~dp0flowchart.py" %*
```

This batch file allows you to run your FCL programs directly using the `flowchart` command.

---

## How to Code in FCL

FCL programs are plain text files with the `.fcl` extension. Each command typically occupies its own line.

### Basic Structure

Every FCL program must begin with `START` and end with `END`:

```fcl
START
    -- Your FCL commands go here --
END
```

### Comments

* Lines starting with `--` are treated as comments and ignored by the interpreter.

---

## Commands

### `START`

* **Purpose**: Marks the beginning of your program.
* **Usage**:

  ```fcl
  START
  ```

### `END`

* **Purpose**: Marks the end of your program. The interpreter will stop execution when it reaches this command.
* **Usage**:

  ```fcl
  END
  ```

### `PRINT`

* **Purpose**: Displays text or the value of a variable to the console.
* **Usage**:

  ```fcl
  PRINT "Your text"
  PRINT variableName
  PRINT "Text " + variableName
  ```
* **Examples**:

  ```fcl
  PRINT "Hello, World!"
  PRINT myVariable
  PRINT "My name is: " + userName
  ```

### `SET`

* **Purpose**: Assigns a value to a variable.
* **Usage**:

  ```fcl
  SET variableName = value
  ```
* **Examples**:

  ```fcl
  SET message = "Welcome!"
  SET age = 30
  SET userAge = age
  ```

### `INPUT`

* **Purpose**: Reads a line of text entered by the user and stores it in the specified variable.
* **Usage**:

  ```fcl
  INPUT variableName
  ```
* **Example**:

  ```fcl
  PRINT "What is your favorite color?"
  INPUT favoriteColor
  PRINT "You like " + favoriteColor + "!"
  ```

### `IF / ELSE / ENDIF`

* **Purpose**: Implements conditional logic.
* **Supported Operators**: `==` (equals), `!=` (not equals)
* **Usage**:

  ```fcl
  IF variable == value
      -- Code to execute if condition is true --
  ELSE
      -- Code to execute if condition is false (optional) --
  ENDIF
  ```
* **Examples**:

  ```fcl
  IF userName == "Alice"
      PRINT "Hello, Alice!"
  ELSE
      PRINT "You're not Alice."
  ENDIF

  SET score = 95
  IF score != 100
      PRINT "Not a perfect score."
  ENDIF
  ```

### `WHILE / ENDWHILE`

* **Purpose**: Implements a loop that repeats as long as the condition is true.
* **Supported Operators**: `==`, `!=`
* **Usage**:

  ```fcl
  WHILE variable != value
      -- Code to execute in the loop --
  ENDWHILE
  ```
* **Example**:

  ```fcl
  SET count = 0
  WHILE count != 5
      PRINT "Count is: " + count
      INCREMENT count
  ENDWHILE
  ```

### `INCREMENT`

* **Purpose**: Increases the value of a numeric variable by 1.
* **Usage**:

  ```fcl
  INCREMENT variableName
  ```
* **Example**:

  ```fcl
  INCREMENT count
  ```

---

## Running an FCL Program

Once you have `flowchart.py` and `flowchart.bat` set up, and an `.fcl` program file (e.g., `myprogram.fcl`), you can run it from your Command Prompt:

### Steps

1. Open **Command Prompt**.
2. Navigate to your FCL program's directory:

   ```cmd
   cd C:\Path\To\Your\FCL\Files
   ```
3. Execute your program:

   ```cmd
   flowchart -r myprogram.fcl
   ```

---

## Example FCL Program

Here's an example of an FCL program (`example.fcl`):

```fcl
START
-- This program uses a WHILE loop to count from 0 to 4.

PRINT "Starting the counting loop..."
SET count = 0

WHILE count != 5
    PRINT "The current count is: " + count
    INCREMENT count
ENDWHILE

PRINT "The loop has finished!"
END
```

---

## Error Handling

* The interpreter will display an error message and exit if you use an undefined variable, invalid syntax, or mismatched control blocks (e.g., missing `ENDIF` or
