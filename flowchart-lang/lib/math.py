# libs/math_lib.py

def add_command(interpreter, args):
    """
    Implements the ADD command.
    Example usage: ADD result_var = val1 + val2
    """
    try:
        dest_var, expr = args.split("=", 1)
        dest_var = dest_var.strip()
        
        val1_str, val2_str = expr.split("+", 1)
        val1 = interpreter._get_value(val1_str.strip())
        val2 = interpreter._get_value(val2_str.strip())
        
        if isinstance(val1, int) and isinstance(val2, int):
            interpreter.variables[dest_var] = val1 + val2
        else:
            print(f"Error: ADD command requires two numbers. Received: {val1} and {val2}.")
            sys.exit(1)
            
    except ValueError:
        print(f"Error: Invalid ADD statement: '{args}'. Expected 'VAR = NUM1 + NUM2'.")
        sys.exit(1)

# Dictionary that maps FCL command names to Python functions.
# The interpreter will find and use this dictionary to extend its command set.
commands = {
    "ADD": add_command,
}
