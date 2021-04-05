from stack import Stack
from parser import lexer, tokenize, to_postfix, eval_postfix
from expression_node import *

# Turn postfix into a tree
def to_tree(postfix_expression):

    the_stack = Stack()

    for token in postfix_expression:

        if token[0] == 'operator':
            operator = token[1]
            right = the_stack.pop()
            left = the_stack.pop()
            node = ExpressionNode.OperatorNode(operator, left, right)
            the_stack.push(node)

        elif token[0] == 'variable':
            variable = token[1]
            node = ExpressionNode.OperandNode.VariableNode(variable)
            the_stack.push(node)

        elif token[0] == 'number':
            number = float(token[1])
            node = ExpressionNode.OperandNode.NumberNode(number)
            the_stack.push(node)

        else:
            return "You entered in an invalid character/word/number"

    return the_stack.top()

# Evaluate the tree
def eval_tree(node, symbol_table):
    if node is None:
        return 0

    elif node.left is None and node.right is None:
        return node.data

    else:
        left = node.left.get_value(symbol_table)
        right = node.right.get_value(symbol_table)

        if node.data == '+':
            return left + right
        elif node.data == '-':
            return left - right
        elif node.data == '*':
            return left * right
        elif node.data == '/':
            return left / right
        elif node.data == "=":
            return right

# Print the tree
def print_tree(node, depth=0):
    if node is not None:
        print_tree(node.right, depth + 1)
        print " " * (depth * 4), node.data
        print_tree(node.left, depth + 1)

# Run the calculator
def main():
    symbol_table = dict()
    while True:
        try:
            # print "Symbol-table is:", symbol_table
            line = raw_input('>> ')
        except EOFError:
            print
            break
        
        try:
            tokens = tokenize(line, '+-*/()=', ' ')
            lexemes = lexer(tokens)
            postfix = to_postfix(lexemes)

            root = to_tree(postfix)
            print "Tree:"
            print_tree(root)

            evaluated_postfix = eval_postfix(postfix, symbol_table)

            value = root.get_value(symbol_table)

            if value is not None:
                print "\nAnswer:", value
            
        except SyntaxError as e:
            print e
        except KeyError as e:
            print e
        except ValueError as e:
            print e


if __name__ == '__main__':
    main()
