def calculate_levenshtein_distance_recursively(str1, str2):
    if not str1: return len(str2)
    if not str2: return len(str1)
    return min(
        calculate_levenshtein_distance_recursively(str1[1:], str2[1:]) + (str1[0] != str2[0]),
        calculate_levenshtein_distance_recursively(str1[1:], str2) + 1,
        calculate_levenshtein_distance_recursively(str1, str2[1:]) + 1
    )


def levenshtein(s, t):
    """ From Wikipedia article; Iterative with two matrix rows. """
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


if __name__ == '__main__':
    print(calculate_levenshtein_distance_recursively("abc", "abds"))
    print(levenshtein("abc", "abds"))
