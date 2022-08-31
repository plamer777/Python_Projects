"""The unit providing classes for game. A purpose of game
 to answer questions of varying degrees of complexity"""
# ----------------------------------------------------------------------
import string
from random import randint
from datetime import datetime
import csv
import requests
# -----------------------------------------------------------------------


class Question:
    """Game question abstraction.
    Fields:
        text_en - the text of the question in English
        text_ru - the text of the question in Russian
        answer_ru - an answer in Russian
        answer_en - an answer in English
        is_translated - shows if translation was successful
        is_asked - shows if question was asked
        is_right - shows if answer was correct
        tip_used - shows if tip was used
        value - a value depending on the question difficulty
        """

    def __init__(self, text: str, answer: str, value: int):

        self._text_en = text
        self._answer_en = answer
        self._is_translated = False
        self._text_ru = ''
        self._answer_ru = ''
        self._is_asked = False
        self._is_right = False
        self._value = value
        self._tip_used = False

    def get_eng_task(self) -> str:
        """The method returns English version of
        the question."""
        return self._text_en

    def get_ru_task(self) -> str:
        """The method returns Russian version of
        the question."""
        if self._is_translated:

            return self._text_ru

    def get_answer(self) -> tuple:
        """The method returns both Russian and
        English versions of the answer."""
        return self._answer_en, self._answer_ru

    def is_tip_used(self) -> bool:
        """This method returns current tip status"""
        return self._tip_used

    def _set_tip_as_used(self):
        """The private method marks tip as used"""
        self._tip_used = True

    def get_answers_len(self) -> tuple:
        """The method provides a len for both versions
        of the answer."""
        return len(self._answer_en), len(self._answer_ru)

    def was_translated(self) -> bool:
        """The method returns bool value if translation
        was successful or not"""
        return self._is_translated

    def mark_as_translated(self):
        """The method changes translation status of question
        on True"""
        self._is_translated = True

    def set_text_ru(self, text_ru: str):
        """The method sets the value of the "text_ru" field"""
        self._text_ru = text_ru

    def set_answer_ru(self, answer_ru: str):
        """The method sets the value of the "answer_ru" field"""
        self._answer_ru = answer_ru

    def get_tip(self) -> tuple:
        """This method returns both Russian and English
        versions of tip"""
        answer_en, answer_ru = self.get_answer()

        # transformation str type to list
        answer_en = list(answer_en)
        answer_ru = list(answer_ru)

        # The cycle replaces some letters with "*"
        for num in range(len(answer_en) // 2):
            # Indexes taken in random order
            ind_en = randint(0, len(answer_en) - 1)
            ind_ru = randint(0, len(answer_ru) - 1)

            answer_en[ind_en] = '*'
            answer_ru[ind_ru] = '*'

        # Changing tip status
        self._set_tip_as_used()

        return ''.join(answer_en), ''.join(answer_ru)

    def check_answer(self, user_answer: str) -> str:
        """The method serves to check if answer was correct.
        A user answer and correct answer compares in letter by letter way
        If 80 percent of letters are correct then user answer is accepted as
        True"""
        user_answer = user_answer.replace(' ', '')
        answer_en, answer_ru = self.get_answer()

        # Here data type was changed and clean from spaces
        answer_en = list(answer_en.lower().replace(' ', ''))
        answer_ru = list(answer_ru.lower().replace(' ', ''))

        # Here We check is user answer's letters in correct answer
        [answer_en.remove(letter) for letter in user_answer
         if letter in answer_en]
        [answer_ru.remove(letter) for letter in user_answer
         if letter in answer_ru]

        # An accuracy checking. If 80 percent of user answer letters are into
        # correct answer then answer will be marked as correct
        en_len, ru_len = self.get_answers_len()
        accuracy_en = ((en_len - len(answer_en)) / en_len) * 100
        accuracy_ru = ((ru_len - len(answer_ru)) / ru_len) * 100

        if accuracy_ru > 80 or accuracy_en > 80:

            self._mark_answer_as_correct()
            return 'Да, это верный ответ!\n'

        else:
            return (f'К сожалению ответ неверный, '
                    f'правильный ответ: {self.get_answer()[0]}'
                    f'({self.get_answer()[1]})\n')

    def was_correct(self) -> bool:
        """This method returns if answer was right or not"""
        return self._is_right

    def _mark_answer_as_correct(self):
        """The private method marking the answer as correct"""
        self._is_right = True

    def mark_as_asked(self):
        """Marking the question as asked"""
        self._is_asked = True

    def get_value(self) -> int:
        """Returning the question value"""
        return self._value

    def was_asked(self) -> bool:
        """Returning the question status was it asked or not"""
        return self._is_asked


class GameMachine:
    """Game Machine class provides fields and methods
    to run game. The class uses Question class to ask
    questions
    Fields:
        game_amount - planned amount of questions
        is_translate - shows if translation is turned on
        score - total result of whole game
        user_name - stores the name of user
        tips - an integer showing hint amount
        games - a list of instances of Question class
        """

    def __init__(self, amount: int, tips: int):

        self._game_amount: int = amount
        self._is_translate: bool = False
        self._score: int = 0
        self._user_name: str = None
        self._tips: int = tips
        self._games: list = []

    def planned_games_amount(self) -> int:
        """Returns the planned amount of games"""
        return self._game_amount

    def decrease_tips(self):
        """Decreases the number of tips"""
        self._tips -= 1

    def get_tips_amount(self) -> int:
        """Returns current hint's amount"""
        return self._tips

    def set_user_name(self):
        """The method gets username and save it in an appropriate field"""
        user_name = input('Введите свое имя чтобы начать игру: ').capitalize()
        self._user_name = user_name

    def get_user_name(self) -> str:
        """Returns the username"""
        return self._user_name

    def _add_question(self, question: Question):
        """Adds a question to the games list"""
        self._games.append(question)

    def get_questions(self) -> list:
        """The method returns a list of questions"""
        return self._games

    def set_score(self, score):
        """The method store score in an instance's field"""
        self._score = score

    def get_score(self) -> int:
        """This method returns total score of the game"""
        return self._score

    def real_games_amount(self) -> int:
        """Returns total real amount of questions added in the list"""
        return len(self._games)

    def load_game(self, url: str):
        """The method loads json object using url.
        Afterwards the object is used to create Question's class instances
        to fill up a list of games
        Arguments:
            url: The link to api resource"""

        # We use two attempts to fill up a list of games
        for attempt in range(2):
            # The planned games amount is added to url to get
            # demanded list of questions.
            games = self._get_json(f'{url}{self.planned_games_amount()}')

            num = 0
            # A cycle is going on 'till list of games won't reach planned
            # games amount
            while self.real_games_amount() < self.planned_games_amount():

                # The breaker if json object haven't got
                # a planned amount of questions
                if num > len(games) - 1:
                    break

                # Creation of Question class instance
                game = games[num]
                question = self._create_task(game)

                if question:
                    self._add_question(question)

                num += 1

            else:
                print(f'Загрузка прошла успешно!\n{"-" * 50}')
                return
        else:
            print(f'Загружено {self.real_games_amount()} вопросов '
                  f'из {self.planned_games_amount()}')

    @staticmethod
    def _create_task(game: dict) -> Question:
        """This staticmethod creates an instance of Question class from json
        data.
        Arguments:
            game - the dict with appropriate fields
        """
        try:
            text = game['question']
            # Deleting possible html tags from answer
            answer = game['answer'].replace('<i>', '').replace('</i>', '')
            value = game['value'] // 10

            # Deleting any possible punctuation in answer
            answer = answer.translate(str.maketrans('', '', string.punctuation))
            question = Question(text, answer, value)
            return question

        except Exception:

            print('Не удалось загрузить вопрос, пробую следующий')
            return None

    @staticmethod
    def _get_json(url: str) -> list:
        """The staticmethod create json object using url.
        Arguments:
            url - the link to api resource
        """
        request = requests.get(url)

        if request.status_code == 200:

            try:
                game = request.json()
                return game

            except Exception:

                print('Не удалось создать json-объект')
                return []

        else:
            print('Возникла ошибка при обращении к серверу')
            return []

    def translate_questions(self):
        """This method translates question and answer and save results
        filling up text_ru and answer_ru fields"""
        from deep_translator import GoogleTranslator

        try:
            # Creation instance of GoogleTranslator class
            translator = GoogleTranslator(target='ru')
            # The variable is used to translate all questions and answers
            # at once
            total_text = ''

            for game in self.get_questions():
                # Summarizing all English questions and answers
                total_text += game.get_eng_task() + '\n' + \
                              game.get_answer()[0] + '\n'

            # Total text translation and creation of a list of Russian
            # questions and answers
            total_text_ru = translator.translate(total_text)
            total_text_ru = total_text_ru.split('\n')

            num = 0
            for game in self.get_questions():

                # Filling up appropriate fields in the question instances
                game.set_text_ru(total_text_ru[num])
                game.set_answer_ru(total_text_ru[num + 1])
                game.mark_as_translated()

                num += 2

        except Exception:
            print('Не удалось выполнить перевод данных')
            return

    def turn_translation_on(self):
        """The method to turn translation on"""
        self._is_translate = True

    def is_translation_on(self) -> bool:
        """The getter of translation status"""
        return self._is_translate

    def start_game(self):
        """The main game method providing gameplay"""
        # Main game cycle
        for num, game in enumerate(self.get_questions(), 1):

            game.mark_as_asked()

            print(f'Вопрос №{num} - стоимость {game.get_value()} очков\n'
                  f'{game.get_eng_task()}\n')
            # Supportive cycle to provide options like hints and translation
            while True:

                if not self.is_translation_on():
                    print('Для включения перевода введите 1')
                # If translation is turned on and question translated
                # successfully then show translation
                elif game.was_translated():
                    print(f'{game.get_ru_task()}\n')

                if self.get_tips_amount() and not game.is_tip_used():
                    print('Чтобы получить подсказку введите 2')

                user_answer = input().lower()

                if user_answer == '1':
                    # Switching translation on and going to next iteration
                    self.turn_translation_on()
                    continue

                elif user_answer == '2':

                    if self.get_tips_amount():

                        self.decrease_tips()
                        # If there're tips and user entered "2" printing hint
                        print(game.get_tip()[0], game.get_tip()[1])
                        continue
                    else:
                        print('К сожалению подсказки закончились')
                # If user_answer != 1 or 2 then to check an answer and break
                # a second cycle
                else:
                    print(game.check_answer(user_answer))
                    break

    def save_results(self, filename: str):
        """The method serves to save results of current game
        Arguments:
            filename (str): The name of the file where the results are going
            to be saved.
            """
        with open(filename, 'a', encoding='utf-8', newline='') as fout:

            csv_writer = csv.writer(fout)
            csv_writer.writerow(self._calculate_score())

    def _calculate_score(self) -> tuple:
        """The method calculates a score of the game and returns a tuple of
        username, score and current timestamp."""
        score = 0

        for game in self.get_questions():
            # If question was asked and correct then to increase a total
            # score on value of the question
            if game.was_asked() and game.was_correct():
                score += game.get_value()

        self.set_score(score)

        return (self.get_user_name(),
                self.get_score(),
                datetime.now().timestamp())

    def load_results(self, filename: str) -> list:
        """The method serves to load a previous best score.
                Arguments:
                    filename (str): The name of the file where the results
                    are going to be loaded from."""
        try:
            with open(filename, 'r', encoding='utf-8') as fin:

                csv_reader = csv.reader(fin)

                best_score = self._get_best_score(csv_reader)

            return self._format_best_score(best_score)

        except FileNotFoundError:
            print(f'Файл {filename} не найден')
            return []

        except csv.Error:
            print('Не удается загрузить данные из файла')
            return []

    @staticmethod
    def _get_best_score(sequence) -> list:
        """The method serves to get the best score from file stream.
                Arguments:
                    sequence (IO): Opened file to read from or another
                    sequence like list.
                Returns:
                    best_score (list): The best score of previous game with
                    name, score and timestamp.
        """
        best_score = [0, 0, 0]

        for result in sequence:

            if not result:
                continue

            try:
                result[1] = int(result[1]) # a game score
                result[2] = float(result[2]) # a timestamp
                best_score = max(best_score, result, key=lambda x: x[1])

                # If there're a few same scores then to get the newest
                if int(best_score[1]) == int(result[1]):

                    best_score = max(best_score, result, key=lambda x: x[2])

            except IndexError:
                print('Не хватает данных в одной строке')

            except ValueError:
                print('Не удалось преобразовать данные в одной строке')

        return best_score

    @staticmethod
    def _format_best_score(best_score: list) -> list:
        """This static method formats timestamp from best score to get days,
        hours, minutes and seconds past since the record
        Arguments:
            best_score (list): The best score with 3 fields (name, score and
            timestamp)
            """
        # Timedelta object having difference between current moment and time
        # of best score. Index 2 is a timestamp
        duration = datetime.now() - datetime.fromtimestamp(best_score[2])

        days = duration.days
        duration = str(duration)

        # If days != 0 then We need to remove "day" or "days" word from
        # timedelta string
        if days != 0:
            duration = duration.replace(' days, ', ':').replace(' day, ', ':')
            duration = duration.split(':')

        else:
            duration = duration.split(':')
            # If days == 0 then We need to insert 0 in the start of the list
            duration.insert(0, days)
        # Finally We have a list of 4 items (days, hours, minutes, seconds)
        duration[3] = float(duration[3])
        duration = list(map(int, duration))
        # Replacing a timestamp with formatted list
        best_score[2] = duration

        return best_score

    def print_results(self, best_score: list):
        """This method prints results of previous best game and current one.
        Arguments:
            best_score (list): A list with 3 fields (name, score,
            time) formatted by _format_best_score method.
            """
        best_score_time = best_score[2]  # A list with days, hours, etc...

        # In final result We use the biggest time period
        if best_score_time[0] != 0:
            time_ago = f'{best_score_time[0]} дней'

        elif best_score_time[1] != 0:
            time_ago = f'{best_score_time[1]} часов'

        elif best_score_time[2] != 0:
            time_ago = f'{best_score_time[2]} минут'

        else:
            time_ago = f'{best_score_time[3]} секунд'

        print(f'{"-" * 50}\nНу вот, {self.get_user_name()}, игра закончилась\n'
              f'Ваш результат {self.get_score()} очков\nЛучший результат'
              f' {best_score[1]} очков установил {best_score[0]}'
              f' {time_ago} назад.\nВам есть к чему стремиться!')
