import Bob_game
import pygame
import neat
import pickle
import os

# set up initial game
myDisplay = pygame.display.Info()
winWidth = myDisplay.current_w-4
winHeight = myDisplay.current_h-210
win = pygame.display.set_mode((winWidth, winHeight))

game = Bob_game.Game(win, winWidth, winHeight)

# set initial speed for bob
bob = game.bobs.sprites()[0]
food = []
initspeedx = 35
initspeedy = 25
bob.speedx = initspeedx
bob.speedy = initspeedy


# ------------------------------------
class MyAI:
    def __init__(self):
        pass

    def move_ai(self, net, closestfood):
        output = net.activate((bob.speedx, bob.speedy, closestfood[0], closestfood[1], closestfood[2]))
        decision = output.index(max(output))
        # print("Decision: ", decision)

        if decision == 0:  # Move up
            if bob.speedy > 0:
                bob.speedy *= -1
        elif decision == 1:  # Move down
            if bob.speedy < 0:
                bob.speedy *= -1
        elif decision == 2:  # Move left
            if bob.speedx > 0:
                bob.speedx *= -1
        elif decision == 3:  # Move right
            if bob.speedx < 0:
                bob.speedx *= -1
        else:  # Turn around
            bob.speedx *= -1
            bob.speedy *= -1

    def train_ai(self, genome, config):
        run = True
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            fps = 30
            clock = pygame.time.Clock()
            for i in range(10*fps):
                clock.tick(fps)
                game.loop(bob)
                food = game.find_food(bob)
                closestfood = food[0]
                # print("closest: ", closestfood)
                self.move_ai(net, closestfood)

            genome.fitness = bob.energy
            game.counter += 1

            break

        return False

    def test_ai(self, net):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            fps = 30
            clock = pygame.time.Clock()
            for i in range(20*fps):
                clock.tick(fps)
                game.loop(bob)
                food = game.find_food(bob)
                closestfood = food[0]
                # print("closest: ", closestfood)
                self.move_ai(net, closestfood)


# -------------------------------------

def eval_genomes(genomes, config):

    for i, (genome_id, genome) in enumerate(genomes):
        print("progress...", round(i/len(genomes) * 100), end=" ")
        genome.fitness = 0
        bob.energy = 0
        bob.rect.x = game.bob_startx
        bob.rect.y = game.bob_starty
        bob.speedx = initspeedx
        bob.speedy = initspeedy

        force_quit = ai.train_ai(genome, config)
        if force_quit:
            quit()


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-31')
    # game.counter = 620
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    ai.test_ai(winner_net)


# run main loop
ai = MyAI()

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

run_neat(config)
test_best_network(config)
