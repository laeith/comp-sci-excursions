# https://leetcode.com/problems/climbing-stairs/

def main():
    print(climb_stairs(5))

    assert 1 == climb_stairs(1)  # 1
    assert 2 == climb_stairs(2)  # 1+1 2
    assert 3 == climb_stairs(3)  # 1+2 2+1 1+1+1
    assert 5 == climb_stairs(4)  # 1+2+1 2+1+1 1+1+1+1 2+2 1+1+2
    assert 8 == climb_stairs(5)


def climb_stairs(n: int) -> int:
    memoized = {}

    def how_many(n):
        if n in memoized:
            return memoized[n]

        if n == 1:
            return 1
        elif n == 2:
            return 2

        # From n - 1 position we can take a 1-step move to get to N
        # From n - 2 position we can take a 2-steps move to get to N
        memoized[n] = how_many(n - 1) + how_many(n - 2)

        return memoized[n]

    return how_many(n)


if __name__ == "__main__":
    main()
