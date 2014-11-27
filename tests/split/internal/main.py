import pygame

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 30

def main():
    pygame.init()

    info = pygame.display.Info()

    # Set the screen size.
    screen = pygame.display.set_mode((info.current_w, info.current_h))

    # Map the back button to the escape key.
    if android:
        android.init()

    # Use a timer to ensure the Android events get regularly
    # called.
    pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

    im = pygame.image.load(android.assets.open("icon.png"))
    w, h = im.get_size()

    x = -w
    y = -h

    while True:

        ev = pygame.event.wait()

        # Handle application state events.
        if ev.type == pygame.APP_WILLENTERBACKGROUND:
            pygame.time.set_timer(TIMEREVENT, 0)
        elif ev.type == pygame.APP_DIDENTERFOREGROUND:
            screen = pygame.display.set_mode((info.current_w, info.current_h))
            pygame.time.set_timer(TIMEREVENT, 1000 / FPS)
        elif ev.type == pygame.APP_TERMINATING:
            break

        # Draw the screen based on the timer.
        if ev.type == TIMEREVENT:
            screen.fill((0, 0, 0, 0))
            screen.blit(im, (x - w/2, y - h/2))
            pygame.display.flip()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            x, y = ev.pos

        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_APP_BACK:
            break


# This isn't run on Android.
if __name__ == "__main__":
    main()
