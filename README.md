## This plugin for FlowLauncher is an advanced calculator (algebraic and symbolic calculations) using Python eval

After any calculation, just press enter to copy the result to the clipboard

### Integer factorization:

Use *prime(n)* to determine if n is prime:

> `prime(1234567891)` = True

Use *factor(n)* to get the prime factorization of n:

> `factor(123456789)` = 3 · 3 · 3 607 · 3 803

To get the list of divisors of n, use *factors(n)*

> `factors(123456789)` = [3, 3607, 3803]

### Base conversions:

Use simple notations to convert to decimal: 0b for binary, 0o for octal, 0x for hexadecimal:
> `0b1010` = 10, `0xDDA55` = 907861

To specify bases, use suffixes (one letter for starting base and one letter for ending base):

> `1485do` = 2715 (decimal to octal)
> 
> `1010bh` = A (binary to hexadecimal)

### Authorized math functions:
pi, cos, sin, tan, abs, log, log10, log2, exp, sqrt, acos, asin, atan, atan2, ceil,
floor, degrees, radians, trunc, round, factorial, gcd, pow, !

### Unique Identifiers:
You can generate unique IDs by typing:
> `uuid`

You'll get 4 codes:
- `UUID` (standard UUID)
- `ULID` (Same code without dashes)
- `Short-UUID` Same code reencoded in base 62 to be shorter
- `CUID` Identifier using a timestamp to be sortable, encoded in base 36

Press enter to copy one of the generated IDs to the clipboard

### Hashes:
You can enter one of the following keywords to generate a hash:
> `md5 <text>`
> 
> `sha1 <text>`
> 
> `sha256 <text>`
> 
> `sha3_256 <text>`
> 
> `sha3_512 <text>`
> 
> `blake <text>`

### Symbolic calculations:

You can use one these functions and the symbols `x` and `y` to perform symbolic calculations:

> `solve(3x^2+2x+1)`
> 
> `factor(2x^4-3x^2)`
> 
> `integrate(x*log(x))`
> 
> `diff(x*log(x))`
> 
> `expand((x+y)^2)`
> 
> `expand((2+i)*(4-i))`
> 
> `simplify(sin(x)/cos(x))`
> 
> `limit(x^2/exp(x),x,-oo)`
> 
> `expand_trig(sin(x + y))`
> 
> `exp(sin(x)).series(x, 0, 4)`


### Date and time calculations:

You can calculate the delta between dates or add or substract hours, days, week to dates:  

> `now - 1975-04-13`
> 
> `2023-09-27 21:59 + 06:55`
> 
> `2023-09-27 - 1969-07-21`
> 
> `2000-01-01 - 1900-01-01`
> 
> `now + 4w`
> 
> `now + 1w 4h 5m`
> 
> `1969-07-21 + 4d 3h 2m`
> 
> `07:59 + 14:35 + 11:55`


### IP address

Enter this code to get your local and external IP address:

> `myip`


### Colors

Enter a color code (hex or RGB) to display the right color with all informations (name, hex, RGB and HSV values):

> `#dd2266` [pink:   #dd2266    RGB(221, 34, 102)    HSL(338°, 73%, 50%)]
> 
> `122,140,250` [blue light:   #7A8CFA    RGB(122, 140, 250)    HSL(232°, 93%, 73%)]
