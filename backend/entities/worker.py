import re
from typing import TypedDict
from uuid import UUID

from .common import ParameterType

class WorkerParameterDescription(TypedDict):
    type: ParameterType
    name: str

class Worker(TypedDict):
    id: UUID
    parameters_declaration: list[WorkerParameterDescription]
    parameters_expession: str

_EXPR_DEFINED_OPERATION_MAP = {
    ParameterType.NUM: ["EXIST", "COMPARE_LITERAL", "COMPARE"],
    ParameterType.BOOL: ["EXIST", "COMPARE_LITERAL", "COMPARE"]
}

class ParameterExpressionResolver:
    def __init__(self, parameters: list[WorkerParameterDescription]):
        self._namespace: dict[str, ParameterType] = {
            param['name']: param['type'] for param in parameters
        }
    
    def resolve(self, expr: str, parameter_values: dict[str, any]) -> bool:
        expr = re.sub(r'\s+', ' ', expr.strip())
        
        def tokenize_expression(expression: str) -> list[str]:
            """Improved tokenizer that handles expressions correctly"""
            tokens = []
            i = 0
            n = len(expression)
            
            while i < n:
                char = expression[i]
                
                # Skip whitespace
                if char.isspace():
                    i += 1
                    continue
                
                # Handle operators and parentheses
                if char in '()':
                    tokens.append(char)
                    i += 1
                    continue
                
                # Handle multi-character operators (<=, >=, ==, !=, AND, OR, NOT)
                if i + 1 < n:
                    two_char = expression[i:i+2].upper()
                    if two_char in ('<=', '>=', '==', '!='):
                        tokens.append(two_char)
                        i += 2
                        continue
                
                if i + 2 < n and expression[i:i+3].upper() == 'AND':
                    tokens.append('AND')
                    i += 3
                    continue
                    
                if i + 1 < n and expression[i:i+2].upper() == 'OR':
                    tokens.append('OR')
                    i += 2
                    continue
                    
                if i + 2 < n and expression[i:i+3].upper() == 'NOT':
                    tokens.append('NOT')
                    i += 3
                    continue
                
                # Handle single-character operators
                if char in '<>=!':
                    tokens.append(char)
                    i += 1
                    continue
                
                # Handle identifiers (parameters and literals)
                if char.isalnum() or char == '_' or char == '.' or char == '-':
                    j = i
                    while j < n and (expression[j].isalnum() or expression[j] == '_' or 
                                   expression[j] == '.' or expression[j] == '-'):
                        j += 1
                    token = expression[i:j]
                    tokens.append(token)
                    i = j
                    continue
                
                # If we get here, it's an unexpected character
                raise ValueError(f"Unexpected character '{char}' at position {i}")
            
            return tokens
        
        def evaluate_expression(tokens: list) -> tuple[bool, int]:
            """Evaluate expression with proper operator precedence"""
            return evaluate_or_expression(tokens)
        
        def evaluate_or_expression(tokens: list) -> tuple[bool, int]:
            """Evaluate OR expressions (lowest precedence)"""
            left, consumed = evaluate_and_expression(tokens)
            pos = consumed
            
            while pos < len(tokens) and tokens[pos] == 'OR':
                right, right_consumed = evaluate_and_expression(tokens[pos + 1:])
                left = left or right
                pos += right_consumed + 1
            
            return left, pos
        
        def evaluate_and_expression(tokens: list) -> tuple[bool, int]:
            """Evaluate AND expressions"""
            left, consumed = evaluate_not_expression(tokens)
            pos = consumed
            
            while pos < len(tokens) and tokens[pos] == 'AND':
                right, right_consumed = evaluate_not_expression(tokens[pos + 1:])
                left = left and right
                pos += right_consumed + 1
            
            return left, pos
        
        def evaluate_not_expression(tokens: list) -> tuple[bool, int]:
            """Evaluate NOT expressions"""
            if not tokens:
                raise ValueError("Unexpected end of expression")
            
            if tokens[0] == 'NOT':
                result, consumed = evaluate_primary(tokens[1:])
                return not result, consumed + 1
            else:
                return evaluate_primary(tokens)
        
        def evaluate_primary(tokens: list) -> tuple[bool, int]:
            """Evaluate primary expressions (parentheses, comparisons, exists)"""
            if not tokens:
                raise ValueError("Unexpected end of expression")
            
            # Handle parentheses
            if tokens[0] == '(':
                result, consumed = evaluate_expression(tokens[1:])
                if consumed >= len(tokens) or tokens[consumed] != ')':
                    raise ValueError("Missing closing parenthesis")
                return result, consumed + 1
            
            # Handle comparisons
            if len(tokens) >= 3 and tokens[1] in ('<', '>', '<=', '>=', '=', '==', '!='):
                left_param = self._normalize_parameter_name(tokens[0])
                operator = tokens[1]
                right_param = tokens[2]
                
                result = self._evaluate_comparison(left_param, operator, right_param, parameter_values)
                return result, 3
            
            # Handle single parameter - check existence or boolean value
            param_name = self._normalize_parameter_name(tokens[0])
            
            # For boolean parameters, return their actual value
            if param_name in self._namespace and self._namespace[param_name] == ParameterType.BOOL:
                if param_name not in parameter_values or parameter_values[param_name] is None:
                    return False, 1
                value = parameter_values[param_name]
                # Convert to proper boolean
                if isinstance(value, str):
                    bool_value = value.upper() in ('TRUE', '1')
                else:
                    bool_value = bool(value)
                return bool_value, 1
            else:
                # For non-boolean parameters, check existence
                result = self._evaluate_exist(param_name, parameter_values)
                return result, 1
        
        tokens = tokenize_expression(expr)
        result, consumed = evaluate_expression(tokens)
        
        if consumed != len(tokens):
            raise ValueError(f"Unexpected tokens at end of expression: {tokens[consumed:]}")
        
        return result
    
    def _normalize_parameter_name(self, token: str) -> str:
        """Extract parameter name from token and return the original case from namespace"""
        # Check if parameter exists in any case
        for known_param in self._namespace.keys():
            if known_param.upper() == token.upper():
                return known_param  # Return the original case from namespace
        
        # If not found, return as is (might be a literal)
        return token
    
    def _evaluate_exist(self, param_name: str, parameter_values: dict[str, any]) -> bool:
        """Evaluate EXIST operation for a parameter"""
        if param_name not in self._namespace:
            raise ValueError(f"Unknown parameter: {param_name}")
        
        param_type = self._namespace[param_name]
        if param_type not in _EXPR_DEFINED_OPERATION_MAP:
            raise ValueError(f"Operations not defined for parameter type: {param_type}")
        
        if "EXIST" not in _EXPR_DEFINED_OPERATION_MAP[param_type]:
            raise ValueError(f"EXIST operation not allowed for parameter type: {param_type}")
        
        return param_name in parameter_values and parameter_values[param_name] is not None
    
    def _evaluate_comparison(self, left_param: str, operator: str, right_param: str, 
                           parameter_values: dict[str, any]) -> bool:
        """Evaluate comparison between two parameters or parameter and literal"""
        # Check if left parameter exists in namespace
        if left_param not in self._namespace:
            raise ValueError(f"Unknown parameter: {left_param}")
        
        left_type = self._namespace[left_param]
        
        # Determine if right operand is a parameter or literal
        right_is_param = False
        normalized_right = self._normalize_parameter_name(right_param)
        if normalized_right in self._namespace:
            right_type = self._namespace[normalized_right]
            right_value = parameter_values.get(normalized_right)
            operation_type = "COMPARE"
            right_is_param = True
        else:
            # It's a literal - parse it based on left parameter type
            right_type = left_type
            right_value = self._parse_literal(right_param, left_type)
            operation_type = "COMPARE_LITERAL"
        
        # Check if operation is allowed
        if left_type not in _EXPR_DEFINED_OPERATION_MAP:
            raise ValueError(f"Operations not defined for parameter type: {left_type}")
        
        allowed_ops = _EXPR_DEFINED_OPERATION_MAP[left_type]
        if operation_type not in allowed_ops:
            raise ValueError(f"{operation_type} operation not allowed for parameter type: {left_type}")
        
        # Get left value
        left_value = parameter_values.get(left_param)
        if left_value is None:
            return False
        
        # For parameter comparisons, check type compatibility
        if right_is_param and left_type != right_type:
            raise ValueError(f"Type mismatch in comparison: {left_type} vs {right_type}")
        
        # Perform comparison based on type
        if left_type == ParameterType.NUM:
            return self._compare_numeric(left_value, operator, right_value)
        elif left_type == ParameterType.BOOL:
            return self._compare_bool(left_value, operator, right_value)
        else:
            raise ValueError(f"Unsupported parameter type for comparison: {left_type}")
    
    def _parse_literal(self, literal: str, target_type: ParameterType) -> any:
        """Parse literal string to appropriate type based on target type"""
        if target_type == ParameterType.NUM:
            try:
                if '.' in literal:
                    return float(literal)
                else:
                    return int(literal)
            except (ValueError, TypeError):
                raise ValueError(f"Cannot parse '{literal}' as number")
        elif target_type == ParameterType.BOOL:
            literal_upper = literal.upper()
            if literal_upper in ('TRUE', '1'):
                return True
            elif literal_upper in ('FALSE', '0'):
                return False
            else:
                raise ValueError(f"Cannot parse '{literal}' as boolean")
        else:
            raise ValueError(f"Unsupported parameter type: {target_type}")
    
    def _compare_numeric(self, left: any, operator: str, right: any) -> bool:
        """Compare numeric values"""
        try:
            left_val = float(left) if not isinstance(left, (int, float)) else left
            right_val = float(right) if not isinstance(right, (int, float)) else right
        except (ValueError, TypeError):
            return False
        
        if operator == '<':
            return left_val < right_val
        elif operator == '<=':
            return left_val <= right_val
        elif operator == '>':
            return left_val > right_val
        elif operator == '>=':
            return left_val >= right_val
        elif operator in ('=', '=='):
            return abs(left_val - right_val) < 1e-10
        elif operator == '!=':
            return abs(left_val - right_val) >= 1e-10
        
        raise ValueError(f"Unsupported operator for numeric comparison: {operator}")
    
    def _compare_bool(self, left: any, operator: str, right: any) -> bool:
        """Compare boolean values"""
        # Convert to proper boolean values
        if isinstance(left, str):
            left_bool = left.upper() in ('TRUE', '1')
        else:
            left_bool = bool(left)
            
        if isinstance(right, str):
            right_bool = right.upper() in ('TRUE', '1')
        else:
            right_bool = bool(right)
        
        if operator in ('=', '=='):
            return left_bool == right_bool
        elif operator == '!=':
            return left_bool != right_bool
        
        raise ValueError(f"Unsupported operator for boolean comparison: {operator}")


