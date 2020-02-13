def playerinput(i):
    upleft = '1'
    upmid = '2'
    upright = '3'
    midleft = '4'
    midmid = '5'
    midright = '6'
    botleft = '7'
    botmid = '8'
    botright = '9'
    tri = '   '
    sep = '________|_______|________'
    topblock = f"\t|\t|\t\n {tri}{upleft}{tri}|{tri}{upmid}{tri}|{tri}{upright}"
    midblock = f"\n{sep}\n\t|\t|\t\n {tri}{midleft}{tri}|{tri}{midmid}{tri}|{tri}{midright}"
    botblock = f"\n{sep}\n\t|\t|\t\n {tri}{botleft}{tri}|{tri}{botmid}{tri}|{tri}{botright}\n\t|\t|"
    if 'ye' in i.lower() or 'ok' in i.lower() or 'ready' in i.lower() or 'go' in i.lower():
        print(topblock+midblock+botblock)
        player1=input('Player 1: What is your name?\n ').capitalize()
        player2=input('Player 2: What is your name?\n ').capitalize()
    else: 
        ins = input("Tell me when you're ready\n ")
        playerinput(ins)
    playing = True
    print(f"\n\n\n\n\n{player1} is X's and {player2} is O's.")
    while playing:
        playerchoice=input(f"\n\n{player1}, choose the location of your first X:")
        if '1' in playerchoice:
            upleft='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '2' in playerchoice:
            upmid='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '3' in playerchoice:
            upright='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '4' in playerchoice:
            midleft='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '5' in playerchoice:
            midmid='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '6' in playerchoice:
            midright='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '7' in playerchoice:
            botleft='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '8' in playerchoice:
            botmid='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '9' in playerchoice:
            botright='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        else:
            continue
    playing = True
    while playing:
        playerchoice=input(f"\n\n{player2}, choose the location of your first O:")
        if '1' in playerchoice and upleft not in ['X','O']:
            upleft='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '2' in playerchoice and upmid not in ['X','O']:
            upmid='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '3' in playerchoice and upright not in ['X','O']:
            upright='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '4' in playerchoice and midleft not in ['X','O']:
            midleft='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '5' in playerchoice and midmid not in ['X','O']:
            midmid='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '6' in playerchoice and midright not in ['X','O']:
            midright='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '7' in playerchoice and botleft not in ['X','O']:
            botleft='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '8' in playerchoice and botmid not in ['X','O']:
            botmid='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '9' in playerchoice and botright not in ['X','O']:
            botright='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        else:
            continue
    playing = True
    while playing:
        playerchoice=input(f"\n\n{player1}, choose the location of your next X:")
        if '1' in playerchoice and upleft not in ['X','O']:
            upleft='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '2' in playerchoice and upmid not in ['X','O']:
            upmid='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '3' in playerchoice and upright not in ['X','O']:
            upright='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '4' in playerchoice and midleft not in ['X','O']:
            midleft='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '5' in playerchoice and midmid not in ['X','O']:
            midmid='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '6' in playerchoice and midright not in ['X','O']:
            midright='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '7' in playerchoice and botleft not in ['X','O']:
            botleft='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '8' in playerchoice and botmid not in ['X','O']:
            botmid='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '9' in playerchoice and botright not in ['X','O']:
            botright='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        else:
            continue
    playing = True
    while playing:
        playerchoice=input(f"\n\n{player2}, choose the location of your next O:")
        if '1' in playerchoice and upleft not in ['X','O']:
            upleft='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '2' in playerchoice and upmid not in ['X','O']:
            upmid='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '3' in playerchoice and upright not in ['X','O']:
            upright='O'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '4' in playerchoice and midleft not in ['X','O']:
            midleft='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '5' in playerchoice and midmid not in ['X','O']:
            midmid='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '6' in playerchoice and midright not in ['X','O']:
            midright='O'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '7' in playerchoice and botleft not in ['X','O']:
            botleft='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '8' in playerchoice and botmid not in ['X','O']:
            botmid='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '9' in playerchoice and botright not in ['X','O']:
            botright='O'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        else:
            continue
    playing = True
    while playing:
        playerchoice=input(f"\n\n{player1}, choose the location of your next X:")
        if '1' in playerchoice and upleft not in ['X','O']:
            upleft='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '2' in playerchoice and upmid not in ['X','O']:
            upmid='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '3' in playerchoice and upright not in ['X','O']:
            upright='X'
            topblock = f"      |      |          \n  {upleft}   |  {upmid}   |  {upright}   "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '4' in playerchoice and midleft not in ['X','O']:
            midleft='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '5' in playerchoice and midmid not in ['X','O']:
            midmid='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '6' in playerchoice and midright not in ['X','O']:
            midright='X'
            midblock = f"\n______|______|______    \n      |      |          \n  {midleft}   |  {midmid}   |  {midright}   \n______|______|______"
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '7' in playerchoice and botleft not in ['X','O']:
            botleft='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '8' in playerchoice and botmid not in ['X','O']:
            botmid='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        elif '9' in playerchoice and botright not in ['X','O']:
            botright='X'
            botblock = f"    \n      |      |          \n  {botleft}   |  {botmid}   |  {botright}   \n      |      |    "
            print(topblock+midblock+botblock)
            playing = False
            break
        else:
            continue
    playing = True
    if [topleft,topmid,topright]==['X','X','X']:
        print(f"{player1} wins!")
        playing = False
    elif [midleft,midmid,midright]==['X','X','X']:
        print(f"{player1} wins!")
        playing = False
            

ins=input('Are you ready?')
playerinput(ins)