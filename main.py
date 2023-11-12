from graphics import Window, Point, Line
import random



def main():
	width, height = 1000, 600
	num_points = 50
	lines = []
	for _ in range(num_points):
		p1 = Point(random.randint(0, width), random.randint(0, height))
		p2 = Point(random.randint(0, width), random.randint(0, height))
		lines.append(Line(p1, p2))


	win = Window(width, height)
	for line in lines:
		win.draw_line(line, fill_color='red')
	win.wait_for_close()

if __name__ == "__main__":
	main()