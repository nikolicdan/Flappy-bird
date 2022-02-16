import pygame, sys, random, numpy
import matplotlib.pyplot as plt


# =============================================================================
# FUNCTIONS FOR Q-learning
# =============================================================================
def ai_play(x, y):
    if (Q[x][y][1] > Q[x][y][0]):
        return True
    return False


def convert(birdxpos, birdypos, bttm_pipes):
    x = min(376, bttm_pipes.bottomleft[0])
    y = bttm_pipes.bottomleft[1] - birdypos
    return int(x/40), int(y/40)


def Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q):
    if jump:
        Q[x_prev][y_prev][1] = 0.4 * Q[x_prev][y_prev][1] + (0.6) * (
                    reward + 0.9 * max(Q[x_new][y_new][0], Q[x_new][y_new][1]))
    else:
        Q[x_prev][y_prev][0] = 0.4 * Q[x_prev][y_prev][0] + (0.6) * (
                    reward + 0.9 * max(Q[x_new][y_new][0], Q[x_new][y_new][1]))


# =============================================================================
# FUNCTIONS FOR Flappy
# =============================================================================

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 540))
    screen.blit(floor_surface, (floor_x_pos + 376, 540))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 170))

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 624:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 540:
        return False

    return True


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def score_display(game_state):
    if game_state == 'main_game':
        # score
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(190, 60))
        screen.blit(score_surface, score_rect)

        # high score
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(270, 30))
        screen.blit(high_score_surface, high_score_rect)

        # iteration
        #interation_surface = game_font.render(f'Iteration: {int(iteration)}', True, (255, 255, 255))
        #interation_rect = interation_surface.get_rect(center=(85, 30))
        #screen.blit(interation_surface, interation_rect)


"""
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (190, 60))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (190, 500))
        screen.blit(high_score_surface, high_score_rect)
"""

# =============================================================================
# INIT
# =============================================================================

pygame.init()
screen = pygame.display.set_mode((376, 624))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 25)

# Game Variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0
loaded_arr = numpy.loadtxt("Q_table1.txt")
Q = loaded_arr.reshape(
    loaded_arr.shape[0], loaded_arr.shape[1] // 2, 2)
#Q = numpy.zeros((10, 30, 2), dtype=float)

# background
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (376, 624))

# floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (376, 100))
floor_x_pos = 0

# bird
bird_surface = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (40, 28))
bird_rect = bird_surface.get_rect(center=(60, 290))

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1600)
pipe_height = [270, 370, 350, 300, 400]

# pipe
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (65, 400))
pipe_list = []
pipe_list.extend(create_pipe())

# for the first pipe?
counter = 0

# graph
iteration = 0
x = []
y = []
flapp = False

# =============================================================================
# GAME
# =============================================================================
while True:

    # adding background
    screen.blit(bg_surface, (0, 0))

    # q-learning
    x_prev, y_prev = convert(bird_rect.topleft[0], bird_rect.topleft[1], pipe_list[-2])
    jump = ai_play(x_prev, y_prev)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # plotting
            """plt.scatter(x, y)
            plt.xlabel("ITERATION")
            plt.ylabel("SCORE")
            plt.title("Flappy Bird")
            plt.show()"""
            pygame.quit()
            sys.exit()

        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                score = 0
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (60, 290)
                counter=0"""

    if jump:
        bird_movement = -5
        bird_rect.centery += bird_movement
        flapp = True
    if flapp:
        flapp = False

    if game_active:
        # adding bird and moving it
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)
        reward = 15

        # adding pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # q-learning
        #x_new, y_new = convert(bird_rect.topleft[0], bird_rect.topleft[1], pipe_list[-2])
        #Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q)

        # updating score
        for pipe_index in range(0, len(pipe_list), 2):
            if pipe_list[pipe_index].centerx == 60:
                score += 1
            if pipe_list[pipe_index].centerx == 40:
                pipe_list.extend(create_pipe())

        score_display('main_game')

    else:

        # graph
        iteration += 1
        x.append(iteration)
        y.append(score)

        # updating high-score
        high_score = update_score(score, high_score)

        # q-learning
        #reward = -1000
        #Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q)
        #game_active = True

        # init
        score = 0
        pipe_list.clear()
        pipe_list.extend(create_pipe())
        bird_movement = 0
        bird_rect.center = (60, 290)
        counter = 0

    # moving floor/needs to be here to be in frontground
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -376:
        floor_x_pos = 0

    # display-update and clock-tick
    pygame.display.update()
    clock.tick()
