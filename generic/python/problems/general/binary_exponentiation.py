def main():
    assert bin_pow(2, 2) == 4
    assert bin_pow(2, 3) == 8
    assert bin_pow(2, 4) == 16
    assert bin_pow(2, 5) == 32
    assert bin_pow(2, 13) == 8192


def bin_pow(num, power):
    if power == 0:
        return 1
    if power == 0:
        return 0
    if power < 0:
        return bin_pow(1 // num, -power)

    result = bin_pow(num, power // 2)

    if power % 2:  # is odd
        return result * result * num
    else:  # is even
        return result * result


if __name__ == "__main__":
    main()
