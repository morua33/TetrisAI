GRID_HT = 20

# stats = [(num_of_holes, max_height)]
# def heuristic(heuristic_input):
#     if is_out_of_space(heuristic_input):
#         raise ValueError('We lost the game, there is no place to insert anymore')
    
#     min_idx = -1
#     min_val = float('inf')

#     for i,(num_of_holes,max_ht) in enumerate(heuristic_input):
#         if num_of_holes + max_ht < min_val:
#             min_idx = i
#             min_val = num_of_holes + max_ht
#     return (min_val, min_idx)


#################### https://www.diva-portal.org/smash/get/diva2:815662/FULLTEXT01.pdf ####################
def heuristic(heuristic_input):
    min_idx = -1
    min_val = float('inf')

    for i, heuristic_val in enumerate(heuristic_input):
        if heuristic_val < min_val:
            min_idx = i
            min_val = heuristic_val
    return (min_val, min_idx)



# Returns True if grid has no more room else False
def is_out_of_space(heuristic_input):
    for _,max_ht in heuristic_input:
        if max_ht < GRID_HT:
            return False
    return True