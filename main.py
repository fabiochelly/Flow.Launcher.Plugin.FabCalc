from os.path import dirname, abspath, join
from sys import path
from math import pi, cos, sin, tan, log, log10, log2, exp, sqrt, acos, asin, atan, atan2, ceil, floor, degrees, radians, trunc, factorial, gcd, pow
from re import compile as re_compile
from subprocess import run
from fractions import Fraction
import uuid
import time
import os
import hashlib

debug = False
basedir = dirname(abspath(__file__))
path.append(join(basedir, "lib"))
from flowlauncher import FlowLauncher

icon_path = join(basedir, "assets", "favicon.png")
base_rx = re_compile("^[\dA-F]+[hbdo]{1,2}$")
factor_rx = re_compile("factor\(\s*(\d+)\s*\)")
factorial_rx = re_compile("(\d+)!")
fractions_rx = re_compile("(\d+)\s*\/\/\s*(\d+)")
sym2int = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'a': 36, 'b': 37, 'c': 38, 'd': 39, 'e': 40, 'f': 41, 'g': 42, 'h': 43, 'i': 44, 'j': 45, 'k': 46, 'l': 47, 'm': 48, 'n': 49, 'o': 50, 'p': 51, 'q': 52, 'r': 53, 's': 54, 't': 55, 'u': 56, 'v': 57, 'w': 58, 'x': 59, 'y': 60, 'z': 61}
int2sym = {v: k for k, v in sym2int.items()}
uuids = {"uuid", "ulid", "cuid", "sulid"}
mathfuncs = list(uuids) + ["simplify", "integrate", "diff", "expand", "solve", "x", "y", "I", "Fraction", "factor", "pi", "cos", "sin", "tan", "abs", "log", "log10", "log2", "exp", "sqrt", "acos", "asin", "atan", "atan2", "ceil", "floor", "degrees", "radians", "trunc", "round", "factorial", "gcd", "pow"]
funcs_rx = re_compile(r'\b(?:' + '|'.join(mathfuncs) + r')\b')
symbols_rx = re_compile(r'[\d\s+*^()!.,/-]+')
safe_functions = {fn: globals()[fn] for fn in mathfuncs if fn in globals()}
decimalcomma = re_compile(r'(?<=\d),(?=\d)')
xfactor_rx = re_compile("(\d)(x)|(\d)(y)")
xpower_rx = re_compile("(x)(\d)|(y)(\d)")
i_rx = re_compile(r"(?<![a-z])i(?![a-z])")
sqrtnum_rx = re_compile(r"√\((\d+)\)")


def fablog(s):
    with open(join(basedir, "log.txt"), "a", encoding="utf-8") as f:
        f.write(f"{s}\n")


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

    @staticmethod
    def cuid():
        ts = FabCalc.int2str(int(time.time() * 1000), 36)
        pid = FabCalc.int2str(os.getpid(), 36)
        rand_block = hashlib.sha256(os.urandom(8)).hexdigest()[:20].upper()
        rand_block = FabCalc.int2str(FabCalc.str2int(rand_block, 16), 36)
        return f"c{ts}{pid}{rand_block}"[:25].lower()

    @staticmethod
    def uuid(cmd):
        if cmd == "cuid": return FabCalc.cuid()
        res = str(uuid.uuid4())
        if cmd != "uuid": res = res.replace("-", "")
        if cmd == "sulid": return FabCalc.int2str(FabCalc.str2int(res.upper(), 16), 62)
        return res
    
    @staticmethod
    def hashes(s):
        pos = s.find(" ")
        if pos == -1: return
        algo = s[:pos]
        if algo not in ("md5", "sha1", "sha256", "sha3_256", "sha3_512", "blake"): return
        expr = s[pos + 1:].encode()
        if algo == "md5": return hashlib.md5(expr).hexdigest()
        if algo == "sha1": return hashlib.sha1(expr).hexdigest()
        if algo == "sha256": return hashlib.sha256(expr).hexdigest()
        if algo == "sha3_256": return hashlib.sha3_256(expr).hexdigest()
        if algo == "sha3_512": return hashlib.sha3_512(expr).hexdigest()
        if algo == "blake": return hashlib.blake2b(expr).hexdigest()
    
    def special_entries(self, entry):
        if entry in uuids: return self.response(FabCalc.uuid(entry), f"{entry.upper()}: press Enter to copy to clipboard")
        res = FabCalc.hashes(entry)
        if res: return self.response(res, f"{entry}: press Enter to copy to clipboard")
        res = self.basecalc(entry)
        if res: return res

        if entry.startswith("factor("):
            m = factor_rx.search(entry)
            return None if m is None else self.response(self.factors(int(m.group(1))), entry)
    
    @staticmethod
    def for_display(entry):
        res = entry.replace("pi", "π").replace("**", "^").replace("*", " · ").replace("I", "ⅈ").replace("sqrt", "√")
        return sqrtnum_rx.sub("√\\1", res)
        

    def query(self, entry: str = ''):
        if not entry or len(entry) > 100: return
        try:
            query = entry.strip().replace("^", "**")
            if query.startswith("$"):
                from sympy import symbols, factor, expand, integrate, diff, solve, simplify, I, log, cos, sin, tan, acos, asin, atan, pi, sqrt
                x, y = symbols("x y")
                query = xfactor_rx.sub("\\1*\\2", query[1:])
                query = xpower_rx.sub("\\1**\\2", query)
                query = i_rx.sub("I", query)
                if not symbols_rx.fullmatch(funcs_rx.sub('', query)): return
                res = str(eval(query, {"__builtins__": None, "x": x, "y": y, "I": I, "Fraction": Fraction, "factor": factor, "expand": expand, "integrate": integrate, "diff": diff, "solve": solve, "simplify": simplify, "log": log, "cos": cos, "sin": sin, "tan": tan, "acos": acos, "asin": asin, "atan": atan, "pi": pi, "sqrt": sqrt}))
                return self.response(FabCalc.for_display(res), FabCalc.for_display(query))

            res = self.special_entries(query)
            if res: return res
            query = decimalcomma.sub(".", query)
            query = factorial_rx.sub("factorial(\\1)", query)
            query = fractions_rx.sub("Fraction(\\1,\\2)", query)
            if not symbols_rx.fullmatch(funcs_rx.sub('', query)): return            
            res = self.fmtnum(eval(query, {"__builtins__": None}, safe_functions))
            return self.response(res, FabCalc.for_display(entry))

        except Exception as e:
            if debug: return self.response(str(e), entry)


if __name__ == "__main__":
    FabCalc()
