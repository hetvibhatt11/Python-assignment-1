import sys

# Allows deeper recursive calls for large expressions
sys.setrecursionlimit(1000000)


# Dictionary to store variable definitions
variables = {}

# Dictionary to store already calculated values
memo = {}

# Set to keep track of variables currently being evaluated
visiting = set()


class ExpressionParser:
    """Parser for arithmetic expressions."""

    def __init__(self, expression):
        self.expression = expression
        self.position = 0

    def skip_spaces(self):
        """Skip spaces in the expression."""

        while (
            self.position < len(self.expression)
            and self.expression[self.position].isspace()
        ):
            self.position += 1

    def parse(self):
        """Parse the complete expression."""

        value = self.parse_expression()

        self.skip_spaces()

        # Extra characters mean invalid syntax
        if self.position != len(self.expression):
            raise ValueError("Invalid expression")

        return value

    def parse_expression(self):
        """
        expression = term { (+ | -) term }
        """

        value = self.parse_term()

        while True:
            self.skip_spaces()

            if self.position >= len(self.expression):
                break

            operator = self.expression[self.position]

            if operator not in "+-":
                break

            self.position += 1

            right = self.parse_term()

            if operator == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term(self):
        """
        term = factor { * factor }
        """

        value = self.parse_factor()

        while True:
            self.skip_spaces()

            if (
                self.position < len(self.expression)
                and self.expression[self.position] == "*"
            ):
                self.position += 1

                right = self.parse_factor()

                value *= right

            else:
                break

        return value

    def parse_factor(self):
        """
        factor = number
               | variable
               | ( expression )
        """

        self.skip_spaces()

        if self.position >= len(self.expression):
            raise ValueError("Invalid expression")

        # Handle parentheses
        if self.expression[self.position] == "(":

            self.position += 1

            value = self.parse_expression()

            self.skip_spaces()

            if (
                self.position >= len(self.expression)
                or self.expression[self.position] != ")"
            ):
                raise ValueError("Missing closing parenthesis")

            self.position += 1

            return value

        # Handle non-negative integer
        if self.expression[self.position].isdigit():

            start = self.position

            while (
                self.position < len(self.expression)
                and self.expression[self.position].isdigit()
            ):
                self.position += 1

            return int(
                self.expression[start:self.position]
            )

        # Handle variable name
        if self.expression[self.position].isalpha():

            start = self.position

            while (
                self.position < len(self.expression)
                and (
                    self.expression[self.position].isalnum()
                    or self.expression[self.position] == "_"
                )
            ):
                self.position += 1

            name = self.expression[
                start:self.position
            ]

            return evaluate_variable(name)

        raise ValueError("Invalid character")


def evaluate_variable(name):
    """
    Evaluate a variable recursively.

    Memoization avoids repeated calculations.
    The visiting set detects cyclic dependencies.
    """

    # If already calculated, return stored value
    if name in memo:
        return memo[name]

    # If currently being evaluated, a cycle exists
    if name in visiting:
        raise RuntimeError("CYCLE")

    # Variable does not exist
    if name not in variables:
        raise ValueError("Undefined variable")

    # Mark variable as being evaluated
    visiting.add(name)

    try:
        parser = ExpressionParser(
            variables[name]
        )

        value = parser.parse()

        # Store result for future use
        memo[name] = value

        return value

    finally:
        # Remove variable after evaluation
        visiting.remove(name)


def main():
    """Main function."""

    try:
        print("=== Recursive Expression Engine ===")
        print()

        # ----------------------------------------------------
        # Input number of variables
        # ----------------------------------------------------
        print("Enter the number of variable definitions.")
        print("Example: 3")

        v = int(input("Number of variables: "))

        if not 1 <= v <= 200000:
            raise ValueError(
                "Number of variables must be between 1 and 200000."
            )

        print()
        print("Now enter each variable definition.")
        print("Format: variable = expression")
        print("Example: a = 2 + 3")
        print()

        # ----------------------------------------------------
        # Input variable definitions
        # ----------------------------------------------------
        for i in range(1, v + 1):

            line = input(
                f"Enter variable definition {i}: "
            ).strip()

            if "=" not in line:
                raise ValueError(
                    "Invalid variable definition. "
                    "Use the format: a = 2 + 3"
                )

            name, expression = line.split("=", 1)

            name = name.strip()
            expression = expression.strip()

            # Validate variable name
            if not name:
                raise ValueError(
                    "Variable name cannot be empty."
                )

            if not name[0].isalpha():
                raise ValueError(
                    "Variable name must start with a letter."
                )

            if not all(
                ch.isalnum() or ch == "_"
                for ch in name
            ):
                raise ValueError(
                    "Variable name can contain only "
                    "letters, digits and underscore."
                )

            if not expression:
                raise ValueError(
                    "Expression cannot be empty."
                )

            variables[name] = expression

        # ----------------------------------------------------
        # Input final expression
        # ----------------------------------------------------
        print()
        print("Enter the expression you want to evaluate.")
        print("Example: c + 10")

        final_expression = input(
            "Expression to evaluate: "
        ).strip()

        if not final_expression:
            raise ValueError(
                "Expression cannot be empty."
            )

        # ----------------------------------------------------
        # Evaluate final expression
        # ----------------------------------------------------
        parser = ExpressionParser(final_expression)

        result = parser.parse()

        print()
        print("Result:", result)

    except RuntimeError as error:

        if str(error) == "CYCLE":
            print()
            print("Result: CYCLE")
        else:
            print()
            print("Result: INVALID")

    except (ValueError, RecursionError):

        print()
        print("Result: INVALID")


# Start the program
if __name__ == "__main__":
    main()

