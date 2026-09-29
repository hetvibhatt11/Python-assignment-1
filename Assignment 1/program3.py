# Recursive Expression Engine with Memoization

memo = {}

def calculate(n):
    # Check if result is already stored
    if n in memo:
        return memo[n]

    # Base case
    if n <= 1:
        return n

    # Recursive calculation
    result = calculate(n - 1) + calculate(n - 2)

    # Store result in memo
    memo[n] = result

    return result


n = int(input("Enter a number: "))

result = calculate(n)

print("Result:", result)
print("Memoized values:", memo)