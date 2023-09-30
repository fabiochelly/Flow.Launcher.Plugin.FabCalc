from os.path import dirname, abspath, join
from sys import path
from math import pi, cos, sin, tan, log, log10, log2, exp, sqrt, acos, asin, atan, atan2, ceil, floor, degrees, radians, trunc, factorial, gcd, pow
import warnings
from re import findall, subn, sub, match, fullmatch

basedir = dirname(abspath(__file__))
path.append(join(basedir, "lib"))
# noinspection PyUnresolvedReferences
from flowlauncher import FlowLauncher

def factor(val): return FabCalc.main_intfactor(int(val), True)
def factors(val): return FabCalc.main_intfactor(int(val), False)

icon_path = join(basedir, "fabcalc.png")
funcs = ["uuid", "now", "factors", "series", "expand_trig", "exp", "limit", "oo", "simplify", "integrate", "diff", "expand", "solve", "Fraction", "factor", "pi", "cos", "sin", "tan", "abs", "log", "log10", "log2", "exp", "sqrt", "acos", "asin", "atan", "atan2", "ceil", "floor", "degrees", "radians", "trunc", "round", "factorial", "gcd", "pow"]
funcs_pattern = r'\b(?:' + '|'.join(funcs) + r')\b'


class FabCalc(FlowLauncher):

    @staticmethod
    def format_date(expr, result):
        dates_in_expr = len(findall(r'\d{4}-\d{2}-\d{2}|now', expr))
    
        if dates_in_expr == 1:
            # Format as date
            from datetime import datetime, timedelta
            base_datetime = datetime(1970, 1, 1)
            target_datetime = base_datetime + timedelta(seconds=result)
            res = target_datetime.strftime('%A %Y-%m-%d %H:%M:%S')
            return res[:-9] if res.endswith(" 00:00:00") else res

        # Format as duration
        days, remainder = divmod(int(result), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days and not hours and not minutes and not seconds: return f"{days} days"
        res = {"d": days, "h": hours, "m": minutes, "s": seconds}
        return " ".join([f"{val}{suffix}" for suffix, val in res.items() if val > 0])

    @staticmethod
    def replace_with_seconds(expr):
        if not expr or ("-" not in expr and "now" not in expr and ":" not in expr): return expr, 0
        from datetime import datetime
        # Regex to identify dates and times
        pattern = r'(?:(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(?:\s(?P<hour>\d{2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?)?)|(?P<only_hour>\d{2}):(?P<only_minute>\d{2})(?::(?P<only_second>\d{2}))?'
    
        def compute_value(match):
            details = match.groupdict()
    
            if details['year']:
                # A date has been found
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
                # Only time has been found
                hour = int(details['only_hour'])
                minute = int(details['only_minute']) if details['only_minute'] else 0
                second = int(details['only_second']) if details['only_second'] else 0
    
                return str(hour * 3600 + minute * 60 + second)
    
        # Replaces all occurrences of dates and times in the string with their equivalent in seconds
        res, cnt = subn(pattern, compute_value, expr)
        if cnt > 0 or "now" in expr:
            from time import time
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
        if base == 16: return hex(intval).upper()[2:]
        res = []
        int2sym = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: 'a', 37: 'b', 38: 'c', 39: 'd', 40: 'e', 41: 'f', 42: 'g', 43: 'h', 44: 'i', 45: 'j', 46: 'k', 47: 'l', 48: 'm', 49: 'n', 50: 'o', 51: 'p', 52: 'q', 53: 'r', 54: 's', 55: 't', 56: 'u', 57: 'v', 58: 'w', 59: 'x', 60: 'y', 61: 'z'}
        while intval:
            intval, value = divmod(intval, base)
            res.append(int2sym[value])
        return ''.join(reversed(res))
    
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
    def res(title: str, subtitle: str):
        return {
            'Title': title,
            'SubTitle': subtitle,
            'IcoPath': icon_path,
            "JsonRPCAction": {"method": "copy_to_clipboard", "parameters": [title]}
        }

    # noinspection PyMethodMayBeStatic
    def copy_to_clipboard(self, text: str):
        p = text.find(" = ")
        if p > -1: text = text[p + 3:].strip()
        from subprocess import run
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
        try:
            res = FabCalc.int2str(int(num, b1), b2)
        except:
            return None
        return [self.res(res, f"{num} {names[b1]} = {res} {names[b2]}")]

    @staticmethod
    def cuid():
        from os import getpid, urandom
        from time import time
        ts = FabCalc.int2str(int(time() * 1000), 36)
        pid = FabCalc.int2str(getpid(), 36)
        from hashlib import sha256
        rand_block = sha256(urandom(8)).hexdigest()[:20].upper()
        rand_block = FabCalc.int2str(int(rand_block, 16), 36)
        return f"c{ts}{pid}{rand_block}"[:25].lower()

    @staticmethod
    def uuids():
        from uuid import uuid4
        res1 = str(uuid4())
        res2 = res1.replace("-", "")
        res3 = FabCalc.int2str(int(res2.upper(), 16), 62)
        info = "Press Enter to copy to clipboard"
        return [
            FabCalc.res(res1, f"UUID : {info}"),
            FabCalc.res(res2, f"ULID : {info}"),
            FabCalc.res(res3, f"Short version (base 62) : {info}"),
            FabCalc.res(FabCalc.cuid(), f"CUID (sortable) : {info}"),
        ]

    @staticmethod
    def is_hash(s):
        p = s.find(" ")
        return p > -1 and s[:p] in ("md5", "sha1", "sha256", "sha3_256", "sha3_512", "blake")

    @staticmethod
    def hashes(s):
        pos = s.find(" ")
        algo, expr = s[:pos], s[pos + 1:].encode()
        import hashlib
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

    @staticmethod
    def fraction_result(query, res, safe):
        # noinspection PyBroadException
        try:
            from fractions import Fraction
            query, cnt = subn(r"([\d.]+)\s*/\s*([\d.]+)", "Fraction(\\1,\\2)", query)
            res2 = str(eval(query, {"__builtins__": None, "Fraction": Fraction}, safe) if cnt else "")
            if "/" in res2: return f"{res2} = {res}"
        except:
            pass
        return res

    def symbolic_eval(self, query):
        from sympy import series, expand_trig, oo, exp, limit, symbols, factor, expand, integrate, diff, solve, simplify, I, log, cos, sin, tan, acos, asin, atan, pi, sqrt
        x, y = symbols("x y")
        query = sub(r"(\d)\(", "\\1*(", query)
        query = sub("(\d)(x)|(\d)(y)", "\\1*\\2", query)
        query = sub("(x)(\d)|(y)(\d)", "\\1**\\2", query)
        query = sub(r"(?<![a-z])i(?![a-z])", "I", query)
        res = str(eval(query, {"__builtins__": None, "series": series, "expand_trig": expand_trig, "oo": oo, "exp": exp, "limit": limit, "x": x, "y": y, "I": I, "factor": factor, "expand": expand, "integrate": integrate, "diff": diff, "solve": solve, "simplify": simplify, "log": log, "cos": cos, "sin": sin, "tan": tan, "acos": acos, "asin": asin, "atan": atan, "pi": pi, "sqrt": sqrt}))
        return [self.res(self.for_display(res), self.for_display(query))]

    def query(self, entry: str = ''):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if not entry or len(entry) > 200: return
            # noinspection PyBroadException
            try:
                # Special entries (hash, UUID, base conversion)
                if entry == "uuid": return FabCalc.uuids()
                if self.is_hash(entry): return [self.res(self.hashes(entry), f"{entry}: press Enter to copy to clipboard")] 
                res = self.basecalc(entry)
                if res: return res
                query, datecnt = self.replace_with_seconds(entry)
                
                # Valid formula
                if not fullmatch(r'[xyi\d\s+*^()!.,/-]+', sub(funcs_pattern, '', query)): return
                query = query.strip().replace("^", "**")
                if "(" in query and ")" not in query: query += ")"

                # Symbolic formula
                if "x" in query or "y" in query or "i" in query: return self.symbolic_eval(query)

                # Algebric formula
                query = sub("(\d+)!", "factorial(\\1)", query)
                safe = {fn: globals()[fn] for fn in funcs if fn in globals()}
                raw = eval(query, {"__builtins__": None}, safe)
                res = self.fmtnum(raw)

                # Dates and fractions
                if datecnt: return [self.res(self.format_date(entry, raw), entry)]
                if "/" in query: res = self.fraction_result(query, res, safe)

                return [self.res(res, self.for_display(entry))]

            except Exception as e:
                # return self.res(str(e), entry + " >> " + query)
                pass


if __name__ == "__main__":
    FabCalc()
