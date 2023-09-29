from os.path import dirname, abspath, join
from sys import path
from math import pi, cos, sin, tan, log, log10, log2, exp, sqrt, acos, asin, atan, atan2, ceil, floor, degrees, radians, trunc, factorial, gcd, pow
from subprocess import run
from fractions import Fraction
import uuid
from time import time
import os
import hashlib
import warnings
from timeit import default_timer as timer
from datetime import datetime, timedelta
from re import findall, subn, sub, match, search, fullmatch

basedir = dirname(abspath(__file__))
path.append(join(basedir, "lib"))
from flowlauncher import FlowLauncher

def factor(val): return FabCalc.main_intfactor(int(val), True)
def factors(val): return FabCalc.main_intfactor(int(val), False)

icon_path = join(basedir, "fabcalc.png")
sym2int = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'a': 36, 'b': 37, 'c': 38, 'd': 39, 'e': 40, 'f': 41, 'g': 42, 'h': 43, 'i': 44, 'j': 45, 'k': 46, 'l': 47, 'm': 48, 'n': 49, 'o': 50, 'p': 51, 'q': 52, 'r': 53, 's': 54, 't': 55, 'u': 56, 'v': 57, 'w': 58, 'x': 59, 'y': 60, 'z': 61}
int2sym = {v: k for k, v in sym2int.items()}
uuids = {"uuid", "ulid", "cuid", "sulid"}
funcs = list(uuids) + ["now", "factors", "series", "expand_trig", "exp", "limit", "oo", "simplify", "integrate", "diff", "expand", "solve", "Fraction", "factor", "pi", "cos", "sin", "tan", "abs", "log", "log10", "log2", "exp", "sqrt", "acos", "asin", "atan", "atan2", "ceil", "floor", "degrees", "radians", "trunc", "round", "factorial", "gcd", "pow"]
funcs_pattern = r'\b(?:' + '|'.join(funcs) + r')\b'
safe_functions = {fn: globals()[fn] for fn in funcs if fn in globals()}

def fablog(s):
    with open(join(basedir, "log.txt"), "a", encoding="utf-8") as f:
        f.write(f"{s}\n")


