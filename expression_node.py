class ExpressionNode(object):
    def __init__(self, d=None, left=None, right=None):
        self.data = d
        self.left = left
        self.right = right

    def get_value(self, symbol_table):
        return self.data

    def add(self, value):
        if self.data is None:
            self.data = ExpressionNode(value, None, None)

        else:
            current_node = self.data

            while True:
                # Pre-existing node with that value
                if current_node.data == value:
                    return False

                # The value is less than the currents node data, go left
                elif value < current_node.data:
                    if current_node.left is None:
                        current_node.left = ExpressionNode(value)
                        return True
                    else:
                        current_node = current_node.left

                # The value is more than the currents node data, go right
                else:  # value > current_node.data
                    if current_node.right is None:
                        current_node.right = ExpressionNode(value)
                        return True
                    else:
                        current_node = current_node.right

    ''' Checks to see if the nodes left and right pointer are none'''
    def is_leaf(self):
        return self.left is None and self.right is None
    
    # + / - * =
    class OperatorNode:
        def __init__(self, d, l, r):
            self.data = d
            self.left = l
            self.right = r

        def __str__(self):
            return str(self.data)

        def get_value(self, symbol_table):
            if self.data == "=":
                right = self.right.get_value(symbol_table)
                left_name = self.left
                symbol_table[left_name] = right
                return right

            elif self.data == '+':
                l_value = self.left.get_value(symbol_table)
                r_value = self.right.get_value(symbol_table)
                return l_value + r_value

            elif self.data == '-':
                l_value = self.left.get_value(symbol_table)
                r_value = self.right.get_value(symbol_table)
                return l_value - r_value

            elif self.data == '*':
                l_value = self.left.get_value(symbol_table)
                r_value = self.right.get_value(symbol_table)
                return l_value * r_value

            elif self.data == '/':
                l_value = self.left.get_value(symbol_table)
                r_value = self.right.get_value(symbol_table)
                return l_value / r_value

        def is_leaf(self):
            return self.left is None and self.right is None
    
    class OperandNode:
        def __init__(self, d, left=None, right=None):
            self.data = d
            self.left = left
            self.right = right

        def is_leaf(self):
            return self.left is None and self.right is None
        
        class VariableNode:
            def __init__(self, d, left=None, right=None):
                self.data = d
                self.left = left
                self.right = right

            def __str__(self):
                return str(self.data)

            def is_leaf(self):
                return self.left is None and self.right is None

            def get_value(self, symbol_table):
                return symbol_table[self.data]

        class NumberNode:
            def __init__(self, d, left=None, right=None):
                self.data = d
                self.left = left
                self.right = right

            def __str__(self):
                return str(self.data)

            def is_leaf(self):
                return self.left is None and self.right is None

            def get_value(self, symbol_table):
                return self.data
