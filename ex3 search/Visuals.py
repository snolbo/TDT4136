from PIL import Image, ImageDraw




class ImageCreator:

    COLORDICT = {
        ".": "white",
        "#": "black",
        "A": "red",
        "B": "darkgreen",
        "r": "tan",
        "g": "lawngreen",
        "f": "forestgreen",
        "m": "gray",
        "w": "blue",
        "p": "black",
        "o": "orange",
        "c": "purple"
    }

    last_saved_image_filename = ""
    last_saved_image = None
    padding = 3

    @staticmethod
    def create_image(image_file_name, rows, cols):
        blank_image = Image.new('RGBA', (rows*ImageCreator.padding, cols*ImageCreator.padding), 'white')
        blank_image.save(image_file_name)
        ImageCreator.last_saved_image_filename = image_file_name
        ImageCreator.last_saved_image = blank_image
        return blank_image

    @staticmethod
    def draw_pixels_on_image(coords_tupp_list, cell_type_list, image=None, filename=None):
        coord_len = len(coords_tupp_list)
        color_len = len(cell_type_list)
        if color_len != coord_len:
            print("DIMENTIONS OF COORDS AND CELL TYPES DONT MATCH")
            return

        if filename is None:
            filename = ImageCreator.last_saved_image_filename
        if image is None:
            image = ImageCreator.last_saved_image
        img_draw = ImageDraw.Draw(image)
        for i in range(0, color_len):
            tupp = coords_tupp_list[i]
            x = tupp[0] * ImageCreator.padding
            y = tupp [1] * ImageCreator.padding
            color = ImageCreator.COLORDICT[cell_type_list[i]]
            for ii in range(0, ImageCreator.padding):
                for jj in range(0, ImageCreator.padding):
                    img_draw.point([x+jj, y+ii], color)
        image.save(filename)
        return

    @staticmethod
    def draw_search_results_on_image(coords_tupp_list, symbols_list, image=None, filename=None):
        if filename is None:
            filename = ImageCreator.last_saved_image_filename
        if image is None:
            image = ImageCreator.last_saved_image
        img_draw = ImageDraw.Draw(image)

        img_draw = ImageDraw.Draw(image)
        new_coord = (0, 0)
        color = 0
        for i in range(0, len(coords_tupp_list)):
            color = ImageCreator.COLORDICT[symbols_list[i]]
            tupp = coords_tupp_list[i]
            x = tupp[0] * ImageCreator.padding + (ImageCreator.padding-1)/2
            y = tupp[1] * ImageCreator.padding + (ImageCreator.padding-1)/2
            new_coord = (x,y)
            img_draw.point(new_coord, color)

        image.save(filename)
        return




