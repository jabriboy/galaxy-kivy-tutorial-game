def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing_x = self.vertical_lines_sp * self.width
        offset = index - 0.5

        line_x = central_line_x + (offset * spacing_x) + self.current_offset_x

        return line_x

def get_line_y_from_index(self, index):
    spacing_y = self.horizontal_lines_sp * self.height
    line_y = index * spacing_y - self.current_offset_y

    return line_y

def get_tiles_coodinates(self, tile_x, tile_y):

    tile_y -= self.current_y_loop

    x = self.get_line_x_from_index(tile_x)
    y = self.get_line_y_from_index(tile_y)

    return x, y