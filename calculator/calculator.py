import sys

def calculate(expression):
    try:
        tokens = expression.split()
        if len(tokens) < 3:
            return str(eval(expression))

        # Multiplication and division
        i = 1
        while i < len(tokens) - 1:
            if tokens[i] == '*':
                tokens[i - 1] = str(float(tokens[i - 1]) * float(tokens[i + 1]))
                del tokens[i:i + 2]
                i = 1
            elif tokens[i] == '/':
                tokens[i - 1] = str(float(tokens[i - 1]) / float(tokens[i + 1]))
                del tokens[i:i + 2]
                i = 1
            else:
                i += 2

        # Addition and subtraction
        i = 1
        while i < len(tokens) - 1:
            if tokens[i] == '+':
                tokens[i - 1] = str(float(tokens[i - 1]) + float(tokens[i + 1]))
                del tokens[i:i + 2]
                i = 1
            elif tokens[i] == '-':
                tokens[i - 1] = str(float(tokens[i - 1]) - float(tokens[i + 1]))
                del tokens[i:i + 2]
                i = 1
            else:
                i += 2

        return tokens[0]
    except Exception as e:
        return f"Error: {e}"

if len(sys.argv) > 1:
    expression = ' '.join(sys.argv[1:])
    result = calculate(expression)
    print(result)
else:
    print("Error: No expression provided.")