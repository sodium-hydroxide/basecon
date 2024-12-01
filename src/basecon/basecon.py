def from_decimal(number: int, base: int) -> list[int]:
    if number == 0:
        return [0]

    out: list[int] = []
    while number != 0:
        out.append(number % base)
        number = number // base
    out = out[::-1]
    return out


def to_decimal(number: list[int], base: int) -> int:
    try:
        assert isinstance(number, list)
        assert isinstance(number[0], int)
    except AssertionError:
        raise TypeError("Invalid number being converted from base %d", base)

    out: int = sum([orig * (base**power) for power, orig in enumerate(number)])
    return out


def conversion(
    number: list[int] | int, base_initial: int, base_final: int
) -> int | list[int]:
    if base_initial == 10 and isinstance(number, int):
        return from_decimal(number, base_final)
    assert not isinstance(number, int)
    if base_final == 10:
        return to_decimal(number, base_initial)
    return from_decimal(to_decimal(number, base_initial), base_final)
