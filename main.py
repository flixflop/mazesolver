from graphics import Window
from maze import Maze


def main():
    width, height = 1040, 800
    num_rows, num_cols = 30, 30
    offset_x = 20
    offset_y = 20
    cellsize_x = (width - 2 * offset_x) / num_rows
    cellsize_y = (height - 2 * offset_y) / num_cols
    win = Window(width, height)

    

    m = Maze(offset_x, offset_y, num_rows, num_cols, cellsize_x, cellsize_y, win)
    m.solve()

    win.wait_for_close()


if __name__ == "__main__":
	main()