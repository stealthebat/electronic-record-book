def is_float(num: int) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False
