#!/usr/bin/env python3
# flowchart.py

import sys
import os
import importlib.util

# --- BUILT-IN COMMAND IMPLEMENTATIONS ---
# All command functions now explicitly take 'interpreter' and 'args'
# as their arguments, just like library functions.

def _command_start(interpreter, args):
    pass # Handled by initial checks

def _command_end(interpreter, args):
    print("\n[SYSTEM] Program finished.")
    # Stop the execution loop by setting the index past the end
    interpreter.current_line_index = len(interpreter.program_lines)

def _command_print(interpreter, args):
    output_parts = []
    current_part = ""
    in_string = False
    for char in args:
        if char == '"':
            in_string = not in_string
            current_part += char
        elif char == '+' and not in_string:
            output_parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    output_parts.append(current_part.strip())

    final_output = []
    for part in output_parts:
        final_output.append(str(interpreter._get_value(part)))
    print("".join(final_output))

def _command_set(interpreter, args):
    try:
        var_name, value_expr = args.split('=', 1)
        var_name = var_name.strip()
        value_expr = value_expr.strip()
        value = interpreter._get_value(value_expr)
        interpreter.variables[var_name] = value
    except ValueError:
        print(f"Error: Invalid SET statement: '{args}'")
        sys.exit(1)

def _command_input(interpreter, args):
    try:
        var_name = args.strip()
        user_input = input()
        interpreter.variables[var_name] = user_input
    except Exception as e:
        print(f"Error during INPUT: {e}")
        sys.exit(1)
        
def _command_increment(interpreter, args):
    var_name = args.strip()
    if var_name in interpreter.variables and isinstance(interpreter.variables[var_name], int):
        interpreter.variables[var_name] += 1
    else:
        print(f"Error: Cannot INCREMENT variable '{var_name}'. It must be a number.")
        sys.exit(1)

def _command_if(interpreter, args):
    condition_met = interpreter._evaluate_condition(args.strip())
    interpreter.execution_stack.append(condition_met)
    if not condition_met:
        jump_to_index = interpreter._find_matching_end_block(interpreter.current_line_index + 1, "IF", "ENDIF")
        if jump_to_index is not None:
            interpreter.current_line_index = jump_to_index - 1
        else:
            print(f"Error: Mismatched IF/ELSE/ENDIF at line {interpreter.current_line_index + 1}")
            sys.exit(1)

def _command_else(interpreter, args):
    interpreter.execution_stack.pop()
    interpreter.execution_stack.append(False)
    jump_to_index = interpreter._find_matching_end_block(interpreter.current_line_index + 1, "IF", "ENDIF")
    if jump_to_index is not None:
        interpreter.current_line_index = jump_to_index - 1
    else:
        print(f"Error: Mismatched ELSE/ENDIF at line {interpreter.current_line_index + 1}")
        sys.exit(1)

def _command_endif(interpreter, args):
    interpreter.execution_stack.pop()
    
def _command_while(interpreter, args):
    condition_met = interpreter._evaluate_condition(args.strip())
    if condition_met:
        interpreter.loop_stack.append(interpreter.current_line_index)
    else:
        jump_to_index = interpreter._find_matching_end_block(interpreter.current_line_index + 1, "WHILE", "ENDWHILE")
        if jump_to_index is not None:
            interpreter.current_line_index = jump_to_index - 1
        else:
            print(f"Error: Mismatched WHILE/ENDWHILE at line {interpreter.current_line_index + 1}")
            sys.exit(1)

def _command_endwhile(interpreter, args):
    if interpreter.loop_stack:
        loop_start_index = interpreter.loop_stack.pop()
        interpreter.current_line_index = loop_start_index - 1
    else:
        print(f"Error: ENDWHILE without a matching WHILE at line {interpreter.current_line_index + 1}")
        sys.exit(1)
        
def _command_import(interpreter, args):
    # This command is handled by the initial _load_libraries call.
    # It's kept here for command registry consistency but does nothing at runtime.
    pass

# Dictionary of built-in commands
BUILT_IN_COMMANDS = {
    "START": _command_start,
    "END": _command_end,
    "PRINT": _command_print,
    "SET": _command_set,
    "INPUT": _command_input,
    "INCREMENT": _command_increment,
    "IF": _command_if,
    "ELSE": _command_else,
    "ENDIF": _command_endif,
    "WHILE": _command_while,
    "ENDWHILE": _command_endwhile,
    "IMPORT": _command_import,
}

