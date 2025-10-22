"""
Outputs a semicolon-delimited CSV with headers or a json file:
category of issue; priority of issue; impacted lines; potential impact; description
"""

from __future__ import annotations

import ast
import argparse
import csv
import os
import re
import sys
import json
from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterable, Dict, Set

# Issue model + severities

@dataclass
class Issue:
    category: str
    priority: str         # HIGH, MEDIUM, LOW
    impacted_lines: str   # "12", "10-22", "5,12,29"
    potential_impact: str
    description: str

class Rule(ast.NodeVisitor):
    """
    Base rule supports two styles:
      1) "return-a-list" rules override check(...) and call self.make(...)
      2) Visitor-style rules implement visit_* and call self.report(...)
         and rely on this default check(...) to traverse the AST.
    """
    name: str = "Unnamed Rule"
    category: str = "General"
    priority: str = "LOW"
    impact: str = "Informational"
    heuristic: bool = False

    _issues: List[Issue]
    filename: str

    def check(self, filename: str, tree: Optional[ast.AST], text: str) -> List[Issue]:
        """
        Default behavior for visitor-style rules: walk the AST and collect issues
        emitted via self.report(...). Rules that prefer the old style can still
        override this method and return a list explicitly.
        """
        if tree is None:
            return []
        self.filename = filename
        self._issues = []

        for n in ast.walk(tree):
            for ch in ast.iter_child_nodes(n):
                setattr(ch, "parent", n)

        self.visit(tree)
        return list(self._issues)

    def make(self, line: int | Tuple[int, int] | Iterable[int], message: str) -> Issue:
        if isinstance(line, tuple):
            impacted = f"{line[0]}-{line[1]}"
        elif isinstance(line, int):
            impacted = str(line)
        else:
            impacted = ",".join(str(x) for x in sorted(set(line)))
        return Issue(self.category, self.priority, impacted, self.impact, message)

    def report(self, category: Optional[str], priority: Optional[str], line: int,
               impact: Optional[str], message: str) -> None:
        """
        Helper for visitor-style rules to record a finding.
        Any None argument falls back to this rule's defaults.
        """
        cat = category or self.category
        pr  = priority or self.priority
        imp = impact or self.impact
        self._issues.append(Issue(cat, pr, str(line), imp, message))


def _iter_py_files(root: str):
    if os.path.isdir(root):
        for r, _, files in os.walk(root):
            for f in files:
                if f.endswith(".py"):
                    yield os.path.join(r, f)
    elif root.endswith(".py") and os.path.exists(root):
        yield root

def _safe_parse(code: str, filename: str) -> Optional[ast.AST]:
    try:
        return ast.parse(code, filename=filename)
    except SyntaxError:
        return None

_BUILTINS = set(dir(__import__("builtins")))


class BareOrBroadExcept(Rule):
    category = "Error Handling"; priority = "HIGH"
    impact = "Bugs hidden by catching everything; harder debugging."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(self.make(node.lineno, 'Catch-all "except:" used. Catch specific exceptions.'))
                elif isinstance(node.type, ast.Name) and node.type.id in {"Exception","BaseException"}:
                    issues.append(self.make(node.lineno, f'Overly broad exception handler ({node.type.id}).'))
                elif isinstance(node.type, ast.Tuple):
                    for elt in node.type.elts:
                        if isinstance(elt, ast.Name) and elt.id in {"Exception","BaseException"}:
                            issues.append(self.make(node.lineno, f'Overly broad exception handler ({elt.id}).'))
        return issues

class AssertForRuntime(Rule):
    category = "Correctness"; priority = "MEDIUM"
    impact = "Asserts can be stripped with -O; critical checks may disappear."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for n in ast.walk(tree):
            if isinstance(n, ast.Assert):
                issues.append(self.make(n.lineno, "Avoid assert for runtime validation; raise exceptions instead."))
        return issues

class MutableDefaultArgs(Rule):
    category = "Correctness"; priority = "HIGH"
    impact = "Shared mutable state across calls; surprising behavior."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        def _is_mutable_default(node: ast.AST) -> bool:
            if isinstance(node, (ast.List, ast.Dict, ast.Set)):
                return True
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"list","dict","set"}:
                return True
            return False
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in fn.args.defaults:
                    if _is_mutable_default(default):
                        issues.append(self.make(fn.lineno, f'Mutable default in function "{fn.name}".'))
                for d in getattr(fn.args, "kw_defaults", []) or []:
                    if d is not None and _is_mutable_default(d):
                        issues.append(self.make(fn.lineno, f'Mutable keyword-only default in function "{fn.name}".'))
        return issues

class OpenWithoutWith(Rule):
    category = "Resource Management"; priority = "MEDIUM"
    impact = "Resource leaks; file handles not closed on error."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        in_with: Set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.With):
                for item in node.items:
                    ce = item.context_expr
                    if isinstance(ce, ast.Call) and ((isinstance(ce.func, ast.Name) and ce.func.id=="open") or (isinstance(ce.func, ast.Attribute) and ce.func.attr=="open")):
                        in_with.add(id(ce))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                f = node.func
                is_open = (isinstance(f, ast.Name) and f.id=="open") or (isinstance(f, ast.Attribute) and f.attr=="open")
                if is_open and id(node) not in in_with:
                    issues.append(self.make(getattr(node,"lineno",1), "Use 'with open(...)' to ensure closure."))
        return issues

class FileModeMismatch(Rule):
    category = "Resource Management"; priority = "HIGH"
    impact = "Read/write mismatch likely bugs."
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        modes: Dict[str, Tuple[str,int]] = {}
        reads: Dict[str, List[int]] = {}
        writes: Dict[str, List[int]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Name) and call.func.id == "open":
                    mode = None
                    if len(call.args)>=2 and isinstance(call.args[1], ast.Constant) and isinstance(call.args[1].value,str):
                        mode = call.args[1].value
                    for kw in call.keywords or []:
                        if kw.arg=="mode" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value,str):
                            mode = kw.value.value
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            modes[t.id] = (mode or "r", node.lineno)
            if isinstance(node, ast.With):
                for item in node.items:
                    ctx = item.context_expr
                    if isinstance(ctx, ast.Call) and isinstance(ctx.func, ast.Name) and ctx.func.id=="open":
                        mode = None
                        if len(ctx.args)>=2 and isinstance(ctx.args[1], ast.Constant) and isinstance(ctx.args[1].value,str):
                            mode = ctx.args[1].value
                        for kw in ctx.keywords or []:
                            if kw.arg=="mode" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value,str):
                                mode = kw.value.value
                        if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                            modes[item.optional_vars.id] = (mode or "r", ctx.lineno)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                var = node.func.value.id
                if node.func.attr in {"read","readline","readlines"}: reads.setdefault(var,[]).append(node.lineno)
                if node.func.attr in {"write","writelines"}: writes.setdefault(var,[]).append(node.lineno)
        for var,(mode,open_line) in modes.items():
            if mode.startswith("r") and var in writes:
                issues.append(self.make(writes[var][0], f'File handle "{var}" opened read-mode "{mode}" but written to.'))
            if mode and mode[0] in {"w","a"} and var in reads:
                issues.append(self.make(reads[var][0], f'File handle "{var}" opened write/append "{mode}" but read from.'))
        return issues

