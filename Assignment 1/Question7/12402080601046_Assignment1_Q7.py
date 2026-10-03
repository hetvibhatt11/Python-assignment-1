class InvalidFormatError(Exception):
    pass
class UnknownVariableError(Exception):
    pass
class DivisionByZeroError(Exception):
    pass
class UnsupportedOperatorError(Exception):
    pass

# Calculator class
class Calculator:

    def __init__(self):
        self.variables = {}

    def get_value(self, value):
        # Check if value is a number
        try:
            return float(value)
        except ValueError:

            # Check if variable exists
            if value in self.variables:
                return self.variables[value]

            raise UnknownVariableError(
                "Unknown variable: " + value
            )

    def calculate(self, left, operator, right):

        left_value = self.get_value(left)
        right_value = self.get_value(right)

        if operator == "+":
            return left_value + right_value

        elif operator == "-":
            return left_value - right_value

        elif operator == "*":
            return left_value * right_value

        elif operator == "/":

            if right_value == 0:
                raise DivisionByZeroError(
                    "Cannot divide by zero"
                )

            return left_value / right_value

        elif operator == "%":

            if right_value == 0:
                raise DivisionByZeroError(
                    "Cannot perform modulo by zero"
                )

            return left_value % right_value

        else:
            raise UnsupportedOperatorError(
                "Unsupported operator: " + operator
            )

def main():

    calculator = Calculator()

    print("Enter formulas, assignments or quit:")

    while True:

        line = input().strip()

        # Stop program
        if line.lower() == "quit":
            break

        try:

            # Assignment such as x = 10
            if "=" in line:

                parts = line.split("=")

                if len(parts) != 2:
                    raise InvalidFormatError(
                        "Invalid assignment format"
                    )

                variable = parts[0].strip()
                value = parts[1].strip()

                # Check variable name
                if not variable.isidentifier():
                    raise InvalidFormatError(
                        "Invalid variable name"
                    )

                if value == "":
                    raise InvalidFormatError(
                        "Missing value"
                    )

                calculator.variables[variable] = (
                    calculator.get_value(value)
                )

                continue

            # Formula
            parts = line.split()

            if len(parts) != 3:
                raise InvalidFormatError(
                    "Formula must be: operand operator operand"
                )

            left = parts[0]
            operator = parts[1]
            right = parts[2]

            result = calculator.calculate(
                left, operator, right
            )

            # Print integer without .0
            if result.is_integer():
                print(int(result))
            else:
                print(result)

        except InvalidFormatError as error:
            print("InvalidFormatError")
            print(error)

        except UnknownVariableError as error:
            print("UnknownVariableError")
            print(error)

        except DivisionByZeroError as error:
            print("DivisionByZeroError")
            print(error)

        except UnsupportedOperatorError as error:
            print("UnsupportedOperatorError")
            print(error)

if __name__ == "__main__":
    main()