if __name__ == "__main__":
    parameters = [
        {"type": ParameterType.NUM, "name": "param1"},
        {"type": ParameterType.NUM, "name": "param2"},
        {"type": ParameterType.BOOL, "name": "param3"},
        {"type": ParameterType.BOOL, "name": "param4"}
    ]
    
    resolver = ParameterExpressionResolver(parameters)
    
    test_values = {
        "param1": 10,
        "param2": 20,
        "param3": False,
        "param4": True
    }
    
    expressions = [
        'param1 < param2',  # True
        'param1 > param2',  # False
        'param1 = param2',  # False
        'param4 AND param1 < param2',  # True
        'param3 AND param1 < param2', # False
        'NOT param4 OR param1 > param2',  # False
        '(param1 < param2) AND param4',  # True
        'NOT (param1 > param2) AND param4',  # True
        'param1 < param2 AND NOT param3',  # True
        'param3 = false',  # True - compare boolean with literal
        'param4 = true',   # True - compare boolean with literal
        'param3 != true',  # True
        '(param1 < param2) AND (NOT param3)',  # True - this was failing before
        'NOT param3',  # True
        'NOT param3 AND param3',  # True
    ]
    
    for expr in expressions:
        try:
            result = resolver.resolve(expr, test_values)
            print(f"Expression: {expr} -> {result}")
        except Exception as e:
            print(f"Expression: {expr} -> ERROR: {e}")