class NonPythonicLoops(Rule):
    category = "Style/Idioms"; priority = "LOW"; impact = "Harder to read; potential for index errors."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                it = node.iter
                if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id=="range":
                    if len(it.args)==1 and isinstance(it.args[0], ast.Call):
                        inner = it.args[0]
                        if isinstance(inner.func, ast.Name) and inner.func.id=="len":
                            issues.append(self.make(node.lineno, "Use direct iteration or enumerate() instead of range(len(...))."))
                if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute) and it.func.attr=="keys":
                    issues.append(self.make(node.lineno, "Iterating dict.keys(); consider dict.items() if values are used."))
        return issues

class LenComparisons(Rule):
    category = "Style/Idioms"; priority = "LOW"; impact = "Prefer truthiness checks for readability."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare) and isinstance(node.left, ast.Call):
                call = node.left
                if isinstance(call.func, ast.Name) and call.func.id=="len" and len(call.args)==1:
                    if len(node.comparators)==1 and isinstance(node.comparators[0], ast.Constant):
                        val = node.comparators[0].value
                        op = node.ops[0].__class__.__name__
                        if val == 0 and op in {"Eq","NotEq","Gt","Lt","GtE","LtE"}:
                            issues.append(self.make(node.lineno, 'Use "if x:" or "if not x:" instead of len(...) comparisons.'))
        return issues

class IdentityVsEquality(Rule):
    category = "Correctness"; priority = "MEDIUM"; impact = "Wrong operator may yield incorrect logic."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                left = node.left
                for op, comp in zip(node.ops, node.comparators):
                    if isinstance(op, (ast.Is, ast.IsNot)):
                        if isinstance(comp, ast.Constant):
                            if comp.value in (True, False):
                                issues.append(self.make(node.lineno, 'Avoid using "is True/False" in comparisons.'))
                            elif comp.value is not None:
                                issues.append(self.make(node.lineno, 'Use "==" for value comparison; reserve "is" for None.'))
                        if isinstance(left, ast.Constant):
                            if left.value in (True, False):
                                issues.append(self.make(node.lineno, 'Avoid using "is True/False" in comparisons.'))
                            elif left.value is not None:
                                issues.append(self.make(node.lineno, 'Use "==" for value comparison; reserve "is" for None.'))
                    if isinstance(op, (ast.Eq, ast.NotEq)):
                        if isinstance(comp, ast.Constant) and comp.value is None:
                            issues.append(self.make(node.lineno, 'Use "is (not) None" for None checks.'))
                        if isinstance(comp, ast.Constant) and comp.value in (True, False):
                            issues.append(self.make(node.lineno, 'Avoid == True/False; use the value directly.'))
                        if isinstance(left, ast.Constant) and left.value is None:
                            issues.append(self.make(node.lineno, 'Use "is (not) None" for None checks.'))
        return issues

class TypeCheckRule(Rule):
    category = "Correctness"; priority = "MEDIUM"; impact = "type(x)==T is brittle; prefer isinstance()."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id == "type":
                    if any(isinstance(op, (ast.Eq, ast.NotEq, ast.Is, ast.IsNot)) for op in node.ops):
                        issues.append(self.make(node.lineno, "Use isinstance(x, T) instead of type(x) == T."))
        return issues

class UnsafeCSVParsing(Rule):
    category = "Robustness"; priority = "MEDIUM"; impact = "Delimiter-in-data breaks parsing; use csv module."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "split":
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    delim = node.args[0].value  # exact comparison; no strip
                    if delim in {",",";","\t"}:
                        issues.append(self.make(node.lineno, f"Possible CSV parsing via split('{delim}'); prefer csv module."))
        return issues

class EvalExecUse(Rule):
    category = "Security"; priority = "HIGH"; impact = "Arbitrary code execution risk."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval","exec"}:
                issues.append(self.make(node.lineno, f'Use of {node.func.id}(). Avoid on untrusted input.'))
        return issues

class DangerousFunctions(Rule):
    category = "Security"; priority = "HIGH"; impact = "Unsafe deserialization or command injection risk."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                val = node.func.value
                attr = node.func.attr
                if isinstance(val, ast.Name) and val.id == "yaml" and attr == "load":
                    has_loader = any((kw.arg or "").lower()=="loader" for kw in (node.keywords or []))
                    if not has_loader:
                        issues.append(self.make(node.lineno, "yaml.load() without Loader; use yaml.safe_load or specify a safe Loader."))
                if isinstance(val, ast.Name) and val.id == "pickle" and attr in {"load","loads"}:
                    issues.append(self.make(node.lineno, "pickle.load(s) on untrusted data is unsafe."))
                full = f"{getattr(val,'id',None)}.{attr}" if isinstance(val, ast.Name) else ""
                if full == "os.system":
                    issues.append(self.make(node.lineno, "os.system used; prefer subprocess without shell=True."))
                if full.startswith("subprocess."):
                    shell_kw = next((kw for kw in (node.keywords or []) if kw.arg=="shell"), None)
                    if shell_kw and isinstance(shell_kw.value, ast.Constant) and shell_kw.value.value is True:
                        issues.append(self.make(node.lineno, "subprocess with shell=True; risk of injection."))
        return issues

class ExitCallsInLibrary(Rule):
    category = "Correctness"; priority = "HIGH"; impact = "Premature interpreter exit; unusable as import."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        main_blocks: List[Tuple[int,int]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                test = node.test
                if (isinstance(test, ast.Compare) and isinstance(test.left, ast.Name) and test.left.id=="__name__"
                    and test.ops and isinstance(test.ops[0], ast.Eq) and test.comparators and isinstance(test.comparators[0], ast.Constant)
                    and test.comparators[0].value == "__main__"):
                    start = getattr(node,"lineno",1)
                    end = max([getattr(n,"lineno",start) for n in ast.walk(node)] or [start])
                    main_blocks.append((start,end))
        def in_main(ln:int)->bool: return any(a<=ln<=b for a,b in main_blocks)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"exit","quit"} and not in_main(getattr(node,"lineno",1)):
                    issues.append(self.make(node.lineno, "exit()/quit() in non-__main__ context; raise exception instead."))
                if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id=="sys" and node.func.attr=="exit" and not in_main(getattr(node,"lineno",1)):
                    issues.append(self.make(node.lineno, "sys.exit() in non-__main__ context; raise exception instead."))
        return issues

