def submarine(input_file: str) -> None:
    x: int = 0
    d: int = 0

    with open(input_file) as f:
        for line in f:
            instruction = line.strip().split()[0]
            units = int(line.strip().split()[1])

            if instruction == "forward":
                x += units
            if instruction == "down":
                d += units
            if instruction == "up":
                d -= units

    print(f"Multiplying final horizontal position by final depth gives {x*d}")


if __name__ == "__main__":
    submarine('input')
