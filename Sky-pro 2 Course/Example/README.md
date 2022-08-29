# SkyPro Python Projects

SkyPro Python Projects are just my onw scripts I write during my learning. 

***

## Short dicription

There're many diffrents script here was written by my kind of simple games, some exemples of working with files and
requests. The repository is going to fill up by new interesting scripts showing inprovement in my skills from month to month. 


## Some examples

***Getting correct word's end***

'''
def get_correct_end(amount, core_word, end_0, end_1, end_2):
    """Функция подбирает правильное окончание слова для разных
    чисел, например: 1 помидор, 2 помидора, 5 помидоров.
    amount - количество, core_word - неизменная часть слова
    end_0, end_1, end_2 - окончания слова для кол-ва 0, 1, 2
    например core_word = помидор, end_0 = 'ов', end_1 = '',
    end_2 = 'а'"""

    amount = amount % 100

    if 10 <= amount <= 19:

        correct_word = core_word + end_0

    else:
        amount = amount % 10

        if 2 <= amount <= 4:
            correct_word = core_word + end_2

        elif amount > 4 or amount == 0:
            correct_word = core_word + end_0

        else:
            correct_word = core_word + end_1

    return correct_word
    '''

***Returning strings by demanded length***

'''    
def get_sliced_str(data_str, width=100, sep=' '):
    """Функция вставляет символы перевода строки '\\n'
    если ширина строки больше width и обнаружен sep
    таким образом на выходе получаем многострочную строку
    вместо однострочной"""

    str_len = 0
    print_str = ''

    for symb in data_str:

        print_str += symb
        str_len += 1

        if str_len > width and symb == sep:

            print_str += '\n'
            str_len = 0

    return print_str
    '''
    
    
    