class UnusedImports(Rule):
    category = "Code Cleanliness"; priority = "LOW"; impact = "Dead code; slower imports; namespace clutter."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        imported: Dict[str,int] = {}
        used: Set[str] = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    name = alias.asname or alias.name.split(".")[0]
                    imported[name] = n.lineno
            if isinstance(n, ast.ImportFrom):
                if n.module == "__future__": continue
                for alias in n.names:
                    if alias.name == "*": continue
                    name = alias.asname or alias.name
                    imported[name] = n.lineno
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                used.add(n.id)
        for name, line in imported.items():
            if name not in used:
                issues.append(self.make(line, f'Imported "{name}" not used.'))
        return issues

class UnusedVariables(Rule):
    category = "Code Cleanliness"; priority = "LOW"; impact = "Possible mistakes; maintainability issues."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        assigned: Dict[str, List[int]] = {}
        used: Set[str] = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                assigned.setdefault(n.id, []).append(n.lineno)
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                used.add(n.id)
        for name, lines in assigned.items():
            if name == "_" or name.startswith("_"): continue
            if name not in used:
                issues.append(self.make(lines[0], f'Variable "{name}" assigned but not used.'))
        return issues

class WildcardImports(Rule):
    category = "Style/Maintainability"; priority = "LOW"; impact = "Polluted namespace; unclear origins."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom):
                for a in n.names:
                    if a.name == "*":
                        issues.append(self.make(n.lineno, f'Wildcard import from "{n.module}". Prefer explicit imports.'))
                        break
        return issues

class ShadowBuiltins(Rule):
    category = "Style"; priority = "LOW"; impact = "Confusion; possible bugs by clobbering built-ins."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef):
                for arg in n.args.args:
                    if arg.arg in _BUILTINS:
                        issues.append(self.make(n.lineno, f'Parameter "{arg.arg}" shadows built-in.'))
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id in _BUILTINS:
                        issues.append(self.make(n.lineno, f'Variable "{t.id}" shadows built-in.'))
        return issues

class DangerousTokenMagicNumbers(Rule):
    category = "Correctness"; priority = "MEDIUM"; impact = "Brittle parsing; unclear meaning."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        pattern = re.compile(r"\.type\s*==\s*\d+")
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                issues.append(self.make(i, "Comparing token .type to numeric literal; prefer named constants from token module."))
        return issues

class PrintStatements(Rule):
    category = "Code Cleanliness"; priority = "LOW"; impact = "Prefer logging or returning values."
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
                issues.append(self.make(n.lineno, "print() used; consider logging or returning values instead."))
        return issues

class FStringMissing(Rule):
    category = "Style"; priority = "LOW"; impact = "String likely intended as f-string; confusing output."
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        safe_const = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "format":
                if isinstance(n.func.value, ast.Constant) and isinstance(n.func.value.value, str):
                    safe_const.add(n.func.value)
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                s = n.value
                if "{" in s and "}" in s and "{{" not in s and "}}" not in s:
                    if n not in safe_const:
                        inside = s[s.find("{")+1:s.find("}")]
                        if any(ch.isalpha() for ch in inside):
                            issues.append(self.make(getattr(n,"lineno",1), "String contains { } but is not an f-string (missing f-prefix or .format)."))
        return issues

class NamingConventions(Rule):
    category = "Style"; priority = "LOW"; impact = "Non-PEP8 naming hurts readability."
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        snake = re.compile(r'^[a-z_][a-z0-9_]*$')
        camel = re.compile(r'^[A-Z][A-Za-z0-9]+$')
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not (n.name.startswith("__") and n.name.endswith("__")) and not snake.match(n.name):
                    issues.append(self.make(n.lineno, f'Function name "{n.name}" is not snake_case.'))
            if isinstance(n, ast.ClassDef):
                if not camel.match(n.name):
                    issues.append(self.make(n.lineno, f'Class name "{n.name}" is not CamelCase.'))
            if isinstance(n, ast.arg):
                if n.arg not in {"self","cls"} and not snake.match(n.arg):
                    issues.append(self.make(n.lineno, f'Parameter name "{n.arg}" is not snake_case.'))
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                name = n.id
                if name in _BUILTINS:
                    issues.append(self.make(n.lineno, f'Variable "{name}" shadows built-in.'))
                if any(c.isupper() for c in name) and not name.isupper():
                    issues.append(self.make(n.lineno, f'Variable "{name}" is not snake_case.'))
        return issues

class UndefinedNameRule(Rule):
    """
    Detect names used before definition/import, without double-reporting.

    Fixes:
    - SHALLOW module-scope pass (does not descend into def/class bodies)
    - Per-function pass inherits module-defined names + function args
    - Tracks names introduced via assignments, for/with targets, comprehensions, and imports
    """
    category = "Correctness"
    priority = "HIGH"
    impact = "Name used before definition/import."
    heuristic = True


    def _names_from_target(self, t: ast.AST) -> list[str]:
        if isinstance(t, ast.Name):
            return [t.id]
        if isinstance(t, (ast.Tuple, ast.List)):
            names: list[str] = []
            for el in t.elts:
                names += self._names_from_target(el)
            return names
        return []

    def _collect_defined_in_scope(self, body: list[ast.stmt]) -> set[str]:
        """
        Collect names considered 'defined' within the given body:
          - function/class names
          - function arguments
          - assignment targets
          - for/with targets
          - comprehension targets
          - imports and from-imports
        """
        defined = set(_BUILTINS) | {"__name__", "__file__"}

        # Walk ONLY the provided body (wrapped in a fake Module) to avoid bleeding across scopes
        wrapper = ast.Module(body=body, type_ignores=[])
        for n in ast.walk(wrapper):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defined.add(n.name)

            if isinstance(n, ast.arguments):
                for a in list(n.args) + list(n.kwonlyargs):
                    defined.add(a.arg)
                if n.vararg:
                    defined.add(n.vararg.arg)
                if n.kwarg:
                    defined.add(n.kwarg.arg)

            if isinstance(n, ast.Assign):
                for t in n.targets:
                    for name in self._names_from_target(t):
                        defined.add(name)

            if isinstance(n, (ast.For, ast.AsyncFor)):
                for name in self._names_from_target(n.target):
                    defined.add(name)

            if isinstance(n, ast.With):
                for item in n.items:
                    if item.optional_vars:
                        for name in self._names_from_target(item.optional_vars):
                            defined.add(name)

            if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
                for gen in n.generators:
                    for name in self._names_from_target(gen.target):
                        defined.add(name)

            if isinstance(n, ast.Import):
                for a in n.names:
                    defined.add(a.asname or a.name.split(".")[0])

            if isinstance(n, ast.ImportFrom):
                for a in n.names:
                    if a.name != "*":
                        defined.add(a.asname or a.name)

        return defined


    def check(self, filename: str, tree: Optional[ast.AST], text: str) -> List[Issue]:
        issues: List[Issue] = []
        if not tree:
            return issues

        module_body: list[ast.stmt] = getattr(tree, "body", [])
        module_defined = self._collect_defined_in_scope(module_body)

        #    Iterate top-level statements only; skip def/class nodes entirely to avoid duplicates.
        for top in module_body:
            if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            for n in ast.walk(top):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    if n.id not in module_defined:
                        issues.append(self.make(n.lineno, f'Name "{n.id}" might be undefined in this scope.'))

        for fn in (x for x in ast.walk(tree) if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))):
            fn_defined = self._collect_defined_in_scope(fn.body)

            fn_args = set()
            if fn.args:
                for a in list(fn.args.args) + list(fn.args.kwonlyargs):
                    fn_args.add(a.arg)
                if fn.args.vararg:
                    fn_args.add(fn.args.vararg.arg)
                if fn.args.kwarg:
                    fn_args.add(fn.args.kwarg.arg)

            visible = module_defined | fn_args | fn_defined

            wrapper = ast.Module(body=fn.body, type_ignores=[])
            for n in ast.walk(wrapper):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    if n.id not in visible:
                        issues.append(self.make(n.lineno, f'Name "{n.id}" might be undefined in this scope.'))

        return issues


