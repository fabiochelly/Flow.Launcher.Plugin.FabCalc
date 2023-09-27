# This plugin for FlowLauncher is an advanced calculator (algebric and symbolic calculations) using Python eval

## Fractions:
Use doubles slashes to get results with fractions. Ex: 1//2+3//7 = 13/14

## Integer factorization:
Use factor(n) to get the prime factorization of n. Ex: factor(123456789) = 3 · 3 · 3 607 · 3 803

## Base conversions:
Use simple notations to convert to decimal: 0b for binary, 0o for octal, 0x for hexadecimal.
Ex: 0b1010 = 10, 0xDDA55 = 907861
To specify bases manually, use suffixes (one letter for starting base and one letter for ending base).
Ex: 1485do = 2715 (decimal to octal)
Ex: 1010bh = A (binary to hexadecimal)

## Authorized math functions:
pi, cos, sin, tan, abs, log, log10, log2, exp, sqrt, acos, asin, atan, atan2, ceil,
floor, degrees, radians, trunc, round, factorial, gcd, pow, !

## Unique Identifiers:
You can enter one of the following keywords to generate a unique ID:
`uuid`
`ulid`
`cuid` (identifier using a timestamp to be sortable, in base 36)
`sulid` (short version of ulid converted to base 62)

Press enter to copy the generated ID to the clipboard

## Hashes:
You can enter one of the following keywords to generate a hash:
`md5 <text>`
`sha1 <text>`
`sha256 <text>`
`sha3_256 <text>`
`sha3_512 <text>`
`blake <text>`

## Symbolic calculations:
Prefix your calculations with the symbol `$` to get a symbolic calculation.
Examples:
`$solve(3x^2+2x+1)`
`$factor(2x^4-3x^2)`
`$integrate(x*log(x))`
`$diff(x*log(x))`
`$expand((x+y)^2)`
`$simplify(sin(x)/cos(x))`

## Date and time calculations:

`now - 1975-04-13`
`2023-09-27 21:59 + 06:55`
`2023-09-27 - 1969-07-21`
`2000-01-01 - 1900-01-01`
`now + 4w`
`now + 1w 4h 5m`
`1969-07-21 + 4d 3h 2m`
`07:59 + 14:35 + 11:55`
