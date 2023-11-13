from cell import Cell
from time import sleep
import random

class Maze:

	def __init__(
			self,
			x1,
			y1,
			num_rows,
			num_cols,
			cell_size_x,
			cell_size_y,
			win=None,
			seed=None
		):
		self._x1 = x1
		self._y1 = y1
		self._num_rows = num_rows
		self._num_cols = num_cols
		self._cell_size_x = cell_size_x
		self._cell_size_y = cell_size_y
		self._win = win	
		if seed:
			random.seed(seed)

		self._cells = []
		
		self._create_cells()
		self._break_entrance_and_exit()
		self._break_walls_r(0,0)
		self._reset_cells_visited()

	def _create_cells(self):
		# Oh man....!!!
		# This here seems to copy the cell for an entire row
		# This gives severe trouble later on, because if one element of that row is marekd
		# as visisted, all of them are.
		#self._cells = [[Cell(self._win)] * self._num_rows for row in range(self._num_cols)]


		for i in range(self._num_cols):
			col_cells = []
			for j in range(self._num_rows):
				col_cells.append(Cell(self._win))
			self._cells.append(col_cells)
		
		for i in range(self._num_cols):
			for j in range(self._num_rows):
				c = self._cells[i][j]
				self._draw_cell(i, j)

	def _draw_cell(self, i, j):
		
		if self._win is None:
			return
		
		top_left_x = self._x1 + i * self._cell_size_x
		top_left_y = self._y1 + j * self._cell_size_y
		bottom_right_x = self._x1 + (i + 1) * self._cell_size_x 
		bottom_right_y = self._y1 + (j + 1) * self._cell_size_y

		self._cells[i][j].draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
		self._animate()

	def _animate(self):

		if self._win is None:
			return

		self._win.redraw()
		#sleep(0.0)

	def _break_entrance_and_exit(self):
		entrance = self._cells[0][0]
		entrance.has_top_wall = False
		self._draw_cell(0, 0)

		out = self._cells[self._num_cols-1][self._num_rows-1]
		out.has_bottom_wall = False
		self._draw_cell(self._num_cols-1, self._num_rows-1)

	def _break_walls_r(self, i, j):
		
		self._cells[i][j].visited = True
		while True:
			next_index_list = []

			# determine which cell(s) to visit next
			# left
			if i > 0 and not self._cells[i - 1][j].visited:
				next_index_list.append((i - 1, j))
			# right
			if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
				next_index_list.append((i + 1, j))
			# up
			if j > 0 and not self._cells[i][j - 1].visited:
				next_index_list.append((i, j - 1))
			# down
			if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
				next_index_list.append((i, j + 1))
			# if there is nowhere to go from here
			# just break out
			if len(next_index_list) == 0:
				self._draw_cell(i, j)
				return

			# randomly choose the next direction to go
			direction_index = random.randrange(len(next_index_list))
			next_index = next_index_list[direction_index]
			
			# knock out walls between this cell and the next cell(s)
			# right
			if next_index[0] == i + 1:
				self._cells[i][j].has_right_wall = False
				self._cells[i + 1][j].has_left_wall = False
			# left
			if next_index[0] == i - 1:
				self._cells[i][j].has_left_wall = False
				self._cells[i - 1][j].has_right_wall = False
			# down
			if next_index[1] == j + 1:
				self._cells[i][j].has_bottom_wall = False
				self._cells[i][j + 1].has_top_wall = False
			# up
			if next_index[1] == j - 1:
				self._cells[i][j].has_top_wall = False
				self._cells[i][j - 1].has_bottom_wall = False

			# recursively visit the next cell
			self._break_walls_r(next_index[0], next_index[1])

	def _reset_cells_visited(self):
		for i in range(self._num_cols):
			for j in range(self._num_rows):
				if self._cells[i][j].visited:
					self._cells[i][j].visited = False

	def solve(self):
		res = self.solver_r(i=0, j=0)
		return res

	def solver_r(self, i, j):

		self._animate()
		self._cells[i][j].visited = True
		if self._cells[i][j] == self._cells[self._num_cols-1][self._num_cols-1]:
			return True
		
		# left
		if i > 0 and not self._cells[i - 1][j].has_right_wall and not self._cells[i - 1][j].visited:
			self._cells[i][j].draw_move(self._cells[i-1][j])
			next_cell = self.solver_r(i-1, j)
			if next_cell:
				return True
			self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)

		# right
		if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i+1][j].has_left_wall:
			self._cells[i][j].draw_move(self._cells[i+1][j])
			next_cell = self.solver_r(i+1, j)
			if next_cell:
				return True
			self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
		# up
		if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j-1].has_bottom_wall:
			self._cells[i][j].draw_move(self._cells[i][j-1])
			next_cell = self.solver_r(i, j-1)
			if next_cell:
				return True
			self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
		# down
		if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j+1].has_top_wall:
			self._cells[i][j].draw_move(self._cells[i][j+1])
			next_cell = self.solver_r(i, j+1)
			if next_cell:
				return True
			self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)	

		return False	


			