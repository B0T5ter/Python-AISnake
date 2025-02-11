import pygame
import random
import numpy as np
import pickle
pygame.init()

# Stałe
WIDTH, HEIGHT = 800, 500
TILE_SIZE = 50
FPS = 10000

currentBerry = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
epsilonaZmina = -1
grafika = True
epsilonChange = True
class QLearningAgent:
    def __init__(self, actions, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.actions = actions 
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}

    def get_state_key(self, state):
        return tuple(state)

    def choose_action(self, state, current_direction):
        state_key = self.get_state_key(state)

        if random.uniform(0, 1) < self.epsilon:
            possible_actions = self.actions.copy()
            if current_direction == (1, 0):
                possible_actions.remove("lewo")
            elif current_direction == (-1, 0):
                possible_actions.remove("prawo")
            elif current_direction == (0, 1):
                possible_actions.remove("góra")
            elif current_direction == (0, -1):
                possible_actions.remove("dół")

            return random.choice(possible_actions)
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = [0] * len(self.actions)

            best_action = self.actions[np.argmax(self.q_table[state_key])]
            if (current_direction == (1, 0) and best_action == "lewo") or \
               (current_direction == (-1, 0) and best_action == "prawo") or \
               (current_direction == (0, 1) and best_action == "góra") or \
               (current_direction == (0, -1) and best_action == "dół"):
                best_action = random.choice([a for a in self.actions if a != best_action])

            return best_action

    def update_q(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = [0] * len(self.actions)

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = [0] * len(self.actions)

        action_index = self.actions.index(action)

        next_action_value = max(self.q_table[next_state_key])

        old_q_value = self.q_table[state_key][action_index]

        new_q_value = old_q_value + self.alpha * (reward + self.gamma * next_action_value - old_q_value)

        self.q_table[state_key][action_index] = new_q_value
class Segment:
    def __init__(self, x, y, color, w=TILE_SIZE):
        self.x, self.y, self.color, self.w = x, y, color, w

class Snake:
    def __init__(self):
        self.body = [Segment(150, 50, (0, 255, 0)), Segment(100, 50, (0, 255, 0)), Segment(50, 50, (0, 255, 0))]
        self.dx, self.dy = 1, 0

    def get_state(self, berry):
        head = self.body[0]

        
        food_dx = (berry.x - head.x) // TILE_SIZE
        food_dy = (berry.y - head.y) // TILE_SIZE

        dist_up = head.y // TILE_SIZE
        dist_down = (HEIGHT - head.y - TILE_SIZE) // TILE_SIZE
        dist_left = head.x // TILE_SIZE
        dist_right = (WIDTH - head.x - TILE_SIZE) // TILE_SIZE

        def is_obstacle(x, y):
            return any(seg.x == x and seg.y == y for seg in self.body)

        obs_up = is_obstacle(head.x, head.y - TILE_SIZE)
        obs_down = is_obstacle(head.x, head.y + TILE_SIZE)
        obs_left = is_obstacle(head.x - TILE_SIZE, head.y)
        obs_right = is_obstacle(head.x + TILE_SIZE, head.y)

        return [
            food_dx, food_dy,  
            dist_up, dist_down, dist_left, dist_right,
            obs_up, obs_down, obs_left, obs_right,
            self.dx, self.dy 
        ]

    def move(self):
        head = self.body[0]
        new_head = Segment(head.x + self.dx * TILE_SIZE, head.y + self.dy * TILE_SIZE, (0, 200, 0))
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail = self.body[-1]
        new_segment = Segment(tail.x, tail.y, (0, 255, 0))
        self.body.append(new_segment)

    def check_collision(self):
        head = self.body[0]

        if any(seg.x == head.x and seg.y == head.y for seg in self.body[1:]):
            return True

        if head.x < 0 or head.x >= WIDTH or head.y < 0 or head.y >= HEIGHT:
            return True

        return False

class Berry:
    def __init__(self, snake):
        self.x, self.y = self.new_position(snake)

    def new_position(self, snake):
        free_positions = [[x * TILE_SIZE, y * TILE_SIZE] for x in range(WIDTH // TILE_SIZE) for y in range(HEIGHT // TILE_SIZE)]
        free_positions = [pos for pos in free_positions if not any(seg.x == pos[0] and seg.y == pos[1] for seg in snake.body)]
        return random.choice(free_positions)

    def respawn(self, snake):
        self.x, self.y = self.new_position(snake)

def reset_game():
    global attempt, currentBerry, berryRecord,reward
    if currentBerry > berryRecord:
        berryRecord = currentBerry
    currentBerry = 0
    attempt += 1
    reward = 0
    snake = Snake()
    berry = Berry(snake)
    return snake, berry

def save_data(table, rekord, proba, filename="game_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump((table, rekord, proba), f)
    print("Dane zapisane!")

def load_data(filename="game_data.pkl"):
    try:
        with open(filename, "rb") as f:
            table, rekord, proba = pickle.load(f)
        print("Dane wczytane!")
        return table, rekord, proba
    except FileNotFoundError:
        print("Plik nie istnieje.")
        return {}, 0, 1
q_table, berryRecord, attempt = load_data()  

def is_moving_towards_food(snake, food):
    old_distance = abs(snake.body[0].x - food.x) + abs(snake.body[0].y - food.y)
    
    new_x = snake.body[0].x + snake.dx * TILE_SIZE
    new_y = snake.body[0].y + snake.dy * TILE_SIZE
    
    new_distance = abs(new_x - food.x) + abs(new_y - food.y)
    
    return new_distance < old_distance

def main():
    global q_table, attempt, berryRecord, currentBerry,reward, grafika, epsilonChange
    agent = QLearningAgent(actions=["góra", "dół", "lewo", "prawo"])
    agent.q_table = q_table
    agent.epsilon = 1
    snake, berry = reset_game()
    
    
    run = True
    while run:
        screen.fill('black')
        reward = 0
        state = snake.get_state(berry)
        current_direction = (snake.dx, snake.dy)
        action = agent.choose_action(state, current_direction)
        
        if action == "góra":
            snake.dx, snake.dy = 0, -1
        elif action == "dół":
            snake.dx, snake.dy = 0, 1
        elif action == "lewo":
            snake.dx, snake.dy = -1, 0
        elif action == "prawo":
            snake.dx, snake.dy = 1, 0

        snake.move()

        if is_moving_towards_food(snake, berry):
            reward += 1
        else:
            reward -= 1

        if snake.body[0].x == berry.x and snake.body[0].y == berry.y:
            snake.grow()
            currentBerry += 1
            berry.respawn(snake)
            reward += 10

        if snake.check_collision():
            reward -= 100 
            if epsilonChange == True:
                if agent.epsilon >= 0.6:
                    epsilonaZmina = -1
                if agent.epsilon <= 0.1:
                    epsilonaZmina = 1
                if epsilonaZmina == -1:
                    agent.epsilon = max(0, agent.epsilon - 0.0001)
                else:
                    agent.epsilon = min(1, agent.epsilon + 0.0001)
            next_state = snake.get_state(berry)
            agent.update_q(state, action, reward, next_state)
            snake, berry = reset_game()
        
        next_state = snake.get_state(berry)
        agent.update_q(state, action, reward, next_state)

        if grafika == True:
            pygame.draw.rect(screen, (255, 0, 0), (berry.x, berry.y, TILE_SIZE, TILE_SIZE))
            for seg in snake.body:
                pygame.draw.rect(screen, seg.color, (seg.x, seg.y, seg.w, seg.w))

        if epsilonChange == True:
            epsCol = (255,255,255)
        else:
            epsCol = (150,150,150)
        attemptText = font.render(f"Proba {attempt}", True, (255, 255, 255))
        screen.blit(attemptText, (10, 10))
        recordText = font.render(f"Rekord {berryRecord}", True, (255, 255, 255))
        screen.blit(recordText, (10, 50))
        currentText = font.render(f"Current {currentBerry}", True, (255, 255, 255))
        screen.blit(currentText, (10, 90))
        epsilonText = font.render(f"Epsilon: {agent.epsilon:.2f}", True, epsCol)
        screen.blit(epsilonText, (10, 130))
        rewardText = font.render(f"Reward: {reward}", True, (255, 255, 255))
        screen.blit(rewardText, (10, 170))
        global FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_data(agent.q_table, berryRecord, attempt)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    FPS = 10
                elif event.key == pygame.K_w:
                    FPS = 10000
                elif event.key == pygame.K_a:
                    agent.epsilon = max(0, agent.epsilon - 0.1)
                elif event.key == pygame.K_d:
                    agent.epsilon = min(1, agent.epsilon + 0.1)
                elif event.key == pygame.K_q:
                    if grafika == True:
                        grafika = False
                    else:
                        grafika = True
                elif event.key == pygame.K_e:
                    if epsilonChange == True:
                        epsilonChange = False
                    else:
                        epsilonChange = True
        if grafika == True or attempt%1000 == 0:
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



if __name__ == "__main__":
    main()
    