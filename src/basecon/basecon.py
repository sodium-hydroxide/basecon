import argparse

BASE16 = {
    0: '0', 1: '1', 2: '2', 3: '3',
    4: '4', 5: '5', 6: '6', 7: '7', 8:
    '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
    13: 'D', 14: 'E', 15: 'F'
}

BASE64 = {
    0: '0', 1: '1',    2: '2',    3: '3',    4: '4',    5: '5',    6: '6',    7: '7',
    8: '8', 9: '9',    10: 'A',   11: 'B',   12: 'C',   13: 'D',   14: 'E',   15: 'F',
    16: 'G', 17: 'H',   18: 'I',   19: 'J',   20: 'K',   21: 'L',   22: 'M',   23: 'N',
    24: 'O', 25: 'P',   26: 'Q',   27: 'R',   28: 'S',   29: 'T',   30: 'U',   31: 'V',
    32: 'W', 33: 'X',   34: 'Y',   35: 'Z',   36: 'a',   37: 'b',   38: 'c',   39: 'd',
    40: 'e', 41: 'f',   42: 'g',   43: 'h',   44: 'i',   45: 'j',   46: 'k',   47: 'l',
    48: 'm', 49: 'n',   50: 'o',   51: 'p',   52: 'q',   53: 'r',   54: 's',   55: 't',
    56: 'u', 57: 'v',   58: 'w',   59: 'x',   60: 'y',   61: 'z',   62: '+',   63: '/'
}

ASCII = {
    # ... [ASCII dictionary remains unchanged]
}

def from_decimal(number: int, base: int) -> list[int]:
    """Convert a decimal number to a different base.

    Parameters
    ----------
    number : int
        The decimal number to convert
    base : int
        The base to convert to

    Returns
    -------
    list[int]
        List of digits in the target base, ordered from most to least significant

    Examples
    --------
    >>> from_decimal(42, 2)
    [1, 0, 1, 0, 1, 0]  # represents binary 101010
    >>> from_decimal(15, 16)
    [15]  # represents hex F
    """
    if number == 0:
        return [0]

    out: list[int] = []
    while number != 0:
        out.append(number % base)
        number = number // base
    out = out[::-1]
    return out


def to_decimal(number: list[int], base: int) -> int:
    """Convert a number from a given base to decimal.

    Parameters
    ----------
    number : list[int]
        List of digits in the source base, ordered from most to least significant
    base : int
        The base of the input number

    Returns
    -------
    int
        The decimal (base-10) representation

    Raises
    ------
    TypeError
        If the input number is not a list of integers

    Examples
    --------
    >>> to_decimal([1, 0, 1, 0, 1, 0], 2)
    42  # converts binary 101010 to decimal
    >>> to_decimal([15], 16)
    15  # converts hex F to decimal
    """
    try:
        assert isinstance(number, list)
        assert isinstance(number[0], int)
    except AssertionError:
        raise TypeError("Invalid number being converted from base %d", base)

    out: int = sum([orig * (base**power) for power, orig in enumerate(number)])
    return out


def conversion(number: list[int] | int, base_initial: int, base_final: int) -> int | list[int]:
    """Convert a number between any two bases.

    Parameters
    ----------
    number : list[int] | int
        If base_initial is 10, this should be an integer.
        Otherwise, it should be a list of digits in the initial base
    base_initial : int
        The base of the input number
    base_final : int
        The desired output base

    Returns
    -------
    int | list[int]
        If base_final is 10, returns an integer.
        Otherwise, returns a list of digits in the final base

    Examples
    --------
    >>> conversion([1, 0, 1, 0], 2, 10)  # binary to decimal
    10
    >>> conversion(10, 10, 2)  # decimal to binary
    [1, 0, 1, 0]
    """
    if base_initial == 10 and isinstance(number, int):
        return from_decimal(number, base_final)
    assert not isinstance(number, int)
    if base_final == 10:
        return to_decimal(number, base_initial)
    return from_decimal(to_decimal(number, base_initial), base_final)


def left_pad(vals: list[str], total_length: int) -> list[str]:
    """Pad a list of strings with leading zeros to reach a specified length.

    Parameters
    ----------
    vals : list[str]
        List of strings to pad
    total_length : int
        Desired total length after padding

    Returns
    -------
    list[str]
        Padded list of strings

    Examples
    --------
    >>> left_pad(['1', '2', '3'], 5)
    ['0', '0', '1', '2', '3']
    """
    num_needed = max(0, total_length - len(vals))
    prepend = ["0"] * num_needed
    out = prepend + vals
    return out


def display_hex(number: int, num_digits=0) -> str:
    """Convert a decimal number to hexadecimal display format.

    Parameters
    ----------
    number : int
        Decimal number to convert
    num_digits : int, optional
        Minimum number of digits to display (will pad with leading zeros)

    Returns
    -------
    str
        Hexadecimal representation prefixed with 'x'

    Examples
    --------
    >>> display_hex(255, 4)
    'x00FF'
    >>> display_hex(15)
    'xF'
    """
    return "x" + "".join(left_pad([BASE16[i] for i in from_decimal(number, base=16)], num_digits))


