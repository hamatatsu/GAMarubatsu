# %% import
import matplotlib.pyplot as plt
import numpy as np

population_num = 100
chromosome_len = 100
value_max = 9


# %% generate
def generate():
  # generate random int 1~9
  population = np.random.randint(1, value_max+1, (population_num, chromosome_len))
  return population


# %% evaluate
def evaluate():
  return 0


# %% selection
def selection():
  return 0


# %% crossover
def crossover():
  return 0


# %% mutation
def mutation():
  return 0


# %% main
def main():
  return 0


# %% testcode
if __name__ == "__main__":
  main()
# %%
