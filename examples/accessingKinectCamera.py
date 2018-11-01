import pykinect2
import pygame
import cv2
import ctypes
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
kinectcam = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)
def draw_color_frame(frame, target_surface):
    target_surface.lock()
    address = kinectcam.surface_as_array(target_surface.get_buffer())
    ctypes.memmove(address, frame.ctypes.data, frame.size)
    del address
    target_surface.unlock()

pygame.init()
frame_surface = pygame.Surface((kinectcam.color_frame_desc.Width, kinectcam.color_frame_desc.Height), 0, 32)
clock = pygame.time.Clock()
pygame.display.set_caption("Kinect View")
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w >> 1, infoObject.current_h >> 1),
                            pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
clock = pygame.time.Clock()

done = False
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        elif event.type == pygame.VIDEORESIZE: # window resized
            screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

    if kinectcam.has_new_color_frame():
        frame = kinectcam.get_last_color_frame()
        draw_color_frame(frame, frame_surface)
        frame = None   
    h_to_w = float(frame_surface.get_height()) / frame_surface.get_width()
    target_height = int(h_to_w * screen.get_width())
    surface_to_draw = pygame.transform.scale(frame_surface, (screen.get_width(), target_height));
    screen.blit(surface_to_draw, (0,0))
    surface_to_draw = None
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
kinectcam.close()
