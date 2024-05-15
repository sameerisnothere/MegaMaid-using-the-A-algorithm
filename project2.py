import pygame
import sys

# Constants
CELL_SIZE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Pygame initialization
pygame.init()
clock = pygame.time.Clock()

# Function to draw the grid with custom robot image
def draw_grid(screen, grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '-':
                color = WHITE
            elif grid[row][col] == 'd':
                color = GRAY
            elif grid[row][col] == 'v':
                color = GREEN
            else:
                color = RED
                    # Draw the robot image on the grid
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Function to find the closest dirty cell
def find_closest_dirty(pos, grid):
    row, col = pos
    height = len(grid)
    width = len(grid[0])

    def heuristic(r, c):
        # Manhattan distance heuristic
        return abs(row - r) + abs(col - c)

    min_distance = float('inf')
    closest_cell = None
    visited = set()

    # Priority queue for open nodes sorted by f(n) = g(n) + h(n)
    open_nodes = [(heuristic(row, col), row, col)]

    while open_nodes:
        _, r, c = open_nodes.pop(0)
        if grid[r][c] == 'd' or grid[r][c] == 'v':
            return (r, c)
        visited.add((r, c))

        # Generate successors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] != 'x' and (nr, nc) not in visited:
                open_nodes.append((heuristic(nr, nc), nr, nc))
                visited.add((nr, nc))

        # Sort open nodes based on f(n) = g(n) + h(n)
        open_nodes.sort()

    return None

# Function to perform next move
def next_move(vacuum_pos, grid):
    row, col = vacuum_pos
    height = len(grid)
    width = len(grid[0])

    # Function to check if a cell is within bounds and clean
    def is_valid_move(r, c):
        return 0 <= r < height and 0 <= c < width

    # Move towards the closest dirty cell
    dirty_cell = find_closest_dirty(vacuum_pos, grid)
    if dirty_cell:
        d_row, d_col = dirty_cell
        if d_row < row and is_valid_move(row - 1, col):
            if dirty_cell == (row - 1, col):
                return "CLEAN NEXT UP", (row - 1, col)
            return "UP", (row - 1, col)
        elif d_row > row and is_valid_move(row + 1, col):
            if dirty_cell == (row + 1, col):
                return "CLEAN NEXT DOWN", (row + 1, col)
            return "DOWN", (row + 1, col)
        elif d_col < col and is_valid_move(row, col - 1):
            if dirty_cell == (row, col - 1):
                return "CLEAN NEXT LEFT", (row, col - 1)
            return "LEFT", (row, col - 1)
        elif d_col > col and is_valid_move(row, col + 1):
            if dirty_cell == (row, col + 1):
                return "CLEAN NEXT RIGHT", (row, col + 1)
            return "RIGHT", (row, col + 1)
        elif d_col == col and d_row == row: 
            return "CLEAN THIS", (row, col)

    # If no dirty cell found or all adjacent cells are dirty, clean current cell
    return "CLEAN", (row, col)

# Main function
def main():
    # Read initial position
    initial_pos = tuple(map(int, input("Enter initial position (row column): ").strip().split()))
    vacuum_pos = initial_pos

    # Read grid size
    height, width = map(int, input("Enter grid size (height width): ").strip().split())

    # Read the grid
    grid = []
    print("Enter the grid configuration:")
    for _ in range(height):
        row = input().strip()
        grid.append(row)

    initialRow, InitialCol = initial_pos
    grid[initialRow] = grid[initialRow][:InitialCol] + 'b' + grid[initialRow][InitialCol + 1:]

    # Pygame setup
    screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
    pygame.display.set_caption("MegaMaid Cleaning")

    # # Load the custom robot image
    # robot_img = pygame.image.load('robot.jpg')  # Replace 'robot.jpg' with your image file
    # if robot_img:
    #     print("Robot image loaded successfully!")
    # else:
    #     print("Error: Failed to load robot image!")

    # robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))  # Scale the image to fit the cell size


    while True:
        screen.fill(WHITE)

        # Draw the grid
        draw_grid(screen, grid)

        # Update the display
        pygame.display.flip()

        # Handle events
        handle_events()

        # Perform next move
        next_operation, new_pos = next_move(vacuum_pos, grid)
        oldRow, oldCol = vacuum_pos
        grid[oldRow] = grid[oldRow][:oldCol] + '-' + grid[oldRow][oldCol + 1:]
        vacuum_pos = new_pos

        if next_operation == "CLEAN":
            break

        # Update the grid with the new position of the robot
        row, col = new_pos
        if next_operation == "CLEAN NEXT DOWN" or next_operation == "CLEAN NEXT UP" or next_operation == "CLEAN NEXT LEFT" or next_operation == "CLEAN NEXT RIGHT":
            grid[row] = grid[row][:col] + 'v' + grid[row][col + 1:]
        else:
            grid[row] = grid[row][:col] + 'b' + grid[row][col + 1:]

        # Limit frame rate
        clock.tick(2)

if __name__ == "__main__":
    main()
