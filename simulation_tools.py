import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os

#pca
from sklearn import datasets, decomposition
from sklearn.decomposition import PCA

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def random_genotype(n):
  return [random.uniform(-10, 10) for i in range(n)]


def fitness(optimal_genotype, genotype):
    if len(optimal_genotype) != len(genotype):
        raise ValueError("Długość wektorów musi być taka sama.")
    suma_kwadratow_roznicy = sum((a - b)**2 for a, b in zip(optimal_genotype, genotype))
    fitness_value = math.sqrt(suma_kwadratow_roznicy)
    return fitness_value


def mutation(mi, genotype, strenght):
  if np.random.random() < mi:
    p = np.random.normal(loc=0, scale=strenght)
    genotype += p
  return genotype


def calculate_optimal_genotype(mi, genotype, strenght, n):
  p = np.random.normal(loc=0.2, scale=strenght, size=n)
  genotype += p
  return genotype

def children_roullete(fitness, max_fitness):
  exponent = (max_fitness - fitness)/15
  l = np.exp(exponent)
  children_amount = np.random.poisson(lam=l)
  #if children_amount > 3:
  #  return 3
  #else:
  return children_amount

# zmienić z liniowej
def calculate_max_fitness(population):
  return max(25 - population * 0.04, 2)


def create_plot(values, time, subfolder_path, data_type):
  
  life = {'x':[], 'y':[]}
  fig, ax = plt.subplots(figsize=(10, 7))
  
  def update(frame):
      ax.clear()
      life['x'].append(frame)
      life['y'].append(values[frame])
      ax.plot(life['x'], life['y'], linestyle='-', linewidth=2, color='lightpink')
      
      if data_type == 'population':
        ax.set_title(f'Liczebność populacji w pokoleniu {str(frame)}')
        ax.set_xlabel('Pokolenie')
        ax.set_ylabel('Populacja')
        
      elif data_type == 'fitness':
        ax.set_title(f'Średni fitness w pokoleniu {str(frame)}')
        ax.set_xlabel('Pokolenie')
        ax.set_ylabel('Fitness')
      ax.tick_params(axis='x')
      ax.set_ylim(0, 1.15 * max(values))
      ax.set_xlim(0, time)
  frames = range(time+1)
  animation = FuncAnimation(fig, update, frames=frames, interval=500)
  animation.save(os.path.join(subfolder_path, f'{data_type}.gif'), writer='pillow')
  fig.savefig(os.path.join(subfolder_path, f'{data_type}_final.jpg'))


def pca(df, n_of_components=2):
  scaler = StandardScaler()
  scaled_data = scaler.fit_transform(df)
  # Wykonanie PCA
  pca = PCA(n_of_components)
  pca_result = pca.fit_transform(scaled_data)
  # Konwersja wyników PCA do DataFrame
  pca_df = pd.DataFrame(data=pca_result, columns=['PCA1', 'PCA2'])
  return pca_df

def pca_scatter(df_list, opt_df, time):
  fig, ax = plt.subplots(figsize=(10, 7))
  max_x = 0
  max_y = 0
  min_x = 0
  min_y= 0
  for pca_df in df_list:
    maximum_x = pca_df["PCA1"].max()
    maximum_y = pca_df["PCA2"].max()
    if maximum_x > max_x:
      max_x = maximum_x
    if maximum_y > max_y:
      max_y = maximum_y

  for pca_df in df_list:
    minimum_x = pca_df["PCA1"].min()
    minimum_y = pca_df["PCA2"].min()
    if minimum_x < min_x:
      min_x = minimum_x
    if minimum_y < min_y:
      min_y = minimum_y

  def update(frame):
      ax.clear()
      # ax.scatter(df_list[frame]['PCA1'].iloc[range(df_list[frame].shape[0] - 1)], df_list[frame]['PCA2'].iloc[range(df_list[frame].shape[0] - 1)], color='red', s=5)
      # ax.scatter(df_list[frame]['PCA1'].iloc[df_list[frame].shape[0]-1], df_list[frame]['PCA2'].iloc[df_list[frame].shape[0]-1], color='green', s=100, marker='s')
      ax.scatter(df_list[frame]['PCA1'], df_list[frame]['PCA2'], color='red', s=5)
      ax.scatter(opt_df['PCA1'].iloc[frame], opt_df['PCA2'].iloc[frame], color='green', marker='s', s=100)
      ax.set_title(f'Genotypy osobników w pokoleniu {str(frame)}')
      ax.tick_params(axis='x')
      ax.set_ylim(1.15*min_y, 1.15 * max_y)
      ax.set_xlim(1.15*min_x, 1.15 * max_x)
      
    
  frames = range(time+1)
  animation = FuncAnimation(fig, update, frames=frames, interval=500)
  animation.save("proba.gif", writer='pillow')
  