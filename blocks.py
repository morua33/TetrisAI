from random import randint

# Modern tetris so use 7-Bag Randomizer
class Blocks:
    def __init__(self):
        # array of shape_coords
        # https://qph.fs.quoracdn.net/main-qimg-bf707b034d64c955a8f5c1f89d7000aa
        # Note: the ordering from bottom to top and left to right is important for the code to function correctly (bc when we delete a row and shift we traverse in same manner)
        self.shapes = {}
        self.shapes['O'] = [[[0,0], [0,1], [1,0], [1,1]]]
        self.shapes['I'] = [[[0,0], [1,0], [2,0], [3,0]], [[0,0], [0,1], [0,2], [0,3]]]
        self.shapes['J'] = [[[0,0], [0,1], [0,2], [1,0]], [[0,0], [0,1], [1,1], [2,1]], [[0,2], [1,0], [1,1], [1,2]], [[0,0], [1,0], [2,0], [2,1]]]
        self.shapes['L'] = [[[0,0], [0,1], [0,2], [1,2]], [[0,0], [0,1], [1,0], [2,0]], [[0,0], [1,0], [1,1], [1,2]], [[0,1], [1,1], [2,0], [2,1]]]
        self.shapes['T'] = [[[0,0], [0,1], [0,2], [1,1]], [[0,1], [1,0], [1,1], [2,1]], [[0,1], [1,0], [1,1], [1,2]], [[0,0], [1,0], [1,1], [2,0]]]
        self.shapes['S'] = [[[0,0], [0,1], [1,1], [1,2]], [[0,1], [1,0], [1,1], [2,0]]]
        self.shapes['Z'] = [[[0,1], [0,2], [1,0], [1,1]], [[0,0], [1,0], [1,1], [2,1]]]
        self.bag = ['O', 'I', 'J', 'L', 'T', 'S', 'Z']


    def generate_shape(self):
        pop_idx = randint(0, len(self.bag)-1)
        shape_name = self.bag.pop(pop_idx)

        # we have sampled everything so reset bag
        if len(self.bag) == 0:
            self.bag = ['O', 'I', 'J', 'L', 'T', 'S', 'Z']
        return shape_name

    def get_first_shape_coords(self, shape_name):
        return self.shapes[shape_name][0]
    
    def get_all_shape_coords(self, shape_name):
        return self.shapes[shape_name]

    def get_next_shape_names(self):
        return self.bag