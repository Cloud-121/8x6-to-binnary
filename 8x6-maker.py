import pygame
import base64
import io
import os
from tkinter import filedialog

pygame.init()

win = pygame.display.set_mode((584, 500))
tile_width = 64
tile_height = 64
margin = 8  # space between the boxes
white = (255, 255, 255)
black = (0, 0, 0)
border_width = 2

# Create a list to hold the state of each square
num_columns = 8
num_rows = 6
square_states = [[True] * num_rows for _ in range(num_columns)]

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)
save_button = font.render("Save", True, white)
save_button_rect = save_button.get_rect(centerx=win.get_width() // 2, bottom=win.get_height() - margin)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if save_button_rect.collidepoint(pos):
                # Prompt the user for a filename
                filename = filedialog.asksaveasfilename(defaultextension=".txt")
                if filename:
                    # Encode the image as a base64 string
                    buffer = io.BytesIO()
                    pygame.image.save(win, buffer, "PNG")
                    base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
                    # Write the base64 string to a file
                    with open(filename, "w") as f:
                        f.write(base64_string)

            for col in range(num_columns):
                for row in range(num_rows):
                    rect = pygame.Rect(
                        margin + col * (tile_width + margin),
                        margin + row * (tile_height + margin),
                        tile_width,
                        tile_height,
                    )
                    if rect.collidepoint(pos):
                        # Toggle the state of the clicked square
                        square_states[col][row] = not square_states[col][row]

    x = margin
    for column in range(num_columns):
        y = margin
        for row in range(num_rows):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            # Draw the border rectangle first
            border_rect = pygame.Rect(
                x + border_width // 2,
                y + border_width // 2,
                tile_width - border_width,
                tile_height - border_width,
            )
            pygame.draw.rect(win, black, border_rect, border_width)
            # Then draw the white or black square inside
            if square_states[column][row]:
                pygame.draw.rect(win, black, rect)
                pygame.draw.rect(win, white, border_rect)
            else:
                pygame.draw.rect(win, white, rect)
                pygame.draw.rect(win, black, border_rect)
            y = y + tile_height + margin
        x = x + tile_width + margin

    # Draw the save button
    win.blit(save_button, save_button_rect)

    pygame.display.update()

pygame.quit()