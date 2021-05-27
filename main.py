from grid import Grid


def main():
    print("Ready")
    side_size = 20
    field = Grid(window_side_length=800, side_size=side_size + 1)
    field.place_propagator(row=side_size // 2, column=side_size // 2)
    field.draw()
    print("Done")


if __name__ == "__main__":
    main()