class FabCalc(FlowLauncher):

    @staticmethod
    def format_date(expr, result):
        date_pattern = r'\d{4}-\d{2}-\d{2}|now'
        dates_in_expr = len(findall(date_pattern, expr))
    
        if dates_in_expr == 1:
            # Formater en tant que date
            base_datetime = datetime(1970, 1, 1)
            target_datetime = base_datetime + timedelta(seconds=result)
            res = target_datetime.strftime('%A %Y-%m-%d %H:%M:%S')
            return res[:-9] if res.endswith(" 00:00:00") else res

        # Formater en tant que durée
        days, remainder = divmod(int(result), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days:
            if not hours and not minutes and not seconds: return f"{days} days"
            return f"{days} d {hours} h {minutes} m and {seconds} s"
        return f"{hours} h {minutes} m {seconds} s"

    @staticmethod
    def replace_with_seconds(expr):
        if not expr or ("-" not in expr and "now" not in expr and ":" not in expr): return expr, 0
        # Regex pour identifier la date, l'heure seule
        pattern = r'(?:(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(?:\s(?P<hour>\d{2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?)?)|(?P<only_hour>\d{2}):(?P<only_minute>\d{2})(?::(?P<only_second>\d{2}))?'
    
        def compute_value(match):
            details = match.groupdict()
    
            if details['year']:
                # Si une date est spécifiée
                year = int(details['year'])
                month = int(details['month'])
                day = int(details['day'])
                hour = int(details['hour']) if details['hour'] else 0
                minute = int(details['minute']) if details['minute'] else 0
                second = int(details['second']) if details['second'] else 0
    
                base_datetime = datetime(1970, 1, 1)
                target_datetime = datetime(year, month, day, hour, minute, second)
                difference = target_datetime - base_datetime
    
                return str(int(difference.total_seconds()))
    
            elif details['only_hour']:
                # Si seule une heure est spécifiée
                hour = int(details['only_hour'])
                minute = int(details['only_minute']) if details['only_minute'] else 0
                second = int(details['only_second']) if details['only_second'] else 0
    
                return str(hour * 3600 + minute * 60 + second)
    
        # Remplacer toutes les occurrences de dates et heures dans la chaîne par leur équivalent en secondes
        res, cnt = subn(pattern, compute_value, expr)
        if cnt > 0 or "now" in expr:
            res = sub(r"\bnow\b", str(time()), res)
            res = sub(r"\b(\d+)w\b", r"+(\1*7*86400)", res)
            res = sub(r"\b(\d+)d\b", r"+(\1*86400)", res)
            res = sub(r"\b(\d+)h\b", r"+(\1*3600)", res)
            res = sub(r"\b(\d+)m\b", r"+(\1*60)", res)
            res = sub(r"\b(\d+)s\b", r"+\1", res)
            cnt += 1
        return res, cnt

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
    def sympy_factors(n, multiples):
        from sympy import primefactors
        factors = primefactors(n)
        if not multiples: return str(factors)
        res = []
        for i in factors:
            while n % i == 0:
                res.append(FabCalc.fmtint(i))
                n //= i
        return " · ".join(res)

    @staticmethod
    def main_intfactor(n, multiples):
        length = len(str(n))
        if n < 2 or length > 99: return "Out of range"
        if length > 15: return FabCalc.sympy_factors(n, multiples)
        res = []
        while n % 2 == 0:
            res.append("2" if multiples else 2)
            n //= 2

        for i in range(3, int(sqrt(n)) + 1, 2):
            while n % i == 0:
                res.append(FabCalc.fmtint(i) if multiples else i)
                n //= i

        if n > 2: res.append(FabCalc.fmtint(n) if multiples else n)
        return " · ".join([str(el) for el in res]) if multiples else str(sorted(set(res)))

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
        p = text.find(" = ")
        if p > -1: text = text[p + 3:].strip()
        run("clip", input=text.encode('UTF-16LE'), check=True)

    def basecalc(self, query: str):
        q = query
        if q.startswith("0x"): q = q[2:].upper() + "h"
        elif q.startswith("0d"): q = q[2:].upper() + "d"
        elif q.startswith("0b"): q = q[2:] + "b"
        elif q.startswith("0o"): q = q[2:] + "o"
        elif q.startswith("0") and len(q) > 1 and q[1].isdigit(): q = q[1:] + "o"

        if not match(r"^[\dA-F]+[hbdo]{1,2}$", q): return False
        ivals = {"b": 2, "o": 8, "d": 10, "h": 16}
        last, prev = q[-1], q[-2]
        if prev in "hdbo": b1, b2, num = ivals[prev], ivals[last], q[:-2]
        else: b1, b2, num = ivals[last], ivals[("h" if last == "d" else "d")], q[:-1]

        names = {2: "bin", 8: "oct", 10: "dec", 16: "hex"}
        res = FabCalc.int2str(FabCalc.str2int(num, b1), b2)
        return self.response(res, f"{num} {names[b1]} = {res} {names[b2]}")

    @staticmethod
    def cuid():
        ts = FabCalc.int2str(int(time() * 1000), 36)
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
        if algo not in ("md5", "sha1", "sha256", "sha3_256", "sha3_512", "blake", "sha3", "sha512"): return
        expr = s[pos + 1:].encode()
        if algo == "md5": return hashlib.md5(expr).hexdigest()
        if algo == "sha1": return hashlib.sha1(expr).hexdigest()
        if algo == "sha256": return hashlib.sha256(expr).hexdigest()
        if algo == "sha3_256": return hashlib.sha3_256(expr).hexdigest()
        if algo == "sha3_512": return hashlib.sha3_512(expr).hexdigest()
        if algo == "blake": return hashlib.blake2b(expr).hexdigest()

    @staticmethod
    def for_display(entry):
        res = entry.replace("pi", "π").replace("**", "^").replace("*", " · ").replace("I", "ⅈ").replace("sqrt", "√").replace("oo", "∞")
        return sub(r"√\((\d+)\)", "√\\1", res)

    def query(self, entry: str = ''):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if not entry or len(entry) > 200: return
            try:
                # Special queries
                if entry in uuids: return self.response(FabCalc.uuid(entry), f"{entry.upper()}: press Enter to copy to clipboard")
                res = FabCalc.hashes(entry)
                if res: return self.response(res, f"{entry}: press Enter to copy to clipboard")
                res = self.basecalc(entry)
                if res: return res
                query, datecnt = self.replace_with_seconds(entry)

                # Valid formula
                if not fullmatch(r'[xyi\d\s+*^()!.,/-]+', sub(funcs_pattern, '', query)): return
                query = query.strip().replace("^", "**")
                if "(" in query and ")" not in query: query += ")"

                # Symbolic formula
                if "x" in query or "y" in query or "I" in query or "i" in query:
                    from sympy import series, expand_trig, oo, exp, limit, symbols, factor, expand, integrate, diff, solve, simplify, I, log, cos, sin, tan, acos, asin, atan, pi, sqrt
                    x, y = symbols("x y")
                    query = sub(r"(\d)\(", "\\1*(", query)
                    query = sub("(\d)(x)|(\d)(y)", "\\1*\\2", query)
                    query = sub("(x)(\d)|(y)(\d)", "\\1**\\2", query)
                    query = sub(r"(?<![a-z])i(?![a-z])", "I", query)
                    res = str(eval(query, {"__builtins__": None, "series": series, "expand_trig": expand_trig, "oo": oo, "exp": exp, "limit": limit,  "x": x, "y": y, "I": I, "Fraction": Fraction, "factor": factor, "expand": expand, "integrate": integrate, "diff": diff, "solve": solve, "simplify": simplify, "log": log, "cos": cos, "sin": sin, "tan": tan, "acos": acos, "asin": asin, "atan": atan, "pi": pi, "sqrt": sqrt}))
                    return self.response(FabCalc.for_display(res), FabCalc.for_display(query))

                # Algebric formula
                query = sub("(\d+)!", "factorial(\\1)", query)
                query = sub(r'(?<=\d),(?=\d)', ".", query)
                raw_res = eval(query, {"__builtins__": None}, safe_functions)
                res = self.fmtnum(raw_res)

                if datecnt: return self.response(FabCalc.format_date(entry, raw_res), entry)
                if "/" in query:
                    query2, cnt = subn("(\d+)\s*/\s*(\d+)", "Fraction(\\1,\\2)", query)
                    res2 = eval(query2, {"__builtins__": None}, safe_functions) if cnt else ""
                    if "/" in str(res2): res = self.fmtnum(res2) + "  =  " + res

                return self.response(res, FabCalc.for_display(entry) + " >> " + query)

            except Exception as e:
                pass
                # return self.response(str(e), entry + " >> " + query)


if __name__ == "__main__":
    FabCalc()
