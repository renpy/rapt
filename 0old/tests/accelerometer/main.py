import pygame

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
import android

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 30

def main():
    pygame.init()
    if android:
        android.init()

    # Set the screen size.
    screen = pygame.display.set_mode((480, 800))

    # Map the back button to the escape key.
    if android:
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.accelerometer_enable(True)
        
    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

    font = pygame.font.Font("FreeSans.ttf", 30)

    def text(s, x, y):
        surf = font.render(s, True, (200, 200, 200, 255))
        screen.blit(surf, (x, y))
        
    
    while True:

        ev = pygame.event.wait()

        if android.check_pause():
            android.wait_for_resume()
                
        # Draw the screen based on the timer.
        if ev.type == TIMEREVENT:
            x, y, z = android.accelerometer_reading()

            screen.fill((0, 0, 0, 255))
            
            text("X: %f" % x, 10, 10)
            text("Y: %f" % y, 10, 50)
            text("Z: %f" % z, 10, 90)

            pygame.display.flip()

        # When the user hits back, ESCAPE is sent. Handle it and end
        # the game.
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            break
    
# This isn't run on Android.
if __name__ == "__main__":
    main()
    
    
