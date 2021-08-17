class Shape:
    def __init__(self, shape_coords, zero_zero_location):
        self.shape_coords = shape_coords                # array of coords (the one in main) ex: [(0,0), (0,1), (1,0), (1,1)]
        self.zero_zero_location = zero_zero_location    # where (0,0) actually is on the grid. Ex: (3,2)