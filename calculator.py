"""Simple calculator utilities and CLI."""

from __future__ import annotations

import argparse
import ast
import operator
from typing import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


_BIN_OPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


_UNARY_OPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}


def evaluate(expression: str) -> float:
    """Safely evaluate a basic arithmetic expression.

    Supports +, -, *, / and parentheses.
    """

    node = ast.parse(expression, mode="eval")
    return _eval_node(node.body)


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Unsupported expression")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate simple arithmetic expressions")
    parser.add_argument("expression", help='Expression to evaluate, e.g. "(2 + 3) * 4"')
    args = parser.parse_args()

    try:
        result = evaluate(args.expression)
    except (ValueError, SyntaxError, ZeroDivisionError) as exc:
        print(f"Error: {exc}")
        return 1

    if result.is_integer():
        print(int(result))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
