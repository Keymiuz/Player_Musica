import pygame
from mutagen.mp3 import MP3
import os

# Inicialize pygame
pygame.init()
pygame.mixer.init()

# Defina cores
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (40, 40, 40)
ACTIVE_BUTTON_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Crie a tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Player")

# Defina a lista de músicas e o índice da música atual
songs = []
current_song_index = -1

# Defina funções para reproduzir, pausar, pular e adicionar músicas


def play_song(index):
    global current_song_index
    if index >= len(songs):
        return
    pygame.mixer.music.load(songs[index]["path"])
    pygame.mixer.music.play()
    current_song_index = index


def pause_song():
    pygame.mixer.music.pause()


def skip_song(direction):
    global current_song_index
    if current_song_index == -1:
        return
    new_index = current_song_index + direction
    if new_index < 0 or new_index >= len(songs):
        return
    play_song(new_index)


def add_song(file_path):
    try:
        # Extract song info using mutagen
        mp3 = MP3(file_path)
        length = mp3.info.length
        # Add song to the list
        songs.append({"path": file_path, "length": length})
    except Exception as e:
        print(f"Error adding song: {e}")


# Adicionar algumas músicas mp3 diretamente no código
add_song("musics/SlowDancing.mp3")
# ... adicione mais músicas ...

# Definir posições dos botões
play_button = pygame.Rect((screen_width - 200) // 2,
                          screen_height - 60, 50, 50)
pause_button = pygame.Rect((screen_width - 200) //
                           2 + 75, screen_height - 60, 50, 50)
skip_forward_button = pygame.Rect(
    (screen_width - 200) // 2 + 150, screen_height - 60, 50, 50)
skip_backward_button = pygame.Rect(
    (screen_width - 200) // 2 - 75, screen_height - 60, 50, 50)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                play_song(current_song_index)
            elif pause_button.collidepoint(event.pos):
                pause_song()
            elif skip_forward_button.collidepoint(event.pos):
                skip_song(1)
            elif skip_backward_button.collidepoint(event.pos):
                skip_song(-1)

    # Preenche a tela com a cor de fundo
    screen.fill(BACKGROUND_COLOR)

    if current_song_index != -1:
        current_song = songs[current_song_index]
        song_info = f"Reproduzindo: {os.path.basename(current_song['path'])} ({current_song['length']:.2f} segundos)"
        font = pygame.font.SysFont("Arial", 20)
        song_info_surface = font.render(song_info, True, TEXT_COLOR)
        screen.blit(song_info_surface, (50, screen_height - 50))

    # Desenha os botões
    def draw_button(rect, color): return pygame.draw.rect(screen, color, rect)

    draw_button(play_button, BUTTON_COLOR if pygame.mixer.music.get_busy()
                else ACTIVE_BUTTON_COLOR)
    draw_button(pause_button, BUTTON_COLOR)
    draw_button(skip_forward_button, BUTTON_COLOR)
    draw_button(skip_backward_button, BUTTON_COLOR)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
