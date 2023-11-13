from cell import Cell
from time import sleep

class Maze:

	def __init__(
			self,
			x1,
			y1,
			num_rows,
			num_cols,
			cell_size_x,
			cell_size_y,
			win=None
		):
		self._x1 = x1
		self._y1 = y1
		self._num_rows = num_rows
		self._num_cols = num_cols
		self._cell_size_x = cell_size_x
		self._cell_size_y = cell_size_y
		self._win = win	
		
		self._create_cells()

	def _create_cells(self):
		self._cells = [[Cell(self._win)] * self.num_cols for row in range(self.num_rows)]
		
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				c = self._cells[i][j]
				self._draw_cell(i, j)

	def _draw_cell(self, i, j):
		
		if self._win is None:
            return
		
		top_left_x = self.x1 + j * self.cell_size_x
		top_left_y = self.y1 + i * self.cell_size_y
		bottom_right_x = self.x1 + (j + 1) * self.cell_size_x 
		bottom_right_y = self.y1 + (i + 1) * self.cell_size_y

		self._cells[i][j].draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
		self._animate()

	def _animate(self):

		if self._win is None:
			return
			
		self._win.redraw()
		sleep(0.05)