import random

TOTAL_GAMES_PER_SIM = 500
TOTAL_SIMS = 10000

BASE_BET = 1
MAX_BET = 64

STARTING_BALANCE = 10000

balance_results = []
total_winnings = 0
avg_winnings = 0

# pick a color to bet on (red = even = true, black = odd = false)
def PickColor():
  number = random.randint(0,1)
  #print("Number is: {}".format(number))
  if number == 0:
    return True
  else:
    return False

# populate black color pick status
def UpdateBlack(red):
  if red == True:
    return False
  else:
    return True

# pick a number on the table
def RollNumber():
  return random.randint(0,36)

def SimulateGame():
  current_bet_amount = 1
  bank_balance = STARTING_BALANCE
  final_balance = 0
  current_run = 1
  new_game_flag = True
  win_flag = False
  red_selected = False
  black_selected = False
  red_winner = False
  black_winner = False
  bankrupt = False

  while current_run <= TOTAL_GAMES_PER_SIM and not bankrupt:
    #print("Current run is {}".format(current_run))
    current_run += 1

    if new_game_flag:
      new_game_flag = False
      #place a bet randomly on red (even) or black (odd)
      #print("Picking a new color to bet on")
      red_selected = PickColor()
      black_selected = UpdateBlack(red_selected)
      current_bet_amount = BASE_BET
    else:
      current_bet_amount = current_bet_amount * 2
      if current_bet_amount > MAX_BET:
        # we are going to bet too much, so cut losses
        #print("Over max bet. Resetting bet amount.")
        new_game_flag = True
        continue

    #print("Betting on red: {}".format(red_selected))
    #print("Betting on black: {}".format(black_selected))
    #print("Current bet amount is {}".format(current_bet_amount))
    #print("Current bank balance is {}".format(bank_balance))

    # subtract the bet amount from bank (make sure we have enough money)
    #print("Bank balance after betting is: {}".format(bank_balance))
    if bank_balance - current_bet_amount < 0:
      #print("Ran out of money on run {}".format(current_run))
      final_balance = 0
      final_run = current_run
      bankrupt = True
      continue
    else:
      bank_balance = bank_balance - current_bet_amount

    # pick a number
    winning_number = RollNumber()
    #print("Winning number is: {}".format(winning_number))

    # see if we win or not
    # if the number is a 0, then we definitely did not win
    if winning_number != 0:
      # if number is even we will pretend it is red
      if winning_number % 2 == 0:
        red_winner = True
        #print("Set red winner to true")
      else:
        black_winner = True
        #print("Set black winner to true")

    # if we win, credit account and reset flag
    if red_selected and red_winner:
      #print("We picked red and red won")
      win_flag = True
    if black_selected and black_winner:
      #print("We picked black and black won")
      win_flag = True
    
    if win_flag:
      win_flag = False
      new_game_flag = True
      #print("Bank balance before winning credit: {}".format(bank_balance))
      #print("About to add this much for winning: {}".format(2 * current_bet_amount))
      bank_balance = bank_balance + 2 * current_bet_amount
      #print("Bank balance after winning credit: {}".format(bank_balance))

    # reset winner flags
    red_winner = False
    black_winner = False

    #print()
    #print()
    #print()
  # if we get here, it means we did not run out of money!
  final_balance = bank_balance
  final_run = current_run - 1
  #print("Final balance: {}".format(final_balance))
  #print("Final run: {}".format(final_run))
  return final_balance

def SimulateBatchOfRuns():
  for run in range(0, TOTAL_SIMS):
    final_balance = SimulateGame()
    balance_results.append(final_balance)

def ProcessResults():
  #print("Batch of balance results:")
  #print(balance_results)

  # do some math to figure out if we finished above or below the average
  total_winnings = sum(balance_results)
  avg_winnings = total_winnings / TOTAL_SIMS
  print("Total Winnings from all simulations: {}".format(total_winnings))
  print("Average Winnings per simulation:     {}".format(avg_winnings))

print("Simulating games...")

SimulateBatchOfRuns()
print()

print("Simulated up to this many games per simulation: {}".format(TOTAL_GAMES_PER_SIM))
print("NOTE: Some may early if we run out of money in bank.")
print("Simulated this many simulations: {}".format(TOTAL_SIMS))
print()

print("Processing results...")

ProcessResults()
print()

if avg_winnings > STARTING_BALANCE:
  print("We were profitable!")
else:
  print("We lost money!")
print()





