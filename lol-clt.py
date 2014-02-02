import optparse
from game_info import LoLGameInfo as LGI

def main():
    """Runs program and handles command line options"""
    option_list = [
        optparse.make_option("-g", "--game",
                    action="store_true", dest="game",
                    help="displays most recent game info for a given summoner"),
        optparse.make_option("-s", "--stats",
                    action="store_true", dest="stats",
                    help="displays stats for a given summoner")
    ]
    p = optparse.OptionParser(description=' Displays LoL game information',
                              prog='lol-clt',
                              version='lol-clt 0.1',
                              option_list=option_list,
                              usage="usage: %prog [option] <summoner>"
    )
    options, arguments = p.parse_args()

    if len(arguments) == 1:
        if options.game:
            info = LGI(arguments[0])
            info.print_current_game_info()
            return  
        if options.stats:
            info = LGI(arguments[0])
            info.print_unranked_summoner_stats()
            return
    p.print_help()  

if __name__ == '__main__':
    main()