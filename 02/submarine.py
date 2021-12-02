def submarine(input_file: str) -> None:
    x: int = 0
    d_one: int = 0
    d_two: int = 0
    a: int = 0

    with open(input_file) as f:
        for line in f:
            instruction = line.strip().split()[0]
            units = int(line.strip().split()[1])

            if instruction == "forward":
                x += units
                d_two += a * units
            if instruction == "down":
                d_one += units
                a += units
            if instruction == "up":
                d_one -= units
                a -= units

    print(
        f"Multiplying final horizontal position by final depth gives {x*d_one}"
    )
    print(f"Using the new interpretation, it gives {x*d_two}")


if __name__ == "__main__":
    submarine('input')
