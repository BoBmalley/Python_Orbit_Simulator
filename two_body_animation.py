import json
import pygame


class TwoBodyView:

    def draw(self):
        pygame.init()
        pygame.display.set_caption("Two Body Simulation")

        screen_size = (1024, 1024)
        planet_a_size = (48, 48)
        planet_b_size = (48, 48)
        center_image_size = (20, 20)

        display_surface = pygame.display.set_mode(screen_size)

        planet_a_picture = pygame.image.load("planet_a.png")
        planet_a_picture = pygame.transform.scale(planet_a_picture, planet_a_size)
        planet_b_picture = pygame.image.load("planet_b.png")
        planet_b_picture = pygame.transform.scale(planet_b_picture, planet_b_size)
        space_picture = pygame.image.load("space.jpg")
        center_picture = pygame.image.load("center.png")
        center_picture = pygame.transform.scale(center_picture, center_image_size)

        clock = pygame.time.Clock()
        clock.tick(60)

        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        play_button_x, play_button_y = 160, 100
        replay_button_x, replay_button_y = 644, 100
        rewind_button_x, rewind_button_y = 402, 100
        button_height, button_width = 220, 60

        font = pygame.font.Font('freesansbold.ttf', 30)

        stop_text = font.render('Stop', True, (255, 255, 255))
        play_text = font.render('Play', True, (255, 255, 255))
        replay_text = font.render('Replay', True, (255, 255, 255))
        rewind_off_text = font.render('Rewind:OFF', True, (255, 255, 255))
        rewind_on_text = font.render('Rewind:ON', True, (255, 255, 255))

        center_screen_value = screen_size[0] / 2
        planet_a_tail_position_value = center_screen_value + planet_a_size[0] / 2
        planet_b_tail_position_value = center_screen_value + planet_b_size[0] / 2

        zoom_value = 100

        with open('positions_log.txt', 'r') as inputfile:
            positions = json.load(inputfile)[0]
        position_number = 0

        is_playing = False
        is_rewind = False

        while True:
            position = positions[position_number]
            display_surface.blit(space_picture, (0, 0))

            display_surface.blit(planet_a_picture,
                                 (center_screen_value + position[0] * zoom_value,
                                  center_screen_value + position[1] * zoom_value))
            display_surface.blit(planet_b_picture,
                                 (center_screen_value + position[2] * zoom_value,
                                  center_screen_value + position[3] * zoom_value))
            if is_playing:
                pygame.draw.circle(space_picture, (102, 153, 255),
                                   (planet_a_tail_position_value + position[0] * zoom_value,
                                    planet_a_tail_position_value + position[1] * zoom_value), 3, 3)
                pygame.draw.circle(space_picture, (255, 102, 255),
                                   (planet_b_tail_position_value + position[2] * zoom_value,
                                    planet_b_tail_position_value + position[3] * zoom_value), 3, 3)
                display_surface.blit(stop_text, (230, 115))
            else:
                display_surface.blit(play_text, (230, 115))

            display_surface.blit(center_picture, (center_screen_value, center_screen_value))
            display_surface.blit(replay_text, (700, 115))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                mouse = pygame.mouse.get_pos()

                if play_button_x <= mouse[0] <= play_button_x + button_height and play_button_y <= mouse[
                    1] <= play_button_y + button_width:
                    pygame.draw.rect(space_picture, color_light,
                                     [play_button_x, play_button_y, button_height, button_width])
                else:
                    pygame.draw.rect(space_picture, color_dark,
                                     [play_button_x, play_button_y, button_height, button_width])

                if replay_button_x <= mouse[0] <= replay_button_x + button_height and replay_button_y <= mouse[
                    1] <= replay_button_y + button_width:
                    pygame.draw.rect(space_picture, color_light,
                                     [replay_button_x, replay_button_y, button_height, button_width])
                else:
                    pygame.draw.rect(space_picture, color_dark,
                                     [replay_button_x, replay_button_y, button_height, button_width])

                if rewind_button_x <= mouse[0] <= rewind_button_x + button_height and rewind_button_y <= mouse[
                    1] <= rewind_button_y + button_width:
                    pygame.draw.rect(space_picture, color_light,
                                     [rewind_button_x, rewind_button_y, button_height, button_width])
                else:
                    pygame.draw.rect(space_picture, color_dark,
                                     [rewind_button_x, rewind_button_y, button_height, button_width])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_x <= mouse[0] <= play_button_x + button_height and play_button_y <= mouse[
                        1] <= play_button_y + button_width:
                        is_playing = not is_playing
                    elif replay_button_x <= mouse[0] <= replay_button_x + button_height and replay_button_y <= mouse[
                        1] <= replay_button_y + button_width:
                        position_number = 0
                        is_playing = False
                        space_picture.fill((255, 255, 255))
                        space_picture = pygame.image.load("space.jpg")
                    elif rewind_button_x <= mouse[0] <= rewind_button_x + button_height and rewind_button_y <= mouse[
                        1] <= rewind_button_y + button_width:
                        is_rewind = not is_rewind
                        is_playing = True
                        pygame.display.update()

            if is_rewind:
                display_surface.blit(rewind_on_text, (430, 115))
            else:
                display_surface.blit(rewind_off_text, (430, 115))

            if is_playing and is_rewind:
                position_number -= 1
                space_picture.fill((255, 255, 255))
                space_picture = pygame.image.load("space.jpg")
                for i in range(position_number):
                    pygame.draw.circle(space_picture, (102, 153, 255),
                                       (planet_a_tail_position_value + positions[i][0] * zoom_value,
                                        planet_a_tail_position_value + positions[i][1] * zoom_value), 3, 3)
                    pygame.draw.circle(space_picture, (255, 102, 255),
                                       (planet_b_tail_position_value + positions[i][2] * zoom_value,
                                        planet_b_tail_position_value + positions[i][3] * zoom_value), 3, 3)
                pygame.draw.rect(space_picture, color_dark, [play_button_x, play_button_y, button_height, button_width])
                pygame.draw.rect(space_picture, color_dark,
                                 [replay_button_x, replay_button_y, button_height, button_width])
                pygame.draw.rect(space_picture, color_dark,
                                 [rewind_button_x, rewind_button_y, button_height, button_width])
                pygame.display.update()
            elif is_playing and not is_rewind:
                position_number += 1

            if position_number == len(positions) - 1 or (position_number == 0 and is_rewind):
                is_playing = False
                is_rewind = False
                position_number = 0
                space_picture.fill((255, 255, 255))
                space_picture = pygame.image.load("space.jpg")
                pygame.draw.rect(space_picture, color_dark, [play_button_x, play_button_y, button_height, button_width])
                pygame.draw.rect(space_picture, color_dark,
                                 [replay_button_x, replay_button_y, button_height, button_width])
                pygame.draw.rect(space_picture, color_dark,
                                 [rewind_button_x, rewind_button_y, button_height, button_width])

            pygame.display.update()


class App:
    def start_simulation(self):
        simulation = TwoBodyView()
        simulation.draw()


app = App()
app.start_simulation()
