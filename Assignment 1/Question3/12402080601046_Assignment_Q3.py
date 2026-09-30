# Recursive Expression Engine with Memoization

variables = {}
memo = {}
visiting = set()


def evaluate_variable(name):
    # Return already calculated value
    if name in memo:
        return memo[name]

    # Check for cyclic dependency
    if name in visiting:
        raise ValueError("CYCLE")

    # Check whether variable exists
    if name not in variables:
        raise ValueError("INVALID")

    visiting.add(name)

    value = evaluate_expression(variables[name])

    visiting.remove(name)

    # Store result for memoization
    memo[name] = value

    return value


def evaluate_expression(expression):
    expression = expression.replace(" ", "")

    if expression == "":
        raise ValueError("INVALID")

    tokens = []
    i = 0

    # Convert expression into tokens
    while i < len(expression):

        # Number
        if expression[i].isdigit():
            number = ""

            while i < len(expression) and expression[i].isdigit():
                number += expression[i]
                i += 1

            tokens.append(("number", number))

        # Variable
        elif expression[i].isalpha():
            name = ""

            while i < len(expression) and expression[i].isalnum():
                name += expression[i]
                i += 1

            tokens.append(("variable", name))

        # Operators and brackets
        elif expression[i] in "+-*()":
            tokens.append((expression[i], expression[i]))
            i += 1

        else:
            raise ValueError("INVALID")

    position = 0

    # Handles + and -
    def parse_expression():
        nonlocal position

        value = parse_term()

        while position < len(tokens):

            operator = tokens[position][0]

            if operator == "+":
                position += 1
                value += parse_term()

            elif operator == "-":
                position += 1
                value -= parse_term()

            else:
                break

        return value

    # Handles *
    def parse_term():
        nonlocal position

        value = parse_factor()

        while position < len(tokens):

            if tokens[position][0] == "*":
                position += 1
                value *= parse_factor()
            else:
                break

        return value

    # Handles numbers, variables and parentheses
    def parse_factor():
        nonlocal position

        if position >= len(tokens):
            raise ValueError("INVALID")

        token_type, token_value = tokens[position]

        # Number
        if token_type == "number":
            position += 1
            return int(token_value)

        # Variable
        if token_type == "variable":
            position += 1
            return evaluate_variable(token_value)

        # Parentheses
        if token_type == "(":
            position += 1

            value = parse_expression()

            if position >= len(tokens):
                raise ValueError("INVALID")

            if tokens[position][0] != ")":
                raise ValueError("INVALID")

            position += 1

            return value

        raise ValueError("INVALID")

    result = parse_expression()

    # Check whether the complete expression was processed
    if position != len(tokens):
        raise ValueError("INVALID")

    return result


def main():

    try:
        # Input number of variables
        v = int(input("Enter number of variables: "))

        if v < 1 or v > 200000:
            raise ValueError("INVALID")

        # Input variable definitions
        print("Enter variable definitions:")

        for _ in range(v):

            line = input()

            if "=" not in line:
                raise ValueError("INVALID")

            name, expression = line.split("=", 1)

            name = name.strip()
            expression = expression.strip()

            if name == "" or expression == "":
                raise ValueError("INVALID")

            variables[name] = expression

        # Input final expression
        final_expression = input("Enter expression to evaluate: ")

        # Evaluate expression
        answer = evaluate_expression(final_expression)

        print("Result:", answer)

    except ValueError as error:

        if str(error) == "CYCLE":
            print("Result: CYCLE")
        else:
            print("Result: INVALID")


if __name__ == "__main__":
    main()