class DictAccessGuard(Rule):
    category = "Robustness"; priority = "MEDIUM"; impact = "Possible KeyError on missing keys."; heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for n in ast.walk(tree):
            if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name):
                issues.append(self.make(getattr(n,"lineno",1), f'Key access on "{n.value.id}" without guard; prefer .get() or "in" checks or try/except.'))
        return issues

class ReturnAnnotationMismatch(Rule):
    category = "Correctness"; priority = "MEDIUM"; impact = "Return type may not match annotation."; heuristic = True

    def _ann_allows_none(self, ann: str) -> bool:
        s = ann.replace(" ", "")
        return ("None" in s) or ("Optional[" in s) or ("Union[" in s and "None" in s)

    def _is_explicit_none(self, value: ast.AST) -> bool:
        # Py3.8+: ast.Constant(value=None)
        if isinstance(value, ast.Constant) and value.value is None:
            return True
        if hasattr(ast, "NameConstant") and isinstance(value, ast.NameConstant) and value.value is None:  # type: ignore
            return True
        return False

    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and fn.returns:
                ann = ast.unparse(fn.returns) if hasattr(ast, "unparse") else None
                returns_none = False
                returns_value = False
                for sub in ast.walk(fn):
                    if isinstance(sub, ast.Return):
                        if sub.value is None or self._is_explicit_none(sub.value):
                            returns_none = True
                        else:
                            returns_value = True
                if ann:
                    if returns_none and not self._ann_allows_none(ann):
                        issues.append(self.make(fn.lineno, f'Function "{fn.name}" returns None but annotation is {ann}.'))
                    if returns_value and ann.strip() in {"None", "NoneType"}:
                        issues.append(self.make(fn.lineno, f'Function "{fn.name}" returns a value but annotation is {ann}.'))
        return issues


class TodoComments(Rule):
    category = 'Process'; priority = 'LOW'
    impact = 'Outstanding work items; ensure tracking.'
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        for i, line in enumerate(text.splitlines(), start=1):
            up = line.upper()
            if "TODO" in up or "FIXME" in up:
                issues.append(self.make(i, "Found TODO/FIXME. Confirm ticket/issue reference or resolve."))
        return issues

class PlatformSpecificPaths(Rule):
    category = 'Portability'; priority = 'MEDIUM'
    impact = 'Path separators or drive letters may break on other OS.'
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        for i, line in enumerate(text.splitlines(), start=1):
            if re.search(r"[A-Za-z]:\\\\", line) or ("\\" in line and "/" in line) or re.search(r"\\{2,}", line):
                issues.append(self.make(i, "Hardcoded path detected. Prefer pathlib.Path or os.path.join for portability."))
        return issues

class PotentialStringCastNeeded(Rule):
    name = 'Potential String Cast Needed'
    category = 'Correctness'
    priority = 'MEDIUM'
    impact = 'TypeError/logic bug if value not str.'
    heuristic = True
    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare) and isinstance(node.left, ast.Call):
                call = node.left
                if isinstance(call.func, ast.Name) and call.func.id == "len" and call.args:
                    arg = call.args[0]
                    argname = None
                    if isinstance(arg, ast.Name):
                        argname = arg.id
                    elif isinstance(arg, ast.Attribute):
                        argname = arg.attr
                    const_cmp = any(isinstance(c, ast.Constant) and isinstance(c.value, int) and 2 <= c.value <= 64
                                    for c in node.comparators)
                    if argname and const_cmp:
                        issues.append(self.make(node.lineno, f'len({argname}) compared to constant. Ensure "{argname}" is str (cast with str() upstream if needed).'))
        return issues


