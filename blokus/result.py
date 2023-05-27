import pygame

# The class has objects that contain piece, piece points, score.
# It has functions to sort the scores
# It has functions to take x arrays and produce final scores depending on the all together values

class Result:

    def __init__(self, piece, points, score):
        self.piece  = piece
        self.points = points
        self.score  = score

    # Sort pieces depending on their score
    def sort_results(list_of_results):
        list_of_results = list_of_results.sort(key=lambda x: x.score, reverse=True)

    # Assign values to pieces depending on their score.
    # If scores are equal, assign same amount of points.
    # Cut rankings down to the maximum of top 20 results that get points.
    def assign_points(list_of_results, strategy_value):
        Result.sort_results(list_of_results)
        while(len(list_of_results) > 20):
            list_of_results.pop()
        i = 10
        k = 0
        last_score = 0
        for result in list_of_results:
            if result.score == last_score:
                k += 0.5
            else:
                k = 0
            last_score = result.score
            result.score = (i + k)*strategy_value
            i -= 0.5

    # Add additional points depending on a size of a piece (size * 2)
    def add_piece_size_points(list_of_results, piece_value):
        for result in list_of_results:
            result.score += result.piece.size*piece_value*2

    # Concatenate 2 lists. Sum up values of the same elements
    def concat_lists(list1, list2):
        not_found_items = []
        for item1 in list1:
            found = True
            for item2 in list2:
                if item1.piece == item2.piece and item1.points == item2.points:
                    item2.score += item1.score
                    found = False
            if(found):
                not_found_items.append(item1)
        return_list = list2 + not_found_items
        return(return_list)

    # Concatenate all the lists, add piece size points and return the TOP1 result in the ranking
    def get_top_move(list_of_lists, piece_size_value):
        final_list = []
        for list in list_of_lists:
            final_list = Result.concat_lists(final_list, list)
        Result.add_piece_size_points(final_list, piece_size_value)
        Result.sort_results(final_list)
        return(final_list[0])
