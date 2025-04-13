import pygame
import sys

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Library of Infinity")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Grid settings
BASE_GRID_SIZE = 50  # Size of each grid cell
grid_offset_x = 0
grid_offset_y = 0
zoom_level = 1.0
grid_size = BASE_GRID_SIZE * zoom_level 

# Mouse tracking variables
dragging = False
last_mouse_pos = (0, 0)
drag_sensitivity = 0.5

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle mouse events for dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                last_mouse_pos = event.pos
            # Zoom in with mouse wheel up
            elif event.button == 4:  # Mouse wheel up
                # Store cursor position before zoom for centered zooming
                cursor_x, cursor_y = pygame.mouse.get_pos()
                
                # Calculate offset from cursor to grid origin before zoom
                offset_from_cursor_x = (cursor_x - grid_offset_x) / zoom_level
                offset_from_cursor_y = (cursor_y - grid_offset_y) / zoom_level
                
                # Adjust zoom level with limits
                zoom_level = min(3.0, zoom_level * 1.1)
                grid_size = BASE_GRID_SIZE * zoom_level
                
                # Adjust grid offset to zoom toward cursor position
                grid_offset_x = cursor_x - offset_from_cursor_x * zoom_level
                grid_offset_y = cursor_y - offset_from_cursor_y * zoom_level
                
            # Zoom out with mouse wheel down
            elif event.button == 5:  # Mouse wheel down
                # Store cursor position before zoom for centered zooming
                cursor_x, cursor_y = pygame.mouse.get_pos()
                
                # Calculate offset from cursor to grid origin before zoom
                offset_from_cursor_x = (cursor_x - grid_offset_x) / zoom_level
                offset_from_cursor_y = (cursor_y - grid_offset_y) / zoom_level
                
                # Adjust zoom level with limits
                zoom_level = max(0.2, zoom_level / 1.1)
                grid_size = BASE_GRID_SIZE * zoom_level
                
                # Adjust grid offset to zoom toward cursor position
                grid_offset_x = cursor_x - offset_from_cursor_x * zoom_level
                grid_offset_y = cursor_y - offset_from_cursor_y * zoom_level
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Calculate the difference from last position with reduced sensitivity
                dx = (event.pos[0] - last_mouse_pos[0]) * drag_sensitivity
                dy = (event.pos[1] - last_mouse_pos[1]) * drag_sensitivity
                
                # Update grid offset
                grid_offset_x += dx
                grid_offset_y += dy
                
                # Update the last mouse position
                last_mouse_pos = event.pos

        # Keyboard controls for zoom
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                # Zoom in
                zoom_level = min(3.0, zoom_level * 1.1)
                grid_size = BASE_GRID_SIZE * zoom_level
            elif event.key == pygame.K_MINUS:
                # Zoom out
                zoom_level = max(0.2, zoom_level / 1.1)
                grid_size = BASE_GRID_SIZE * zoom_level
    
    # Fill screen with white
    screen.fill(BLACK)
    
    # Draw grid with current zoom level
    # Calculate effective grid size based on zoom
    effective_grid_size = BASE_GRID_SIZE * zoom_level
    
    # Calculate starting positions for grid lines
    start_x = grid_offset_x % effective_grid_size
    start_y = grid_offset_y % effective_grid_size
    
    # Draw vertical lines
    x = start_x
    while x < WIDTH:
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        x += effective_grid_size
    
    # Draw horizontal lines
    y = start_y
    while y < HEIGHT:
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
        y += effective_grid_size
    
    # Draw coordinate indicators
    font = pygame.font.SysFont(None, 24)
    pos_text = f"Grid Offset: ({int(grid_offset_x)}, {int(grid_offset_y)}) | Zoom: {zoom_level:.2f}x"
    text_surface = font.render(pos_text, True, WHITE)
    screen.blit(text_surface, (10, 10))
    
    # Display controls
    controls_text = "Controls: Mouse drag to pan | Mouse wheel to zoom | +/- keys to zoom"
    controls_surface = font.render(controls_text, True, WHITE)
    screen.blit(controls_surface, (10, 40))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()