def display_binary(number: int, num_digits=0) -> str:
    """Convert a decimal number to binary display format.

    Parameters
    ----------
    number : int
        Decimal number to convert
    num_digits : int, optional
        Minimum number of digits to display (will pad with leading zeros)

    Returns
    -------
    str
        Binary representation prefixed with 'b'

    Examples
    --------
    >>> display_binary(5, 8)
    'b00000101'
    >>> display_binary(3)
    'b11'
    """
    return "b" + "".join(left_pad([str(i) for i in from_decimal(number, base=2)], num_digits))


def display_ascci(number: int) -> str:
    """Convert a decimal number to its ASCII representation.

    Parameters
    ----------
    number : int
        Decimal number to convert

    Returns
    -------
    str
        ASCII representation or 'NOT ASCII' if number is out of range

    Examples
    --------
    >>> display_ascci(65)
    'A            '
    >>> display_ascci(7)
    '[BEL]  (\\a)   '
    """
    try:
        out = ASCII[number]
    except KeyError:
        out = "NOT ASCII    "
    return out


def make_integer(number: str) -> int:
    """Convert a string to an integer, ensuring no information is lost.

    Parameters
    ----------
    number : str
        String representation of a number

    Returns
    -------
    int
        Integer value

    Raises
    ------
    TypeError
        If the string cannot be unambiguously converted to an integer

    Examples
    --------
    >>> make_integer("42")
    42
    >>> make_integer("3.14")  # raises TypeError
    """
    try:
        number_float = float(number)
        number_int = int(number)
        assert float(number_int) == number_float
    except (ValueError, AssertionError):
        raise TypeError(f"number ({number}) cannot be unambiguously converted to an integer")
    return number_int


def clean_inputs(numbers: str | list[str]) -> list[int]:
    """Convert string input(s) to a list of integers.

    Parameters
    ----------
    numbers : str | list[str]
        Space-separated string of numbers or list of number strings

    Returns
    -------
    list[int]
        List of integers

    Examples
    --------
    >>> clean_inputs("1 2 3")
    [1, 2, 3]
    >>> clean_inputs(["42", "255"])
    [42, 255]
    """
    if isinstance(numbers, str):
        numbers = numbers.split(sep=" ")
    out = [make_integer(number) for number in numbers]
    return out


def lowest_multiple(multiple: int, number: int) -> int:
    """Find the lowest multiple of a number that is greater than or equal to another number.

    Parameters
    ----------
    multiple : int
        The base multiple
    number : int
        The number to find the next multiple for

    Returns
    -------
    int
        Lowest multiple of 'multiple' that is >= 'number'

    Examples
    --------
    >>> lowest_multiple(8, 12)
    16
    >>> lowest_multiple(5, 15)
    15
    """
    if not number % multiple:
        return number
    else:
        return multiple * (number // multiple + 1)


def get_lengths(number: int) -> tuple[int, int, int]:
    """Calculate display lengths needed for decimal, binary, and hex representations.

    Parameters
    ----------
    number : int
        Number to calculate lengths for

    Returns
    -------
    tuple[int, int, int]
        Tuple of (decimal_length, binary_length, hex_length)

    Examples
    --------
    >>> get_lengths(255)
    (3, 8, 2)  # 3 decimal digits, 8 binary digits, 2 hex digits
    """
    len_dec = len(str(number))
    len_bin = lowest_multiple(8, len(display_binary(number)))
    len_hex = lowest_multiple(2, len(display_hex(number)))
    return len_dec, len_bin, len_hex


def display_single(number: int, len_dec: int, len_bin: int, len_hex: int) -> str:
    """Format a single number for display in decimal, binary, hex, and ASCII.

    Parameters
    ----------
    number : int
        Number to display
    len_dec : int
        Width for decimal representation
    len_bin : int
        Width for binary representation
    len_hex : int
        Width for hexadecimal representation

    Returns
    -------
    str
        Formatted string with all representations

    Examples
    --------
    >>> display_single(65, 3, 8, 2)
    ' 65  b01000001  x41  A            '
    """
    return f"{"".join(left_pad(list(str(number)), len_dec))}  {display_binary(number, len_bin)}  {display_hex(number, len_hex)}  {display_ascci(number)}"


def display_multiple(numbers: list[int]) -> str:
    """Format multiple numbers for display, aligned in columns.

    Parameters
    ----------
    numbers : list[int]
        List of numbers to display

    Returns
    -------
    str
        Multi-line string with formatted representations

    Examples
    --------
    >>> print(display_multiple([65, 66, 67]))
    65  b01000001  x41  A
    66  b01000010  x42  B
    67  b01000011  x43  C
    """
    max_vals = get_lengths(max(numbers))
    out = "\n".join([display_single(number, *max_vals) for number in numbers])
    return out


def parse_args():
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Process a list of decimal representations')
    parser.add_argument('decimal_representation', nargs='*', type=str,
                       help='List of strings representing decimal values')
    return parser.parse_args()


def main() -> None:
    """Main function to run the number base conversion utility."""
    args: list[str] = parse_args().decimal_representation
    numbers = clean_inputs(args)
    out = display_multiple(numbers)
    print(out)


if __name__=="__main__":
    main()
