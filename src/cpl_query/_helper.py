def is_number(t: type) -> bool:
    return issubclass(t, int) or issubclass(t, float) or issubclass(t, complex)
