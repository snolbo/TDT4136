from assignment5 import *
import time


b = create_sudoku_csp("easy.txt")
print "EASY"
start = time.time()
print_sudoku_solution(b.backtracking_search())
print "Time : " + str(time.time() - start)
print "Backtrack calls: " + str(b.backtrack_calls)
print "Backstrack failures: " + str(b.backtrack_failures)
print

b = create_sudoku_csp("medium.txt")
print "MEDIUM"
start = time.time()
print_sudoku_solution(b.backtracking_search())
print "Time : " + str(time.time() - start)
print "Backtrack calls: " + str(b.backtrack_calls)
print "Backstrack failures: " + str(b.backtrack_failures)
print

print "HARD"
b = create_sudoku_csp("hard.txt")
start = time.time()
print_sudoku_solution(b.backtracking_search())
print "Time : " + str(time.time() - start)
print "Backtrack calls: " + str(b.backtrack_calls)
print "Backstrack failures: " + str(b.backtrack_failures)
print


print "VERYAHRD"
b = create_sudoku_csp("veryhard.txt")
start = time.time()
print_sudoku_solution(b.backtracking_search())
print "Time : " + str(time.time() - start)
print "Backtrack calls: " + str(b.backtrack_calls)
print "Backstrack failures: " + str(b.backtrack_failures)