class FlowchartInterpreter:
    """
    A simple interpreter for the Flowchart Language (FCL).
    Supports basic operations: START, END, PRINT, SET, INPUT, IF, ELSE, ENDIF.
    Also supports single-line comments starting with '--', WHILE loops and INCREMENT.
    This version includes a library system via the 'IMPORT' command.
    """

    def __init__(self, step_by_step_mode=False):
        self.variables = {}
        self.program_lines = []
        self.current_line_index = 0
        self.loop_stack = []
        self.step_by_step_mode = step_by_step_mode
        self._commands = BUILT_IN_COMMANDS.copy()
        self._load_libraries()

    def _load_libraries(self):
        """Loads all Python modules from the 'libs' directory."""
        libs_dir = os.path.join(os.path.dirname(__file__), "libs")
        if not os.path.exists(libs_dir):
            if self.step_by_step_mode:
                print("[SYSTEM] Warning: 'libs' directory not found. No external libraries loaded.")
            return

        for filename in os.listdir(libs_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                file_path = os.path.join(libs_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec is None:
                        raise ImportError(f"Could not load spec for {filename}")
                    
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, 'commands'):
                        # Add commands from the library to the interpreter's registry
                        for command_name, command_func in module.commands.items():
                            self._commands[command_name] = command_func
                            
                    if self.step_by_step_mode:
                        print(f"[SYSTEM] Loaded library '{module_name}' from '{filename}'.")

                except Exception as e:
                    print(f"Error loading library '{filename}': {e}")
                    sys.exit(1)


    def load_program(self, file_path):
        """
        Loads the FCL program from the specified file,
        ignoring empty lines and lines starting with '--' (comments).
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'")
            sys.exit(1)

        with open(file_path, 'r') as f:
            self.program_lines = [
                line.strip() for line in f
                if line.strip() and not line.strip().startswith('--')
            ]

        if not self.program_lines:
            print("Error: Empty program file or only comments.")
            sys.exit(1)

        if self.program_lines[0] != "START":
            print("Error: Program must begin with 'START'.")
            sys.exit(1)
        if self.program_lines[-1] != "END":
            print("Error: Program must end with 'END'.")
            sys.exit(1)

    def _get_value(self, token):
        """
        Helper to get the actual value of a token,
        either a string literal, a number, or a variable's value.
        """
        if isinstance(token, str):
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]
            elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                return int(token)
            elif token in self.variables:
                return self.variables[token]
            else:
                print(f"Error: Undefined variable or invalid literal '{token}'")
                sys.exit(1)
        return token

    def _evaluate_condition(self, condition_str):
        """
        Evaluates a boolean condition (e.g., "var == value" or "var != value").
        """
        parts = []
        operator = None
        if '==' in condition_str:
            parts = condition_str.split('==', 1)
            operator = '=='
        elif '!=' in condition_str:
            parts = condition_str.split('!=', 1)
            operator = '!='
        else:
            print(f"Error: Invalid condition format: '{condition_str}'. Expected 'VAR == VALUE' or 'VAR != VALUE'.")
            sys.exit(1)

        if len(parts) != 2:
            print(f"Error: Malformed condition: '{condition_str}'")
            sys.exit(1)

        var_name = parts[0].strip()
        expected_value_str = parts[1].strip()

        if var_name not in self.variables:
            print(f"Error: Undefined variable '{var_name}' in condition.")
            sys.exit(1)

        actual_value = self.variables[var_name]
        expected_value = self._get_value(expected_value_str)

        if operator == '==':
            return actual_value == expected_value
        elif operator == '!=':
            return actual_value != expected_value
        return False

    def _find_matching_end_block(self, start_index, start_keyword, end_keyword):
        """
        Finds the matching END block for a given START block.
        """
        level = 0
        for i in range(start_index, len(self.program_lines)):
            line = self.program_lines[i].strip()
            if line.startswith(start_keyword):
                level += 1
            elif line == end_keyword:
                if level == 0:
                    return i + 1
                else:
                    level -= 1
        return None

    def execute(self):
        """
        Executes the loaded FCL program.
        """
        # This flag indicates if we are currently skipping lines because
        # an IF condition was false, or we are in an ELSE block after a true IF.
        self.execution_stack = [True]

        while self.current_line_index < len(self.program_lines):
            line = self.program_lines[self.current_line_index]
            parts = line.split(' ', 1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""

            if self.step_by_step_mode:
                print(f"\n[STEP {self.current_line_index + 1}] Executing: '{line}'")
                input("Press Enter to continue...")

            if self.execution_stack[-1]:
                if command in self._commands:
                    command_func = self._commands[command]
                    # This call is now consistent for all command functions.
                    command_func(self, args)
                else:
                    print(f"Error: Unknown command '{command}' on line {self.current_line_index + 1}: '{line}'")
                    sys.exit(1)
            else:
                if command in ["IF", "WHILE"]:
                    self.execution_stack.append(False)
                elif command in ["ELSE", "ENDIF", "ENDWHILE"]:
                    self.execution_stack.pop()
                pass

            self.current_line_index += 1


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ["-r", "-s"]:
        print("Usage: flowchart -r <file.fcl> or flowchart -s <file.fcl>")
        sys.exit(1)

    mode = sys.argv[1]
    file_path = sys.argv[2]
    
    step_by_step = (mode == "-s")
    
    interpreter = FlowchartInterpreter(step_by_step_mode=step_by_step)
    interpreter.load_program(file_path)
    interpreter.execute()

if __name__ == "__main__":
    main()
