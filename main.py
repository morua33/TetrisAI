import grid
import blocks
import ai
import stats
import csv

# tetris = grid.Grid()
# block = blocks.Blocks()


def write_to_csv(file_name, data_arr):
    with open(file_name, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data_arr)


def three_rules():
    while 1:
        shape_name = block.generate_shape()
        all_shape_coords = block.get_all_shape_coords(shape_name)
        min_shape_coords_idx = min_col_idx = -1
        min_val = float('inf')

        for i,shape_coords in enumerate(all_shape_coords):
            heuristic_input = tetris.insert_wrapper(shape_coords)
            val,col_idx = ai.heuristic(heuristic_input)
            
            if val < min_val:
                min_val = val
                min_shape_coords_idx = i
                min_col_idx = col_idx

        shape_coords = all_shape_coords[min_shape_coords_idx]
        insert_row_idx = tetris.find_row_idx_if_inserted_at_given_col_idx(min_col_idx, shape_coords)
        tetris.insert(insert_row_idx, min_col_idx, shape_coords)
        tetris.destroy_rows_wrapper()
        # print(repr(tetris))
        # print(tetris.get_stats())


for i in range(200):
    try:
        tetris = grid.Grid()
        block = blocks.Blocks()
        three_rules()
    except ValueError:
        pass
    print(i)

write_to_csv('stats.csv', stats.num_rows_destroyed_stats)
print(stats.num_rows_destroyed_stats)

# almost the same code as three_rules()
def one_step_prediction():
    while 1:
        shape_name = block.generate_shape()
        all_shape_coords = block.get_all_shape_coords(shape_name)
        min_shape_coords_idx = min_col_idx = -1
        min_val = float('inf')

        for i,shape_coords in enumerate(all_shape_coords):
            heuristic_input = tetris.insert_wrapper_one_step(shape_coords, block.get_next_shape_names())
            val,col_idx = ai.heuristic(heuristic_input)
            
            if val < min_val:
                min_val = val
                min_shape_coords_idx = i
                min_col_idx = col_idx

        shape_coords = all_shape_coords[min_shape_coords_idx]
        insert_row_idx = tetris.find_row_idx_if_inserted_at_given_col_idx(min_col_idx, shape_coords)
        tetris.insert(insert_row_idx, min_col_idx, shape_coords)
        tetris.destroy_rows_wrapper()
        # print(repr(tetris))
        print(tetris.get_stats())

# one_step_prediction()  


