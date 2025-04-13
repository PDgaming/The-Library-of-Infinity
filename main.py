import pygame
import sys

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Library of Infinity")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 170, 255)
AXIS_COLOR = (0, 200, 255)

# Grid settings
BASE_GRID_SIZE = 50  # Size of each grid cell

# Mouse tracking variables
dragging = False
last_mouse_pos = (0, 0)
drag_sensitivity = 1

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Initialize grid offset to center the origin in the middle of the screen
        self.grid_offset_x = WIDTH // 2
        self.grid_offset_y = HEIGHT // 2
        self.zoom_level = 1.0
        self.grid_size = BASE_GRID_SIZE * self.zoom_level
    
    def get_true_origin(self):
        """Calculate the position of the true origin (0,0) on screen"""
        origin_x = self.grid_offset_x
        origin_y = self.grid_offset_y
        return (origin_x, origin_y)
    
    def run(self):
        global WIDTH, HEIGHT, screen
        running = True
        
        # Pre-create bloom surfaces for reuse
        bloom_surfaces = []
        for offset in range(3):
            bloom_alpha = 100 - (offset * 30)
            bloom_color = (*BLUE[:3], bloom_alpha)
            surface = pygame.Surface((1, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(surface, bloom_color, (0, 0), (0, HEIGHT), 1)
            bloom_surfaces.append(surface)
        
        horizontal_bloom_surfaces = []
        for offset in range(3):
            bloom_alpha = 100 - (offset * 30)
            bloom_color = (*BLUE[:3], bloom_alpha)
            surface = pygame.Surface((WIDTH, 1), pygame.SRCALPHA)
            pygame.draw.line(surface, bloom_color, (0, 0), (WIDTH, 0), 1)
            horizontal_bloom_surfaces.append(surface)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Handle window resize events
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.size
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    
                    # Recreate horizontal bloom surfaces for new width
                    horizontal_bloom_surfaces = []
                    for offset in range(3):
                        bloom_alpha = 100 - (offset * 30)
                        bloom_color = (*BLUE[:3], bloom_alpha)
                        surface = pygame.Surface((WIDTH, 1), pygame.SRCALPHA)
                        pygame.draw.line(surface, bloom_color, (0, 0), (WIDTH, 0), 1)
                        horizontal_bloom_surfaces.append(surface)
                    
                    # Recreate vertical bloom surfaces for new height
                    bloom_surfaces = []
                    for offset in range(3):
                        bloom_alpha = 100 - (offset * 30)
                        bloom_color = (*BLUE[:3], bloom_alpha)
                        surface = pygame.Surface((1, HEIGHT), pygame.SRCALPHA)
                        pygame.draw.line(surface, bloom_color, (0, 0), (0, HEIGHT), 1)
                        bloom_surfaces.append(surface)
                    
                # Handle mouse events for dragging
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:  # Left mouse button
                        self.dragging = True
                        self.last_mouse_pos = event.pos
                    # Zoom in with mouse wheel up
                    elif event.button == 4:  # Mouse wheel up
                        # Store cursor position before zoom for centered zooming
                        cursor_x, cursor_y = pygame.mouse.get_pos()
                        
                        # Calculate offset from cursor to grid origin before zoom
                        offset_from_cursor_x = (cursor_x - self.grid_offset_x) / self.zoom_level
                        offset_from_cursor_y = (cursor_y - self.grid_offset_y) / self.zoom_level
                        
                        # Adjust zoom level with limits
                        self.zoom_level = min(3.0, self.zoom_level * 1.1)
                        self.grid_size = BASE_GRID_SIZE * self.zoom_level
                        
                        # Adjust grid offset to zoom toward cursor position
                        self.grid_offset_x = cursor_x - offset_from_cursor_x * self.zoom_level
                        self.grid_offset_y = cursor_y - offset_from_cursor_y * self.zoom_level
                        
                    # Zoom out with mouse wheel down
                    elif event.button == 5:  # Mouse wheel down
                        # Store cursor position before zoom for centered zooming
                        cursor_x, cursor_y = pygame.mouse.get_pos()
                        
                        # Calculate offset from cursor to grid origin before zoom
                        offset_from_cursor_x = (cursor_x - self.grid_offset_x) / self.zoom_level
                        offset_from_cursor_y = (cursor_y - self.grid_offset_y) / self.zoom_level
                        
                        # Adjust zoom level with limits
                        self.zoom_level = max(0.2, self.zoom_level / 1.1)
                        self.grid_size = BASE_GRID_SIZE * self.zoom_level
                        
                        # Adjust grid offset to zoom toward cursor position
                        self.grid_offset_x = cursor_x - offset_from_cursor_x * self.zoom_level
                        self.grid_offset_y = cursor_y - offset_from_cursor_y * self.zoom_level
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:  # Left mouse button
                        self.dragging = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        # Calculate the difference from last position with reduced sensitivity
                        dx = (event.pos[0] - self.last_mouse_pos[0]) * drag_sensitivity
                        dy = (event.pos[1] - self.last_mouse_pos[1]) * drag_sensitivity
                        
                        # Update grid offset
                        self.grid_offset_x += dx
                        self.grid_offset_y += dy
                        
                        # Update the last mouse position
                        self.last_mouse_pos = event.pos
            
            # Fill screen with white
            screen.fill(BLACK)
            
            # Draw grid with current zoom level
            # Calculate effective grid size based on zoom
            effective_grid_size = BASE_GRID_SIZE * self.zoom_level
            
            # Calculate starting positions for grid lines
            start_x = self.grid_offset_x % effective_grid_size
            start_y = self.grid_offset_y % effective_grid_size

            # Get the true origin position
            origin_x, origin_y = self.get_true_origin()
            
            # Draw vertical lines with optimized bloom
            x = start_x - effective_grid_size  # Start one grid cell outside view
            while x < WIDTH + effective_grid_size:  # End one grid cell outside view
                # Use pre-created bloom surfaces
                for i, surface in enumerate(bloom_surfaces):
                    screen.blit(surface, (x + i, 0))
                
                # Draw main line
                if abs(x - origin_x) < effective_grid_size / 2:
                    pygame.draw.line(screen, AXIS_COLOR, (x, 0), (x, HEIGHT), 3)
                else:
                    pygame.draw.line(screen, LIGHT_BLUE, (x, 0), (x, HEIGHT), 1)
                
                # Limit number of cells when zoomed out
                max_lines = 100
                if WIDTH / effective_grid_size > max_lines:
                    # Skip some lines
                    step = int(WIDTH / (effective_grid_size * max_lines)) + 1
                    x += effective_grid_size * step
                else:
                    x += effective_grid_size
            
            # Draw horizontal lines with optimized bloom
            y = start_y
            while y < HEIGHT:
                # Use pre-created bloom surfaces
                for i, surface in enumerate(horizontal_bloom_surfaces):
                    screen.blit(surface, (0, y + i))
                
                # Draw main line
                if abs(y - origin_y) < effective_grid_size / 2:
                    pygame.draw.line(screen, AXIS_COLOR, (0, y), (WIDTH, y), 3)
                else:
                    pygame.draw.line(screen, LIGHT_BLUE, (0, y), (WIDTH, y), 1)
                y += effective_grid_size
            
            # Draw the origin point with circle
            origin_radius = 5 * self.zoom_level  # Scale with zoom
            pygame.draw.circle(screen, WHITE, (origin_x, origin_y), origin_radius)
            
            # Draw labels for the origin
            font = pygame.font.SysFont(None, 20)
            origin_label = font.render("(0,0)", True, WHITE)
            screen.blit(origin_label, (origin_x + origin_radius + 5, origin_y - 20))
            
            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()