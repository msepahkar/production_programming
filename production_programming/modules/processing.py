# -*- coding: utf-8 -*-

from things import part_things


# ===========================================================================
class Processing:
    # ===========================================================================
    @staticmethod
    def put_into_levels(part: part_things.Part):
        # prepare the levels array
        levels = [[part]]

        # put the sub parts into levels and add them to the levels array (recursively)
        for sub_part in part.sub_parts_as_parts:

            # recursion
            sub_part_levels = Processing.put_into_levels(sub_part)

            # add levels of the sub part to the main level
            index = 1
            for level in sub_part_levels:
                while index + 1 > len(levels):
                    levels.append([])
                levels[index] += level
                index += 1

        return levels

