from grid import Grid
from constants import Constants


def main():
    print("Ready")
    if Constants.window_side_length % Constants.side_size != 0:
        window_length = Constants.window_side_length // Constants.side_size * Constants.side_size
    else:
        window_length = Constants.window_side_length
    field = Grid(window_side_length=window_length, side_size=Constants.side_size)
    field.place_propagator(row=Constants.side_size // 2, column=Constants.side_size // 2)
    field.draw()
    print("Done")


if __name__ == "__main__":
    main()