class ConcurrencyRule(Rule):
    """
    Heuristics for common threading / multiprocessing pitfalls:
    - threading.Thread started but never joined in the same scope
    - multiprocessing.Process/Pool used at module import time without a main guard
    - multiprocessing.Process started but never joined in the same scope
    """
    category = "Concurrency"
    priority = "MEDIUM"
    impact = "Race conditions, zombie processes, or platform-specific hangs."
    heuristic = True

    def _collect_main_blocks(self, tree):
        blocks = []
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                t = node.test
                if (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == "__name__"
                    and t.ops and isinstance(t.ops[0], ast.Eq)
                    and t.comparators and isinstance(t.comparators[0], ast.Constant)
                    and t.comparators[0].value == "__main__"):
                    start = getattr(node, "lineno", 1)
                    end = max([getattr(n, "lineno", start) for n in ast.walk(node)] or [start])
                    blocks.append((start, end))
        return blocks

    def _in_main(self, lineno, main_blocks):
        return any(a <= lineno <= b for a, b in main_blocks)

    def _is_ctor(self, call_node, names: set[str], module: str, ctor: str) -> bool:
        f = call_node.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            if f.value.id == module and f.attr == ctor:
                return True
        if isinstance(f, ast.Name) and f.id in names:
            return True
        return False

    def check(self, filename, tree, text):
        issues = []
        if not tree: return issues

        main_blocks = self._collect_main_blocks(tree)

        threading_names = set()
        mp_process_names = set()
        mp_pool_names = set()

        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom):
                if n.module == "threading":
                    for a in n.names:
                        if a.name == "Thread":
                            threading_names.add(a.asname or a.name)
                if n.module == "multiprocessing":
                    for a in n.names:
                        if a.name == "Process":
                            mp_process_names.add(a.asname or a.name)
                        if a.name == "Pool":
                            mp_pool_names.add(a.asname or a.name)

        def analyze_scope(body_nodes: list[ast.stmt], scope_name: str, in_module: bool):
            thread_vars_started: set[str] = set()
            thread_vars_joined: set[str]  = set()
            proc_vars_started: set[str]   = set()
            proc_vars_joined: set[str]    = set()
            thread_start_lines: dict[str, int] = {}
            proc_start_lines: dict[str, int]   = {}
            thread_vars: set[str] = set()
            proc_vars: set[str]   = set()

            for node in ast.walk(ast.Module(body=body_nodes, type_ignores=[])):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    call = node.value
                    if self._is_ctor(call, threading_names, "threading", "Thread"):
                        for t in node.targets:
                            if isinstance(t, ast.Name):
                                thread_vars.add(t.id)
                    if self._is_ctor(call, mp_process_names, "multiprocessing", "Process"):
                        for t in node.targets:
                            if isinstance(t, ast.Name):
                                proc_vars.add(t.id)

                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    attr = node.func.attr
                    base = node.func.value
                    if isinstance(base, ast.Name):
                        if attr == "start" and base.id in thread_vars:
                            thread_vars_started.add(base.id); thread_start_lines.setdefault(base.id, getattr(node, "lineno", 1))
                        if attr == "join"  and base.id in thread_vars:
                            thread_vars_joined.add(base.id)
                        if attr == "start" and base.id in proc_vars:
                            proc_vars_started.add(base.id); proc_start_lines.setdefault(base.id, getattr(node, "lineno", 1))
                        if attr == "join"  and base.id in proc_vars:
                            proc_vars_joined.add(base.id)

                    if attr == "start" and isinstance(base, ast.Call):
                        if self._is_ctor(base, threading_names, "threading", "Thread"):
                            issues.append(self.make(getattr(node, "lineno", 1),
                                "Thread started without a matching join(); ensure a join() in this code path."))
                        if self._is_ctor(base, mp_process_names, "multiprocessing", "Process"):
                            issues.append(self.make(getattr(node, "lineno", 1),
                                "Process started without a matching join(); ensure a join() in this code path."))

                if in_module and isinstance(node, ast.Call):
                    parent_is_module = True  # our walk wrapper uses Module(body=...), so top-level nodes are module children
                    if parent_is_module and (self._is_ctor(node, mp_pool_names, "multiprocessing", "Pool")
                        or self._is_ctor(node, mp_process_names, "multiprocessing", "Process")):
                        ln = getattr(node, "lineno", 1)
                        if not self._in_main(ln, main_blocks):
                            issues.append(self.make(ln,
                                "multiprocessing object created at import time; protect with if __name__ == '__main__':"))

            for v in sorted(thread_vars_started - thread_vars_joined):
                issues.append(self.make(thread_start_lines.get(v, 1),
                    f'Thread "{v}" started but not joined in scope "{scope_name}".'))
            for v in sorted(proc_vars_started - proc_vars_joined):
                issues.append(self.make(proc_start_lines.get(v, 1),
                    f'Process "{v}" started but not joined in scope "{scope_name}".'))

        analyze_scope(getattr(tree, "body", []), scope_name="<module>", in_module=True)

        for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            analyze_scope(fn.body, scope_name=fn.name, in_module=False)

        return issues



class ThreadSafetyRule(Rule):
    """
    Heuristics for thread-safety risks:
      - Detect module-level mutable globals (list/dict/set) that are written,
      - AND presence of threading.Thread usage in the module.
    """

    CATEGORY = "Concurrency"
    PRIORITY = "MEDIUM"
    IMPACT = "Shared mutable globals accessed by threads can cause races; use locks or confine state."

    def visit_Module(self, node: ast.Module) -> None:
        self._threads_present = False
        self._mutable_globals = set()
        self._global_writes = set()

        for n in ast.walk(node):
            for ch in ast.iter_child_nodes(n):
                setattr(ch, "parent", n)

        for n in ast.walk(node):
            if isinstance(n, ast.Call) and isinstance(n.func, (ast.Name, ast.Attribute)):
                name = n.func.id if isinstance(n.func, ast.Name) else n.func.attr
                if name == "Thread":
                    self._threads_present = True
                    break

        for n in node.body:
            if isinstance(n, ast.Assign):
                if any(isinstance(t, ast.Name) for t in n.targets):
                    if isinstance(n.value, (ast.Dict, ast.List, ast.Set)):
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                self._mutable_globals.add(t.id)

        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    for name in self._names_written(t):
                        if name in self._mutable_globals:
                            self._global_writes.add(name)
            elif isinstance(n, ast.AugAssign):
                for name in self._names_written(n.target):
                    if name in self._mutable_globals:
                        self._global_writes.add(name)
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if isinstance(n.func.value, ast.Name) and n.func.value.id in self._mutable_globals:
                    self._global_writes.add(n.func.value.id)

        if self._threads_present and self._global_writes:
            lines = sorted({getattr(n, "lineno", 1) for n in ast.walk(node)
                            if isinstance(n, ast.Name) and n.id in self._global_writes})
            self.report(
                self.CATEGORY,
                self.PRIORITY,
                lines[0] if lines else 1,
                self.IMPACT,
                f"{self.filename}: Mutable globals {sorted(self._global_writes)} written while using threads; use locks or avoid shared state."
            )

    def _names_written(self, target: ast.AST):
        names = set()
        for n in ast.walk(target):
            if isinstance(n, ast.Name):
                names.add(n.id)
        return names


class OpenEncodingRule(Rule):
    """
    Require explicit 'encoding=' when opening text files.
    Triggers when:
      - open(...) called without 'encoding' kwarg, and
      - mode is missing or indicates text (e.g., 'r', 'w', 'a', 'rt', 'wt', etc.).
    """

    CATEGORY = "Robustness"
    PRIORITY = "LOW"
    IMPACT = "Implicit platform encoding can cause subtle bugs across environments."

    _TEXT_PREFIXES = ("r", "w", "a", "x")
    _BINARY_FLAG = "b"

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            has_encoding = any(isinstance(kw, ast.keyword) and kw.arg == "encoding" for kw in node.keywords)
            mode = None
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
                mode = node.args[1].value

            text_mode = False
            if mode is None:
                text_mode = True  # default is text
            elif any(mode.startswith(p) for p in self._TEXT_PREFIXES) and self._BINARY_FLAG not in mode:
                text_mode = True

            if text_mode and not has_encoding:
                self.report(
                    self.CATEGORY,
                    self.PRIORITY,
                    node.lineno,
                    self.IMPACT,
                    f"{self.filename}: open() called for text mode without 'encoding='."
                )
        self.generic_visit(node)




class CircularImportRule(Rule):
    """
    Heuristic for potential circular-import workarounds:
      - Local ('package.module') imports inside function bodies.
      - Conditional TYPE_CHECKING imports (often used to break cycles).
    These are *signals*, not definitive cycles, so warn as MEDIUM with clear wording.
    """

    CATEGORY = "Maintainability"
    PRIORITY = "MEDIUM"
    IMPACT = "Likely circular-import workaround; consider refactoring shared types or moving imports."

    def visit_Import(self, node: ast.Import) -> None:
        if self._inside_function(node) and any("." in n.name for n in node.names):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Local-module import inside a function suggests a circular import workaround.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if self._inside_function(node) and (node.level or (node.module and "." in node.module)):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Relative/inner import inside a function suggests a circular import workaround.")
        parent_if = getattr(node, "parent_if", None)
        if parent_if and isinstance(parent_if.test, ast.Attribute) and getattr(parent_if.test, "attr", "") == "TYPE_CHECKING":
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Import under TYPE_CHECKING likely indicates a type-only import to avoid cycles.")
        self.generic_visit(node)

    def _inside_function(self, node: ast.AST) -> bool:
        cur = getattr(node, "parent", None)
        while cur:
            if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return True
            if isinstance(cur, ast.If):
                if isinstance(node, ast.ImportFrom):
                    setattr(node, "parent_if", cur)
            cur = getattr(cur, "parent", None)
        return False


