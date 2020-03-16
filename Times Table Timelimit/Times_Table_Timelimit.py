import multiprocessing
import os
import sys
import time 


def my_input(fileno, q):
    
    sys.stdin = os.fdopen(fileno) 
    q.put(input().strip())

    
def load_answer(timeout):
           
    fn = sys.stdin.fileno() 

    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=my_input, args=(fn, q,)) 
    p2 = multiprocessing.Process(target=time.sleep, args=(timeout,))

    p1.start()
    p2.start()

    while p2.is_alive():
        if not p1.is_alive():
            p2.terminate()
            return (q.get(), False)   
    else:
        p1.terminate()
        return ("", True)
            
            
def my_random():

    from random import randint
    
    t = randint(1,8)
    if t==1: x,y = randint(1,9), randint(0,9)
    elif t==2: x,y = randint(3,9), randint(0,9)
    elif t==3: x,y = randint(1,9), randint(3,9)
    else: x,y = randint(3,9), randint(4,9)
    
    return x,y,bool(randint(0,1))
    

def main_screen():
    
    points_scored = 0                           # number of correct answers
    x = y = 0                    
    ster = True                                 # True->product, False->quotient
    asked = [(x,y,ster)]                        # asked questions
    mistakes = []
    timeout = 5                                 # timelimit in seconds
    number_of_questions = 30                    # number of questions

    for i in range(1,number_of_questions+1):

        os.system("cls" if os.name=="nt" else "clear")

        print("\n   T A B L I C Z K A  M N O Ż E N I A\n   ","="*34, sep="")
        print("   ||"+"*"*i+" "*(30-i)+"||\n")

        while (x,y,ster) in asked: (x,y,ster) = my_random()

        asked.append((x,y,ster))

        if ster:
            print("\n   {0}.    {1} * {2} = ".format(i,x,y), end="")
            correct_answer = str(x*y)
        else:
            print("\n   {0}.    {1} : {2} = ".format(i,x*y,x), end="")
            correct_answer = str(y)

        (answer, timelimit) = load_answer(timeout)

        if not timelimit:
            if answer == correct_answer:
                points_scored += 1
                print('   Dobrze!')
            else:
                print('   Błąd!' + '    -  ' + correct_answer)
                mistakes.append((i,x,y,ster,answer))
        else:
            print("\n   czas minął    -  " + correct_answer)
            mistakes.append((i,x,y,ster,answer))

        time.sleep(1)

    print('\n   Liczba odpowiedzi poprawnych:'+ str(points_scored).rjust(4))
    print('   Liczba odpowiedzi błędnych:'+ str(i-points_scored).rjust(6))
    print()

    for i in mistakes:
        if i[3]:
            print(((str(i[0])+".").rjust(6) + (str(i[1])).rjust(5) +
            " * " + str(i[2]) + " = " + (str(i[1]*i[2])).rjust(2) + 
            ("("+str(i[4])+")").rjust(8)).center(35))
        else:
            print(((str(i[0])+".").rjust(6) + (str(i[1]*i[2])).rjust(5) + 
            " : "+ str(i[1]) + " = " + (str(i[2])).rjust(2) + 
            ("("+str(i[4])+")").rjust(8)).center(35))

    print('\n   Press ENTER')
    input()

    print('   K O N I E C')


if __name__ == "__main__":
    
    main_screen()


