class View:
    def __init__(self):
        """
        initial all data
        Input: None
        Output: None
        """
        def cross(a, b):
            return [s + t for s in a for t in b]
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = cross(self.rows, self.cols)
        self.row_units = [cross(r, self.cols) for r in self.rows]
        self.column_units = [cross(self.rows, c) for c in self.cols]
        self.square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                             for cs in ('123', '456', '789')]
        self.unitlist = self.row_units + self.column_units + self.square_units
        self.units = dict((s, [u for u in self.unitlist if s in u])
                          for s in self.boxes)
        self.peers = dict(
            (s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)

    def display(self, values):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                          for c in self.cols))
            if r in 'CF':
                print(line)
        return

    def grid_values(self, grid):
        """
        Convert grid into a dict of {square: char} with '123456789' for empties.
        Input: A grid in string form.
        Output: A grid in dictionary form
                Keys: The boxes, e.g., 'A1'
                Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
        """
        chars = []
        digits = '123456789'
        for c in grid:
            if c in digits:
                chars.append(c)
            if c == '.':
                chars.append(digits)
        assert len(chars) == 81
        return dict(zip(self.boxes, chars))

    def eliminate(self, values):
        """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        for box in solved_values:
            digit = values[box]
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(digit, '')
        return values

    def only_choice(self, values):
        """
        Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        for unit in self.unitlist:
            for digit in '123456789':
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    values[dplaces[0]] = digit
        return values

    def reduce_puzzle(self, values):
        """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        solved_values = [box for box in values.keys() if len(values[box]) == 1]
        stalled = False
        while not stalled:
            solved_values_before = len(
                [box for box in values.keys() if len(values[box]) == 1])
            values = self.eliminate(values)
            values = self.only_choice(values)
            solved_values_after = len(
                [box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        values = self.reduce_puzzle(values)
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in self.boxes):
            return values  # Solved!
        n, s = min((len(values[s]), s)
                   for s in self.boxes if len(values[s]) > 1)
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.ssearch(new_sudoku)
            if attempt:
                return attempt


if __name__ == "__main__":
    view = View()

    view.display(view.search(view.grid_values(
        '..3.2.6..9..3.5..1..18.6......1.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))
