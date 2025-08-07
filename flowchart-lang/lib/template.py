# libs/template.py

# This is a template for creating a new library for the Flowchart-Lang interpreter.
# Save this file inside the 'libs' folder.

def my_new_command(interpreter, args):
    """
    Implements a new custom FCL command.
    All command functions must accept two arguments:
    - interpreter: The main FlowchartInterpreter instance.
    - args: A string containing all arguments passed to the command.

    Example Usage: MY_COMMAND "Hello, World!"
    """
    # Use the interpreter instance to access and modify the program's state.

    # Access a variable from the program
    # my_var = interpreter.variables.get("my_variable_name")

    # Get the value of an FCL token (can be a string, number, or variable)
    # my_value = interpreter._get_value(args)

    # Example: A command that prints a custom message.
    print(f"[MY_COMMAND] A custom command was executed with argument: {args}")

    # You can also update variables in the interpreter.
    # interpreter.variables["new_variable"] = "some value"

    # For more complex parsing of 'args', you can use string methods like split().
    # For example, to handle "VAR = VALUE":
    # try:
    #     var_name, value_expr = args.split("=", 1)
    #     var_name = var_name.strip()
    #     value_expr = value_expr.strip()
    #     value = interpreter._get_value(value_expr)
    #     interpreter.variables[var_name] = value
    # except ValueError:
    #     print(f"Error: Invalid MY_COMMAND statement: '{args}'")
    #     sys.exit(1)


# The 'commands' dictionary is the most important part of the library.
# The interpreter looks for this dictionary to find all the new commands
# provided by your library. The keys are the FCL command names, and the
# values are the Python functions that implement them.
commands = {
    "MY_COMMAND": my_new_command,
    # You can add more commands to your library like this:
    # "ANOTHER_COMMAND": another_command_function,
}