class ImportOrderRule(Rule):
    """
    Light-weight import hygiene:
      - Relative ('from .', 'from ..') should come *after* absolute imports.
      - Within a contiguous import block, names should be alphabetically ordered.
    (Full stdlib/third-party/local grouping requires project config; this rule focuses on obvious cases.)
    """

    CATEGORY = "Style/Maintainability"
    PRIORITY = "LOW"
    IMPACT = "Consistent import ordering improves readability and reduces merge noise."

    def visit_Module(self, node: ast.Module) -> None:
        lines = {}
        for n in node.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                lines[n.lineno] = n

        seen_absolute = False
        for lineno in sorted(lines):
            n = lines[lineno]
            if isinstance(n, ast.ImportFrom) and n.level and n.level > 0:
                if not seen_absolute:
                    self.report(self.CATEGORY, self.PRIORITY, n.lineno, self.IMPACT,
                                f"{self.filename}: Relative import appears before absolute imports; reorder.")
            else:
                seen_absolute = True

        block = []
        prev_lineno = None
        for lineno in sorted(lines):
            if prev_lineno is None or lineno == prev_lineno + 1:
                block.append(lines[lineno])
            else:
                self._check_block(block)
                block = [lines[lineno]]
            prev_lineno = lineno
        if block:
            self._check_block(block)

    def _check_block(self, block):
        names = []
        for node in block:
            if isinstance(node, ast.Import):
                for a in node.names:
                    names.append(a.name)
            else:
                base = ("." * node.level) + (node.module or "")
                for a in node.names:
                    names.append(f"{base}.{a.name}" if base else a.name)
        if names != sorted(names, key=str.lower):
            self.report(self.CATEGORY, self.PRIORITY, block[0].lineno, self.IMPACT,
                        f"{self.filename}: Import statements in this block are not alphabetically ordered.")


class IgnoredReturnValueRule(Rule):
    """
    Warn when the value from a likely-value-returning call is ignored.
    Heuristics: function/method names like get/find/compute/search/match/read/load/json/build/calc
    Skip known side-effecty names like print, write, add, update, setdefault, append, extend, logger.*.
    """

    CATEGORY = "Correctness"
    PRIORITY = "LOW"
    IMPACT = "Ignoring return values can hide bugs and make code harder to reason about."

    SUSPECT_PREFIXES = ("get", "find", "compute", "calc", "build", "create",
                        "search", "match", "read", "load", "parse", "json")
    SIDE_EFFECTY = {"print", "write", "writelines", "append", "extend", "add", "update", "setdefault",
                    "logger", "log", "info", "warning", "error", "debug", "critical"}

    def visit_Expr(self, node: ast.Expr) -> None:
        if isinstance(node.value, ast.Call):
            func = node.value.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr

            if name:
                low = name.lower()
                if any(low.startswith(p) for p in self.SUSPECT_PREFIXES) and low not in self.SIDE_EFFECTY:
                    self.report(
                        self.CATEGORY,
                        self.PRIORITY,
                        node.lineno,
                        self.IMPACT,
                        f"{self.filename}: Return value from '{name}()' is ignored; assign or use it."
                    )
        self.generic_visit(node)


