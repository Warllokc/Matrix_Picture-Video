import pygame as pg 
import numpy as np 
import pygame.camera

# Defining a Matrix class that generates the scrolling characters:
# Initialize variables, including the font size, the size of the matrix, the characters to use, and the font object to use
class Matrix():
  def __init__(self, app, font_size = 6):
    self.app = app
    self.FONT_SIZE = font_size
    self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
    self.katakana = np.array([chr(int('0x30a0', 16) + i) for i in range (96)] + ['' for i in range(10)])
    self.font = pg.font.Font('font/arial-unicode-ms.ttf', font_size, bold=True)

# Randomly generate the initial matrix of characters, the intervals at which to change the characters, and the speed at which each column moves
    self.matrix = np.random.choice(self.katakana, self.SIZE)
    self.char_intervals = np.random.randint(25, 50, size = self.SIZE)
    self.cols_speed = np.random.randint(100, 500, size = self.SIZE)

# Generate prerendered characters for each color that will be used, so that each character does not need to be rendered each frame
    self.prerendered_chars = self.get_prerendered_chars()

# Create method that capture and returns a frame from the camera object 
  def get_frame(self):
      image = app.cam.get_image()
      image = pg.transform.scale(image, self.app.RES)
      pixel_array = pg.pixelarray.PixelArray(image)
      return pixel_array

# Define methods to get prerendered characters for each character and color
  def get_prerendered_chars(self):
      char_colors = [(0, green, 0) for green in range(256)]
      prerendered_chars = {}
      for char in self.katakana:
          prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
          prerendered_chars.update(prerendered_char)
      return prerendered_chars

# Define a method to run the simulation for each frame
  def run(self):
    frames = pg.time.get_ticks()
    self.change_letters(frames)
    self.shift_column(frames)
    self.draw()

# Define a method to update the matrix and shift the columns
  def shift_column(self, frames):
      num_cols = np.argwhere(frames % self.cols_speed == 0)
      num_cols = num_cols[:, 1]
      num_cols = np.unique(num_cols)
      self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

# Define a method to randomly change some of the characters in the matrix
  def change_letters(self, frames):
    mask = np.argwhere(frames % self.char_intervals ==0)
    new_chars = np.random.choice(self.katakana, mask.shape[0])
    self.matrix[mask[:, 0], mask[:, 1]] = new_chars

# Define a method to draw the characters to the screen
  def draw(self):
    self.image = self.get_frame()
    for y, row in enumerate(self.matrix):
      for x, char in enumerate(row):
          if char:
              pos = x * self.FONT_SIZE, y * self.FONT_SIZE
              _, red, green, blue = pg.Color(self.image[pos])
              if red and green and blue:
                  color = (red + green + blue) // 3
                  color = 220 if 160 < color < 220 else color
                  char = self.prerendered_chars[(char, (0, color, 0))]
                  char.set_alpha(color + 60)
                  self.app.surface.blit(char, pos)


# Defining a MatrixVision class that creates the main application window
class MatrixVision():
  def __init__(self):
    self.RES = self.WIDTH, self.HEIGHT = 1400, 800
    pg.init()
    self.screen = pg.display.set_mode(self.RES)
    self.surface = pg.Surface(self.RES)
    self.clock = pg.time.Clock()
    self.matrix = Matrix(self)

# initialize and start a Pygame camera object to capture video frames from a connected camera
    pygame.camera.init()
    self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    self.cam.start()

# Define a method to draw the Matrix class to the screen
  def draw(self):
    self.surface.fill(pg.Color('black'))
    self.matrix.run()
    self.screen.blit(self.surface,(0,0)) 

# Define a method to run the application
  def run(self):
    while True:
      self.draw()
      [exit() for i in pg.event.get() if i.type == pg.QUIT]
      pg.display.flip()
      self.clock.tick(30)

# The main body of the code: 
# Create an instance of the MatrixVision class and Run the application
if __name__ == '__main__':
    app = MatrixVision()
    app.run()