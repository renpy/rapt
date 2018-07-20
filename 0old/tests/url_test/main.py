import pygame
import webbrowser

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
    import android.mixer
except ImportError:
    android = None

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 30

# Color constants.
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)

def main():
    pygame.init()
    if android:
        android.init()
        
        android.mixer.music.load("click.wav")
        android.mixer.music.play(-1)

    # Set the screen size.
    screen = pygame.display.set_mode((480, 800))

    # Map the back button to the escape key.
    if android:
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

    # The color of the screen.
    color = RED

    while True:

        ev = pygame.event.wait()

        # Android-specific: 
        if android:
            if android.check_pause():
                android.wait_for_resume()

        # Draw the screen based on the timer.
        if ev.type == TIMEREVENT:
            screen.fill(color)
            pygame.display.flip()
            android.mixer.periodic()

        # When the touchscreen is pressed, change the color to green. 
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            color = GREEN
            if android:
                android.vibrate(.25)
                print "Open URL Version 2"
                webbrowser.open("http://www.renpy.org/")
            
        # When it's released, change the color to RED.
        elif ev.type == pygame.MOUSEBUTTONUP:
            color = RED

        # When the user hits back, ESCAPE is sent. Handle it and end
        # the game.
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            break
    
# This isn't run on Android.
if __name__ == "__main__":
    main()
    
    