class ComplexityRule(Rule):
    """
    Simple cyclomatic-like complexity + size check.
    Triggers if complexity > max_complexity OR lines > max_lines (configurable).
    """

    CATEGORY = "Maintainability"
    PRIORITY = "LOW"
    IMPACT = "High complexity/size reduces readability and increases bug risk."

    def __init__(self, max_complexity: int = 10, max_lines: int = 50) -> None:
        self.max_complexity = max_complexity
        self.max_lines = max_lines

    def _complexity(self, node: ast.AST) -> int:
        score = 1
        for n in ast.walk(node):
            if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With,
                              ast.BoolOp, ast.IfExp, ast.comprehension, ast.Match)):
                score += 1
        return score

    def _loc(self, node: ast.AST) -> int:
        start = getattr(node, "lineno", None)
        end = getattr(node, "end_lineno", None)
        if start and end:
            return (end - start) + 1
        return 0

    def _check_named(self, node, kind: str, name: str) -> None:
        cplx = self._complexity(node)
        loc = self._loc(node)
        if cplx > self.max_complexity or loc > self.max_lines:
            self.report(
                self.CATEGORY,
                self.PRIORITY,
                node.lineno,
                self.IMPACT,
                f"{self.filename}: {kind} '{name}' too complex (C={cplx}, LOC={loc}); "
                f"thresholds: C>{self.max_complexity} or LOC>{self.max_lines}."
            )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_named(node, "Function", node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_named(node, "Async function", node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._check_named(node, "Class", node.name)
        self.generic_visit(node)


class MissingDocstringRule(Rule):
    """
    Require docstrings on public modules, classes, and functions.
    Public = name not starting with underscore.
    """

    CATEGORY = "Style/Maintainability"
    PRIORITY = "LOW"
    IMPACT = "Missing docstrings hurt discoverability and maintenance."

    def visit_Module(self, node: ast.Module) -> None:
        if not ast.get_docstring(node):
            self.report(self.CATEGORY, self.PRIORITY, 1, self.IMPACT,
                        f"{self.filename}: Module missing top-level docstring.")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not node.name.startswith("_") and not ast.get_docstring(node):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Public function '{node.name}' missing docstring.")
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if not node.name.startswith("_") and not ast.get_docstring(node):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Public async function '{node.name}' missing docstring.")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if not node.name.startswith("_") and not ast.get_docstring(node):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Public class '{node.name}' missing docstring.")
        self.generic_visit(node)


class MagicLiteralRule(Rule):
    """
    Flags suspicious 'magic' numeric literals in code paths (comparisons/returns/assignments)
    that are not defined as named constants.
    Exempt common sentinels: -1, 0, 1, 2 and indexes in range() calls.
    """

    CATEGORY = "Style"
    PRIORITY = "LOW"
    IMPACT = "Unexplained literals obscure intent; prefer named constants."

    _allowed = {-1, 0, 1, 2}

    def visit_Compare(self, node: ast.Compare) -> None:
        self._check_literal(node)
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        self._check_literal(node)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Skip assignments to ALL_CAPS (these *define* constants)
        if not all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
            self._check_literal(node)
        self.generic_visit(node)

    def _check_literal(self, node: ast.AST) -> None:
        def bad_num(n: ast.AST) -> bool:
            return isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and n.value not in self._allowed

        # Don’t flag inside a range(...) call (common iteration)
        def inside_range(n: ast.AST) -> bool:
            cur = n
            while cur:
                if isinstance(cur, ast.Call) and isinstance(cur.func, ast.Name) and cur.func.id == "range":
                    return True
                cur = getattr(cur, "parent", None)
            return False

        for child in ast.walk(node):
            if bad_num(child) and not inside_range(child):
                self.report(self.CATEGORY, self.PRIORITY, getattr(child, "lineno", getattr(node, "lineno", 1)),
                            self.IMPACT, f"{self.filename}: Magic literal '{child.value}' detected; use a named constant.")


class EmptyExceptBodyRule(Rule):
    """
    Flags except blocks that effectively swallow errors (pass/ellipsis/literal-only).
    """

    CATEGORY = "Error Handling"
    PRIORITY = "HIGH"
    IMPACT = "Silently ignoring errors hides failures and complicates debugging."

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if not node.body:
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: Empty 'except' block; handle or re-raise.")
            return

        def _trivial(stmt: ast.stmt) -> bool:
            if isinstance(stmt, ast.Pass):
                return True
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                return stmt.value.value is Ellipsis or isinstance(stmt.value.value, str)
            return False

        if all(_trivial(s) for s in node.body):
            self.report(self.CATEGORY, self.PRIORITY, node.lineno, self.IMPACT,
                        f"{self.filename}: 'except' body does nothing (pass/ellipsis/docstring). Avoid swallowing exceptions.")
        self.generic_visit(node)


class ExceptionChainingRule(Rule):
    """
    Flag re-raises inside except blocks that drop the original context.
    Examples:
        except Exception as e:
            raise ValueError("bad")         # <-- missing "from e"
        except Exception:
            raise SomeError from None       # <-- explicitly suppresses context
    Allowed:
        except Exception as e:
            raise ValueError("bad") from e
        except Exception:
            raise
    """

    CATEGORY = "Error Handling"
    PRIORITY = "MEDIUM"
    IMPACT = "Lost traceback/context makes debugging and triage harder."

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        for sub in node.body:
            if isinstance(sub, ast.Raise):
                if sub.exc is None:
                    continue
                # has explicit 'from cause'?
                if sub.cause is None:
                    self.report(
                        "Error Handling",
                        self.PRIORITY,
                        getattr(sub, "lineno", node.lineno),
                        self.IMPACT,
                        f"{self.filename}: New exception raised in 'except' without 'from' to preserve context."
                    )
                else:
                    if isinstance(sub.cause, ast.Constant) and sub.cause.value is None:
                        self.report(
                            "Error Handling",
                            self.PRIORITY,
                            getattr(sub, "lineno", node.lineno),
                            self.IMPACT,
                            f"{self.filename}: Exception raised 'from None' suppresses chaining; prefer 'from e' or bare re-raise."
                        )
        self.generic_visit(node)


ALL_RULES: List[Rule] = [
    BareOrBroadExcept(),
    AssertForRuntime(),
    MutableDefaultArgs(),
    OpenWithoutWith(),
    FileModeMismatch(),
    NonPythonicLoops(),
    LenComparisons(),
    IdentityVsEquality(),
    TypeCheckRule(),
    UnsafeCSVParsing(),
    EvalExecUse(),
    DangerousFunctions(),
    ConcurrencyRule(),
    ExitCallsInLibrary(),
    UnusedImports(),
    UnusedVariables(),
    WildcardImports(),
    ShadowBuiltins(),
    DangerousTokenMagicNumbers(),
    PrintStatements(),
    FStringMissing(),
    NamingConventions(),
    UndefinedNameRule(),
    DictAccessGuard(),
    ReturnAnnotationMismatch(),
    TodoComments(),
    PlatformSpecificPaths(),
    PotentialStringCastNeeded(),
    ExceptionChainingRule(),
    EmptyExceptBodyRule(),
    MagicLiteralRule(),
    MissingDocstringRule(),
    ComplexityRule(max_complexity=10, max_lines=50),
    IgnoredReturnValueRule(),
    ImportOrderRule(),
    CircularImportRule(),
    OpenEncodingRule(),
    ThreadSafetyRule(),

]

PRIORITY_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

def run_on_file(path: str, min_priority: str, max_lines: Optional[int]) -> List[Issue]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return []
    tree = _safe_parse(text, path)
    issues: List[Issue] = []
    for rule in ALL_RULES:
        findings = rule.check(path, tree, text)
        for iss in findings:
            if PRIORITY_RANK.get(iss.priority, 1) >= PRIORITY_RANK.get(min_priority, 1):
                if max_lines and "," in iss.impacted_lines:
                    lines = iss.impacted_lines.split(",")
                    if len(lines) > max_lines:
                        kept = ",".join(lines[:max_lines]) + f",+{len(lines) - max_lines} more"
                        issues.append(Issue(iss.category, iss.priority, kept, iss.potential_impact, iss.description))
                        continue
                issues.append(iss)
    return issues


def _severity_pick_max(a: str, b: str) -> str:
    return a if PRIORITY_RANK.get(a, 0) >= PRIORITY_RANK.get(b, 0) else b

def _parse_lines(s: str) -> list[int]:
    """
    Parse 'impacted_lines' strings like '12', '10-12', '3,7,9', '11-13,17' into a list of ints.
    Unknown formats are ignored.
    """
    lines: list[int] = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                start, end = int(a), int(b)
                if start <= end:
                    lines.extend(range(start, end + 1))
            except ValueError:
                pass
        else:
            try:
                lines.append(int(part))
            except ValueError:
                pass
    return lines

def _compress_lines(nums: list[int]) -> str:
    """
    Turn sorted unique ints into compact ranges: [1,2,3,7,9,10] -> '1-3,7,9-10'
    """
    if not nums:
        return ""
    nums = sorted(set(nums))
    out = []
    start = prev = nums[0]
    for x in nums[1:]:
        if x == prev + 1:
            prev = x
            continue
        out.append(f"{start}-{prev}" if start != prev else f"{start}")
        start = prev = x
    out.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ",".join(out)

def merge_same_issue_across_lines(items: list[tuple[str, Issue]]) -> list[tuple[str, Issue]]:
    """
    Merge *identical issues* on different lines into a single row per (file, category, potential_impact, description).

    Rules:
    - Key = (filename, category, normalized potential_impact, normalized description)
      -> “exactly the same issue” as you requested
    - impacted_lines: union of all lines, sorted & range-compressed
    - priority: keep the highest across merged items
    - potential_impact / description: keep unique texts (in practice they’re already identical per key)
    - keep stable output order: first occurrence of each key defines order
    """
    def norm(s: str) -> str:
        return " ".join(s.split())  # collapse whitespace only

    grouped: dict[tuple[str, str, str, str], dict] = {}
    order: list[tuple[str, str, str, str]] = []

    for filename, issue in items:
        key = (filename, issue.category, norm(issue.potential_impact), norm(issue.description))
        if key not in grouped:
            grouped[key] = {
                "filename": filename,
                "category": issue.category,
                "priority": issue.priority,
                "impacted_lines": _parse_lines(issue.impacted_lines),
                "impacts": [issue.potential_impact],
                "descs": [issue.description],
            }
            order.append(key)
        else:
            g = grouped[key]
            g["priority"] = _severity_pick_max(g["priority"], issue.priority)
            g["impacted_lines"].extend(_parse_lines(issue.impacted_lines))
            if issue.potential_impact not in g["impacts"]:
                g["impacts"].append(issue.potential_impact)
            if issue.description not in g["descs"]:
                g["descs"].append(issue.description)

    merged: list[tuple[str, Issue]] = []
    for key in order:
        g = grouped[key]
        lines = _compress_lines(g["impacted_lines"])
        merged.append((
            g["filename"],
            Issue(
                category=g["category"],
                priority=g["priority"],
                impacted_lines=lines if lines else "",  # should not be empty
                potential_impact=" | ".join(g["impacts"]),
                description=" | ".join(g["descs"]),
            ),
        ))
    return merged



def write_csv(issues: List[Tuple[str, Issue]], out_path: str):
    headers = ["category of issue", "priority of issue", "impacted lines", "potential impact", "description"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(headers)
        for filename, issue in issues:
            full_desc = f"{os.path.basename(filename)}: {issue.description}"
            w.writerow([issue.category, issue.priority, issue.impacted_lines, issue.potential_impact, full_desc])


def write_json(issues: List[Tuple[str, Issue]], out_path: str) -> None:
    """
    Write machine-readable JSON. Schema (array of objects):
      [
        {
          "file": "path/to/file.py",
          "category": "...",
          "priority": "LOW|MEDIUM|HIGH",
          "impacted_lines": "1,2,3" | "10-12" | "",
          "potential_impact": "...",
          "description": "filename: message"
        },
        ...
      ]
    """
    data = []
    for filename, issue in issues:
        item = {
            "file": filename,
            "category": issue.category,
            "priority": issue.priority,
            "impacted_lines": issue.impacted_lines,
            "potential_impact": issue.potential_impact,
            "description": f"{os.path.basename(filename)}: {issue.description}",
        }
        data.append(item)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def write_text_log(issues: List[Tuple[str, Issue]], filename: str, log_path: str) -> None:
    """
    Write a short, human-friendly log summary:
      - file name
      - total issues
      - counts by priority
      - counts by category
      - first few example lines
    """
    by_priority: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_category: Dict[str, int] = {}
    examples: List[str] = []

    for _, iss in issues:
        by_priority[iss.priority] = by_priority.get(iss.priority, 0) + 1
        by_category[iss.category] = by_category.get(iss.category, 0) + 1
        if len(examples) < 10:
            examples.append(
                f"[{iss.priority}] {iss.category} @ {iss.impacted_lines} :: {iss.description}"
            )

    total = len(issues)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"pycodereview summary for {os.path.basename(filename)}\n")
        f.write("=" * 72 + "\n")
        f.write(f"Total issues: {total}\n")
        f.write(
            f"By priority: HIGH={by_priority.get('HIGH',0)}, "
            f"MEDIUM={by_priority.get('MEDIUM',0)}, "
            f"LOW={by_priority.get('LOW',0)}\n"
        )
        f.write("By category:\n")
        for cat, cnt in sorted(by_category.items(), key=lambda kv: (-kv[1], kv[0])):
            f.write(f"  - {cat}: {cnt}\n")
        if examples:
            f.write("\nExamples:\n")
            for ex in examples:
                f.write(f"  • {ex}\n")

def _priority_sort_key(p: str) -> int:
    return -PRIORITY_RANK.get(p, 0)

def sort_findings(items: list[tuple[str, Issue]]) -> list[tuple[str, Issue]]:
    def first_line(s: str) -> int:
        # impacted_lines can be "12", "10-22", "3,7,9", "12,+3 more"
        head = s.split(",", 1)[0]
        head = head.split("-", 1)[0]
        try:
            return int(head)
        except ValueError:
            return 0
    return sorted(
        items,
        key=lambda x: (
            _priority_sort_key(x[1].priority),
            x[1].category,
            os.path.basename(x[0]),
            first_line(x[1].impacted_lines),
        ),
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pycodereview",
        description="Static checks for Python code quality, correctness, security, and maintainability.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  pycodereview path/to/file.py\n"
            "  pycodereview path/to/file.py --merge-issues\n"
            "  pycodereview path/to/file.py --min-priority MEDIUM --out report.csv --log review.log\n"
        ),
    )
    parser.add_argument(
        "file",
        help="Single Python source file to analyze (e.g., src/module.py)",
    )
    parser.add_argument(
        "--out",
        default="review_report.csv",
        help="Output CSV path (semicolon-delimited). Default: review_report.csv",
    )
    parser.add_argument(
        "--json-output",
        dest="json_output",
        default=None,
        help="Optional path to also write machine-readable JSON output.",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Optional path to write a short text log/summary (e.g., analysis.log).",
    )
    parser.add_argument(
        "--min-priority",
        default="LOW",
        choices=["LOW", "MEDIUM", "HIGH"],
        help="Only report issues at or above this priority. Default: LOW",
    )
    parser.add_argument(
        "--fail-on",
        default=None,
        choices=["LOW", "MEDIUM", "HIGH"],
        help="Exit with code 2 if any issue at/above this priority is found.",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=None,
        help="If an issue lists many impacted lines, cap the shown count to this number.",
    )
    parser.add_argument(
        "--merge-issues",
        action="store_true",
        help="Merge identical issues across multiple lines into a single row.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="pycodereview 1.0.1",
    )

    args = parser.parse_args(argv)

    # ---- Simple single-file validation (no directories in v1) ----
    if not os.path.exists(args.file):
        parser.error(f"Input path does not exist: {args.file}")
    if os.path.isdir(args.file):
        parser.error(
            "Directories are not supported in v1. Please pass a single .py file.\n"
            "Tip: you can batch files with a shell loop script if needed."
        )
    if not args.file.lower().endswith(".py"):
        parser.error("Input must be a .py source file.")

    # ---- Run analysis on the single file ----
    all_issues: List[Tuple[str, Issue]] = []
    file_issues = run_on_file(args.file, args.min_priority, args.max_lines)
    all_issues.extend((args.file, iss) for iss in file_issues)

    if args.merge_issues:
        all_issues = merge_same_issue_across_lines(all_issues)

    all_issues = sort_findings(all_issues)

    # ---- Outputs ----
    write_csv(all_issues, args.out)
    if args.json_output:
        write_json(all_issues, args.json_output)
    if args.log:
        write_text_log(all_issues, args.file, args.log)

    # ---- Optional failing threshold ----
    if args.fail_on:
        threshold = PRIORITY_RANK[args.fail_on]
        worst = 0
        for _, iss in all_issues:
            worst = max(worst, PRIORITY_RANK.get(iss.priority, 0))
        if worst >= threshold:
            return 2

    return 0

if __name__ == "__main__":
    sys.exit(main())
