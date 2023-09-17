import logging

import coloredlogs

import os
# import pygame

from Coach import Coach
from chess_game.chessgame import chessgame as Game
from othello.pytorch.NNet import NNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 1,
    'numEps': 2,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 5,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 100,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
    'display' : False

})

# game = pygame.display.set_mode((800,800))
def main():
    
    
    if args.display:
        pygame.init()
        WIN = pygame.display.set_mode((800,800))
    log.info('Loading %s...', Game.__name__)
    g = Game(8)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()
    log.info ('learn finished')

    # done = False
    # while done==False:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done=True 



if __name__ == "__main__":
    os.environ["TORCH_AUTOGRAD_SHUTDOWN_WAIT_LIMIT"] = "0"
    main()
    log.info ('finish')
