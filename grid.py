import shape
import blocks
import stats

block = blocks.Blocks()

class Grid:
    def __init__(self):
        self.HT = 16    # height
        self.WT = 10    # width
        self.grid = [['' for _ in range(self.WT)] for _ in range(self.HT)]   # '' for empty, something in not_used_ids
        self.dct = {}   # unique_id:Shape()
        
        # How to represent the blocks
        self.not_used_ids = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'k9', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9']
        self.used_ids = []
        
        # Statistics
        self.num_blocks_inserted = 0
        self.num_rows_destroyed = 0

    ###################################### Insert related functions ######################################
    # shape_coords represents a shape via array of coordinates. Ex: [(0,0), (0,1), (1,0), (2,0)]
    # returns the number of holes given a certain orientation of a shape (note we are assuming no fancy sliding moves) and tallest height for insertion at every column
    def insert_wrapper(self, shape_coords, insert_below_row_idx=float('inf')):
        heuristic_input = []

        # 1) find width of the shape
        width = self.find_width(shape_coords)

        # 2) find column to insert (currently we are inserting in the column that results in the shape being as low as possible)
        for insert_col_idx in range(self.WT-width+1):    # j is the column index of the left-most portion of the inserted shape

            insert_row_idx = self.find_row_idx_if_inserted_at_given_col_idx(insert_col_idx, shape_coords, insert_below_row_idx)    
            undo_indices,can_insert = self.insert(insert_row_idx, insert_col_idx, shape_coords, '$$')   # random unique_id placeholder
            heuristic_val = (self.rule_one() + self.rule_two() + self.rule_three()) if can_insert else 601  # I know the max heuristic value is 600 bc three rules for every cell
            self.undo_insert(undo_indices)
            heuristic_input.append(heuristic_val)
        
        return heuristic_input
    

    def insert_wrapper_one_step(self, shape_coords, next_shape_names, insert_below_row_idx=float('inf')):
        heuristic_input = []

        # 1) find width of the shape
        width = self.find_width(shape_coords)

        # 2) find column to insert (currently we are inserting in the column that results in the shape being as low as possible)
        for insert_col_idx in range(self.WT-width+1):    # j is the column index of the left-most portion of the inserted shape

            insert_row_idx = self.find_row_idx_if_inserted_at_given_col_idx(insert_col_idx, shape_coords, insert_below_row_idx)    
            undo_indices,can_insert = self.insert(insert_row_idx, insert_col_idx, shape_coords, '&&')   # random unique_id placeholder
            
            if can_insert:
                heuristic_val = self.next_step(next_shape_names)

            else:
                heuristic_val = float('inf')
            
            self.undo_insert(undo_indices)
            heuristic_input.append(heuristic_val)
        
        return heuristic_input


    # Helper function for insert_wrapper_one_step: returns the average heuristic value across all the different next shapes
    def next_step(self, next_shape_names):
        heuristic_values = []
        for shape_name in next_shape_names:
            all_shape_coords = block.get_all_shape_coords(shape_name)
            for shape_coords in all_shape_coords:  # next shape
                heuristic_values.append(sum(self.insert_wrapper(shape_coords)))
        return sum(heuristic_values) / float(len(heuristic_values))


    ###################################### Start: https://www.diva-portal.org/smash/get/diva2:815662/FULLTEXT01.pdf  ######################################
    # Helper function for rule_one(), rule_two(), and rule_three()
    def get_max_heights(self, rule_num):
        max_heights = []
        if rule_num == 1: max_heights.append(-1)
        
        lower_bound = 1 if rule_num == 1 else 0
        upper_bound = self.WT-1 if rule_num == 3 else self.WT

        for j in range(lower_bound, upper_bound):
            for i in range(self.HT-1, -2, -1):
                if i == -1 or self.grid[i][j] != '':
                    max_heights.append(i)
                    break

        if rule_num == 3: max_heights.append(-1)

        return max_heights    


    # Heuristic
    def rule_one(self):
        max_heights = self.get_max_heights(1)
        ans = 0
        for j in range(self.WT-1):
            for i in range(max_heights[j+1]+1):
                if self.grid[i][j] == '':
                    ans += ((i+1)**2)
        return ans

    # Heuristic
    def rule_two(self):
        max_heights = self.get_max_heights(2)
        ans = 0
        for j in range(self.WT):
            for i in range(0, max_heights[j]+1):
                if self.grid[i][j] == '':
                    ans += ((i+1)**3)    # weight the rules
                    # ans += 1
        return ans

    # Heuristic
    def rule_three(self):
        max_heights = self.get_max_heights(3)
        ans = 0
        for j in range(1, self.WT):
            for i in range(max_heights[j-1]+1):
                if self.grid[i][j] == '':
                    ans += ((i+1)**2)
        return ans
    

    ###################################### End: https://www.diva-portal.org/smash/get/diva2:815662/FULLTEXT01.pdf  ######################################


    



    # Heuristic: returns the number of holes from inserting a shape oriented in manner given by shape_coords at insert_row_idx and insert_col_idx
    def num_of_holes(self, shape_coords, insert_row_idx, insert_col_idx):
        holes_cnt = 0
        for r,c in shape_coords:
            for i in range(insert_row_idx+r-1, -1, -1):
                # print('row_idx: ' + str(i) + ' | col_idx: ' + str(insert_col_idx+c) + '\n')
                if i >= self.HT: return float('inf')
                if self.grid[i][insert_col_idx+c] != '': break
                holes_cnt += 1
        return holes_cnt
    

    # Heuristic: tallest index of any part of shape_coords
    def tallest_height(self, shape_coords, insert_row_idx):
        max_ht = float('-inf')
        for r,_ in shape_coords:
            max_ht = max(max_ht, insert_row_idx+r)
        return max_ht


    # Helper function for insert_wrapper: given the shape_coords, returns the width of the shape
    def find_width(self, shape_coords):
        min_j = float('inf'); max_j = float('-inf')
        for _,c in shape_coords:
            min_j = min(min_j, c); max_j = max(max_j, c)
        return max_j - min_j + 1        


    # Helper function for insert_wrapper: no side effects
    def find_row_idx_if_inserted_at_given_col_idx(self, col_idx, shape_coords, insert_below_row_idx=float('inf')):
        insert_below_row_idx = min(insert_below_row_idx, self.HT-1)
        # print('insert_below_row_idx: ' + str(insert_below_row_idx) + '\n')
        max_row_idx = float('-inf')     # when r == 0
        for r,c in shape_coords:
            row_idx = insert_below_row_idx-r
            # print('row_idx: ' + str(row_idx) + '\n')
            while row_idx+r >= 0:
                if self.grid[row_idx+r][col_idx+c] != '':
                    if row_idx+r >= self.HT:
                        max_row_idx = float('inf')  # can't insert at col_idx
                    else:
                        max_row_idx = max(max_row_idx, row_idx+1)
                    break
                elif row_idx+r == 0:
                    max_row_idx = max(max_row_idx, row_idx)
                    break
                row_idx -= 1
        return max_row_idx



    # Helper function for insert_wrapper: given the insert_row_idx, insert_col_idx and shape_coords, do the actual insertion by modifying self.grid, self.dct, and self.used_ids
    #   returns an array of the indices of the cells inserted and whether inserting was successful as a tuple;  ex: [(3,3), (3,4), (4,3), (4,4)]
    def insert(self, insert_row_idx, insert_col_idx, shape_coords, unique_id=None):
        if unique_id == None:
            unique_id = self.not_used_ids.pop()
            self.used_ids.append(unique_id)
            self.num_blocks_inserted += 1
            self.dct[unique_id] = shape.Shape(shape_coords[:], (insert_row_idx, insert_col_idx))

        undo_indices = []
        # print(self.dct[unique_id].shape_coords)
        # print('\n')
        for r,c in shape_coords:
            if insert_row_idx+r >= self.HT or insert_col_idx+c >= self.WT:
                if unique_id == '$$':   # we don't have to insert here
                    return (undo_indices, False)
                else:
                    print(self.get_stats())
                    stats.num_rows_destroyed_stats.append(self.num_rows_destroyed)
                    raise ValueError('We lost the game, there is no place to insert anymore')
            else:
                if self.grid[insert_row_idx+r][insert_col_idx+c] != '':
                    print('We accidentally overwrote an occupied cell.')
                    raise ValueError('We accidentally overwrote an occupied cell.')
                else:
                    self.grid[insert_row_idx+r][insert_col_idx+c] = unique_id
                    undo_indices.append((insert_row_idx+r, insert_col_idx+c))
        return (undo_indices, True)

    
    def undo_insert(self, undo_indices):
        for r,c in undo_indices:
            self.grid[r][c] = ''
        


    ###################################### Destroy Rows related functions ######################################
    # Rows that are completely occupied get destroyed thus shifting down pieces. Keeps doing this until there are no more rows to destroy
    def destroy_rows_wrapper(self):
        filled_row_idx = self.find_filled_row()
        # print('filled_row_idx: ' + str(filled_row_idx) + '\n')
        while filled_row_idx != None:
            # print(repr(self))
            # print("\n\n############################## Destroyed row " + str(filled_row_idx) +  " ##############################\n\n")
            self.destroy_row(filled_row_idx)
            self.shift(filled_row_idx+1)
            self.num_rows_destroyed += 1
            # print(repr(self))
            filled_row_idx = self.find_filled_row()
            
    
    # Helper function for destroy_rows_wrapper that returns the index of the lowest fully occupied row else None
    def find_filled_row(self):
        for i in range(self.HT):
            is_fully_occupied = True
            for j in range(self.WT):
                if self.grid[i][j] == '':
                    is_fully_occupied = False
                    break

            if is_fully_occupied: return i
    

    # Helper function for destroy_rows_wrapper: given the row_idx to destroy, destroy that row and update self.dct accordingly
    def destroy_row(self, row_idx):
        for col_idx in range(self.WT):
            unique_id = self.grid[row_idx][col_idx]
            # shape = self.dct[unique_id]   # might be a naming conflict bc the other file is called shape
            if unique_id == '': continue
            zero_row_idx, zero_col_idx = self.dct[unique_id].zero_zero_location
            # print((zero_row_idx, zero_col_idx), (row_idx, col_idx))
            # print(self.dct[unique_id].shape_coords)
            # print('unique id: ' + str(self.grid[row_idx][col_idx]) + ' | zero_row_idx: ' + str(zero_row_idx) + ' | zero_col_idx: ' + str(zero_col_idx) + ' | row_idx: ' + str(row_idx) + ' | col_idx: ' + str(col_idx) + ' | shape_coords: ' + str(self.dct[unique_id].shape_coords) + '\n')
            self.grid[row_idx][col_idx] = ''
            self.dct[unique_id].shape_coords.remove([row_idx-zero_row_idx, col_idx-zero_col_idx])

            if len(self.dct[unique_id].shape_coords) == 0:
                self.used_ids.remove(unique_id)
                self.not_used_ids.append(unique_id)
            

   

    # Helper function for destroy_rows_wrapper: shifts everything above row_idx (inclusive) down one row
    def shift(self, row_idx):
        for i in range(row_idx, self.HT):
            for j in range(self.WT):
                unique_id = self.grid[i][j]
                if unique_id != '':
                    # modify self.dct
                    zero_row_idx, zero_col_idx = self.dct[unique_id].zero_zero_location
                    self.dct[unique_id].shape_coords.remove([i-zero_row_idx, j-zero_col_idx])
                    self.dct[unique_id].shape_coords.append([i-zero_row_idx-1, j-zero_col_idx])
                
                    # modify self.grid
                    self.grid[i-1][j], self.grid[i][j] = self.grid[i][j], ''
        
                

                



    def get_stats(self):
        return 'num_blocks_inserted: ' + str(self.num_blocks_inserted) + '\nnum_rows_destroyed: ' + str(self.num_rows_destroyed) + '\n'

    def __repr__(self):
        rows_res = []
        for row in self.grid:
            row_res = []
            for char in row:
                if char == '': row_res.append('    ')
                else: row_res.append(' ' + char + ' ')
            rows_res.append('|'.join(row_res))

        rows_res.append(self.used_ids[-1])
        rows_res.reverse()
        return ('\n'.join(rows_res)) + '\n\n'