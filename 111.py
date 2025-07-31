import random
from colorama import init, Fore

init(autoreset=True)

def player_move(stones):
    while True:
        try:
            take = int(input(f"Твоя очередь. В куче {stones} шт. Сколько берешь? (1-3): "))
            if 1 <= take <= 3 and take <= stones:
                return take
            else:
                print("Нельзя взять так много или мало. Попробуй снова.")
        except ValueError:
            print("Нужно ввести число от 1 до 3.")


def computer_move(stones):
    # Оптимальная стратегия: оставить кратное 4
    take = stones % 4
    if take == 0:
        take = random.randint(1, min(3, stones))
    print(f"Компьютер берёт {take} шт.")
    return take

def hello():
    print(Fore.GREEN + "Игра Ним с одной кучей камней. Кто берет последний — выигрывает.")
    print("За ход можно брать от 1 до 3 камней.")

def nim_game():

    stones = random.randint(13, 30)


    while stones > 0:
        # Игрок
        take = player_move(stones)
        stones -= take
        if stones == 0:
            print(Fore.GREEN + "Ты победил!")
            break

        # Компьютер
        take = computer_move(stones)
        stones -= take
        if stones == 0:
            print(Fore.RED + "Компьютер победил!")
            break

    input("Еще раз ?")
    nim_game()

hello()
nim_game()
