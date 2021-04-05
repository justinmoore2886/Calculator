from stack import Stack
import string

# Return a higher number for operator/operand with higher precedence
def precedence(op):
    if op in '*/':
        return 3
    elif op in '+-':
        return 1
    else:
        return 0

# Take a mathematical expression and turn it into tokens for each part
def tokenize(line, specials, whitespace):
    tokens = []
    current_token = ''
    non_operands = specials + whitespace
    for i in xrange(len(line)):
        c = line[i]
        if c in non_operands:
            if current_token != '':
                tokens.append(current_token)
                current_token = ''
            if c in specials:
                tokens.append(c)
        else:
            current_token += c
    if current_token != '':
        tokens.append(current_token)
    return tokens

# Check if token is an operator
def is_operator(token):
    if type(token) == str:
        return token in '+-*/=()'
    else:
        return False

# Check if the token is a variable (ie. contains all valid var characters)
def is_variable_name(token):
    if type(token) == float:
        return False

    if token[0] not in (string.ascii_letters + '_'):
        return False
    else:
        for c in token[1:]:
            if c not in (string.ascii_letters + '_' + string.digits):
                return False
        return True

# Get a value from our table of stored tokens
def get_value(token, symbol_table):
    if type(token) == float:
        return token
    
    elif is_variable_name(token):
        try:
            return symbol_table[token]
        except KeyError:
            raise KeyError('Variable ' + token + ' is undefined')


def lexer(tokens):
    result = []
    for token in tokens:
        if is_operator(token):
            result.append(('operator', token))
        else:
            try:
                value = float(token)
                result.append(('number', value))
            except ValueError:
                if is_variable_name(token):
                    result.append(('variable', token))
                else:
                    result.append(('unknown', token))
    return result

# Converts infix to postfix
def to_postfix(infix_lexemes):
    pending_operators = Stack()
    postfix_expression = []
    for pair in infix_lexemes:
        (lex_type, token) = pair

        if lex_type == 'operator':
            if token == '(':
                pending_operators.push(pair)

            elif token == ')':
                while not pending_operators.empty() and\
                      pending_operators.top()[1] != '(':
                    postfix_expression.append(pending_operators.pop())

                if pending_operators.empty():
                    raise SyntaxError("Too many close parentheses")
            
                pending_operators.pop()

            else:
                while not pending_operators.empty() and precedence(pending_operators.top()[1]) >= precedence(token):
                    postfix_expression.append(pending_operators.pop())
                pending_operators.push(pair)

        elif lex_type == 'number':
            postfix_expression.append(pair)

        elif lex_type == 'variable':
            postfix_expression.append(pair)

        else:
            raise SyntaxError('Bad token: "' + token + '"')
            
    while not pending_operators.empty():
        if pending_operators.top() == '(':
            raise SyntaxError("Too many open parentheses")
        postfix_expression.append(pending_operators.pop())
        
    return postfix_expression

# Evaulate the postfix expression and return number
def eval_postfix(postfix_expression, symbol_table):
    s = Stack()
    for pair in postfix_expression:
        (lex_type, token) = pair
        if lex_type == 'operator':
            try:
                right = s.pop()
                left = s.pop()
            except IndexError:
                raise SyntaxError('Too many operators')
            if token != '=':
                left = get_value(left, symbol_table)
            right = get_value(right, symbol_table)
            if token == '+':
                value = left + right
            elif token == '-':
                value = left - right
            elif token == '*':
                value = left * right
            elif token == '/':
                if right == 0:
                    raise ValueError('Division by zero')
                value = left / right
            elif token == '=':
                symbol_table[left] = right
                value = right
            else:
                raise ValueError('Bad operator: "' + token + '"')
            s.push(value)
        elif lex_type == 'variable':
            s.push(token)
        elif lex_type == 'number':
            value = float(token)
            s.push(value)
        else:
            raise SyntaxError('bad token: "' + token + '"')
    if len(s) > 1:
        raise SyntaxError('Too few operators')
    elif len(s) == 1:
        return get_value(s.pop(), symbol_table)
    else:
        return None

# For testing if the parser works
def main():
    symbol_table = dict()
    while True:
        try:
            line = raw_input('>> ')
        except EOFError:
            print
            break
        
        try:
            tokens = tokenize(line, '+-*/()=', ' ')
            lexemes = lexer(tokens)
            postfix_lexemes = to_postfix(lexemes)
            value = eval_postfix(postfix_lexemes, symbol_table)
            if value is not None:
                print value
        except SyntaxError as e:
            print e
        except KeyError as e:
            print e
        except ValueError as e:
            print e


if __name__ == '__main__':
    main()
