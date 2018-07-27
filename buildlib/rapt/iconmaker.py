import pygame_sdl2
import os
import plat


class IconMaker(object):

    def __init__(self, directory):

        self.directory = directory

    def scale(self, surf, size):

        while True:
            w, h = surf.get_size()

            if (w == size) and (h == size):
                break

            w = max(w // 2, size)
            h = max(h // 2, size)

            surf = pygame_sdl2.transform.smoothscale(surf, (w, h))

        return surf

    def load_image(self, fn):

        for i in [
                os.path.join(self.directory, fn),
                os.path.join(plat.path("templates"), fn)
                ]:

            if os.path.exists(i):

                print(i)

                surf = pygame_sdl2.image.load(i)
                surf = surf.convert_alpha()
                return surf

        else:
            raise Exception("Could not find {}.".format(fn))

    def load_foreground(self, size):
        rv = self.load_image("android-icon_foreground.png")
        return self.scale(rv, size)

    def load_background(self, size):
        rv = self.load_image("android-icon_background.png")
        return self.scale(rv, size)

    def load_icon(self, size):
        bigsize = int(1.5 * size)
        fg = self.load_foreground(bigsize)
        icon = self.load_background(bigsize)

        icon.blit(fg, (0, 0))

        offset = int(.25 * size)

        icon = icon.subsurface((offset, offset, size, size))

        mask = self.load_image("android-icon_mask.png")
        mask = self.scale(mask, size)

        icon.blit(mask, (0, 0), None, pygame_sdl2.BLEND_RGB_MULT)

        # TODO: Roundrect mask.

        return icon


if __name__ == "__main__":

    pygame_sdl2.display.init()
    pygame_sdl2.display.set_mode((640, 480))
    pygame_sdl2.event.pump()

    im = IconMaker("/home/tom/ab/renpy/the_question")

    surf = im.load_icon(192)

    pygame_sdl2.image.save(surf, "/tmp/icon.png")
