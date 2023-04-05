import pygame
from point import Point
from mesh import ClothMesh

# define constants
WINDOW_TITLE = "My Simulation"
WINDOW_SIZE = (800, 800)
FPS = 60

# initialize pygame
pygame.init()

# create window
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()

# Game objects
clothMesh = ClothMesh(topLeft=(200, 10), size=(22, 22))

t = pygame.time.get_ticks()
font = pygame.font.SysFont("arial", 20)
# main loop
running = True
while running:
    # set frames per second
    clock.tick(FPS)
    dt = (pygame.time.get_ticks() - t) / 1000.0
    t = pygame.time.get_ticks()

    # handle inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # toggle fullscreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_RETURN:
                if window.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
                    pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
                else:
                    resolutions = pygame.display.list_modes()
                    pygame.display.set_mode(resolutions[1], pygame.FULLSCREEN)
            elif event.key == pygame.K_r:
                clothMesh.reset()
        if pygame.mouse.get_pressed()[0]:
            clothMesh.isMouseDown = True
        else:
            clothMesh.isMouseDown = False

    clothMesh.update()

    # update the window
    pygame.display.flip()
    window.fill((0, 0 ,0))

    text = font.render(f"{round(1/dt)} fps", True, (255, 255, 255))
    window.blit(text, (0, 0))
    text = font.render(f"press R to reset", True, (255, 255, 255))
    window.blit(text, (0, 20))
    

pygame.quit()