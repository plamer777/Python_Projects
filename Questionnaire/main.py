from classes import GameMachine
# ----------------------------------------------------------------
URL = 'http://jservice.io/api/random?count='
RESULTS = 'results.csv'
# ----------------------------------------------------------------


def main(url: str, results: str):
    """The function creates instance of GameMachine class and runs all the
    game logic
    Arguments:
        url {str} -- a url of the resource with appropriate JSON data
        results {str} -- a file with saved results
        """
    game_machine = GameMachine(5, 3)
    game_machine.load_game(url)
    game_machine.translate_questions()
    game_machine.set_user_name()
    game_machine.start_game()
    game_machine.save_results(results)

    best_score = game_machine.load_results(results)

    game_machine.print_results(best_score)
# ----------------------------------------------------------------


if __name__ == '__main__':
    main(URL, RESULTS)
