from os.path import dirname, abspath, join
from sys import path
from math import *
from re import compile as re_compile
from subprocess import run
from fractions import Fraction

basedir = dirname(abspath(__file__))
path.append(join(basedir, "lib"))
from flowlauncher import FlowLauncher

icon_path = join(basedir, "assets", "favicon.png")
base_rx = re_compile("^[\dA-F]+[hbdo]{1,2}$")
factor_rx = re_compile("factor\(\s*(\d+)\s*\)")
factorial_rx = re_compile("(\d+)!")
fractions_rx = re_compile("(\d+)\s*\/\/\s*(\d+)")
sym2int = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
int2sym = {v: k for k, v in sym2int.items()}
mathfuncs = ["Fraction", "factor", "pi", "cos", "sin", "tan", "abs", "log", "log10", "log2", "exp", "sqrt", "acos", "asin", "atan", "atan2", "ceil", "floor", "degrees", "radians", "trunc", "round", "factorial", "gcd", "pow"]
funcs_rx = re_compile(r'\b(?:' + '|'.join(mathfuncs) + r')\b')
symbols_rx = re_compile(r'[\d\s+*^()!.,/-]+')
safe_functions = {fn: globals()[fn] for fn in mathfuncs if fn in globals()}
decimalcomma = re_compile(r'(?<=\d),(?=\d)')


class FabCalc(FlowLauncher):

    @staticmethod
    def int2str(intval, base):
        if base == 10: return str(intval)
        res = []
        while intval:
            intval, value = divmod(intval, base)
            res.append(int2sym[value])
        return ''.join(reversed(res))

    @staticmethod
    def str2int(snum, base):
        if base == 10: return int(snum)
        res = 0
        for c in snum:
            assert c in sym2int, f'Invalid character for base {base}'
            value = sym2int[c]
            assert value < base, f'Invalid digit for base {base}'
            res *= base
            res += value
        return res

    @staticmethod
    def factors(n):
        res = []
        while n % 2 == 0:
            res.append("2")
            n //= 2

        for i in range(3, int(sqrt(n)) + 1, 2):
            while n % i == 0:
                res.append(FabCalc.fmtint(i))
                n //= i

        if n > 2: res.append(FabCalc.fmtint(n))
        return " · ".join(res)

    @staticmethod
    def fmtnum(num):
        if isinstance(num, float):
            if abs(int(num) - num) < 0.000001: return FabCalc.fmtint(int(num))
            return f"{num:.8f}".replace("_", " ").rstrip("0")
        return FabCalc.fmtint(num) if isinstance(num, int) else str(num)

    @staticmethod
    def fmtint(num):
        return str(num) if num < 1000 else f"{num:_}".replace("_", " ")

    @staticmethod
    def response(title: str, subtitle: str):
        return [{
            'Title': title,
            'SubTitle': subtitle,
            'IcoPath': icon_path,
            "JsonRPCAction": {
                "method": "copy_to_clipboard",
                "parameters": [title]
            }
        }]

    def copy_to_clipboard(self, text: str):
        run("clip", input=text.encode('UTF-16LE'), check=True)

    def basecalc(self, query: str):
        q = query
        if q.startswith("0x"): q = q[2:].upper() + "h"
        elif q.startswith("0d"): q = q[2:].upper() + "d"
        elif q.startswith("0b"): q = q[2:] + "b"
        elif q.startswith("0o"): q = q[2:] + "o"
        elif q.startswith("0") and len(q) > 1 and q[1].isdigit(): q = q[1:] + "o"

        if not base_rx.match(q): return False
        ivals = {"b": 2, "o": 8, "d": 10, "h": 16}
        last, prev = q[-1], q[-2]
        if prev in "hdbo": b1, b2, num = ivals[prev], ivals[last], q[:-2]
        else: b1, b2, num = ivals[last], ivals[("h" if last == "d" else "d")], q[:-1]

        names = {2: "bin", 8: "oct", 10: "dec", 16: "hex"}
        res = FabCalc.int2str(FabCalc.str2int(num, b1), b2)
        return self.response(res, f"{num} {names[b1]} = {res} {names[b2]}")

    def query(self, entry: str = ''):
        try:
            query = entry.strip().replace("^", "**")
            query = decimalcomma.sub(".", query)
            if not query or len(query) > 100: return
            query = factorial_rx.sub("factorial(\\1)", query)
            query = fractions_rx.sub("Fraction(\\1,\\2)", query)
    
            res = self.basecalc(query)
            if res: return res

            if query.startswith("factor("):
                m = factor_rx.search(query)
                return None if m is None else self.response(self.factors(int(m.group(1))), query)

            if not symbols_rx.fullmatch(funcs_rx.sub('', query)): return
            result = eval(query, {"__builtins__": None}, safe_functions)
            return self.response(self.fmtnum(result), entry.replace("pi", "π"))
        except Exception:
            return


if __name__ == "__main__":
    FabCalc()
