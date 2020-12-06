## Goal
Create a linear regression that will use previous Metacritic data for actors and core crew members to predict the Metacritic score for films. 

## Motivation
Prior to the pandemic beginning in spring, I was looking forward to the summer of 2020 because Christopher Nolan was finally releasing his next film. After March that anticipation faded as New York City shutdown and didn't reopened until the early summer month. The film industry took massive losses on films such as "Birds of Prey," taking in a total gross of 200 million dollars when the breakeven for the film would have been 250-300 million dollars. Birds of Prey had a sequal that was in development that has sense been shut down by Hollywood studios due to the massive loss companies suffered because of the lacking box office. I wanted to create a model that could predict the Metacritic score of a film based on the previous performance of movies. I thought to myself about how production companies and other financing bodies for films could make up for the loss that they would continue to suffer as the pandemic continued on as they were forced movies to be released only to gross far less than they would in a normal summer film season, as well as being forced into shelving films until they could have a wide release when the pandemic ended. 

## Data
My dataset was scrapped from Metacritic using Beautiful Soup. This proved to be more difficult than with practice that I had scrapping from websites that don't have restrictions on how much you can scrape, such as Wikipedia. I used CloudScraper to help scrape more and used the Requests library to use a header for the html request that I was making. I also used the sessions object to send my requests with cookies as a last effort. In the end I scraped every movie that Metacritic had in the database. From each movie I used the user score, the metascore, and all of the cast and crew information. 

I created a database for my data in Postgres with four tables: cast and crew credits, film details (runtime, release date, language), and finally the films with their metacritic score and userscore. I created my main features for analysis by using a film's release date and all of the actors in the film to create three features, prinicple cast mean previous Metascore, supporting cast mean previous Metascore, and then the mean of all the scores combined. I did the same with the crew having 4 features in the end: directors mean previous metascore, writers, producers, and then all other crew members were pooled together for an other crew members mean metascore variable. I did the same with the userscores to create the same seven features. I had films that had null values because everyone has to start somewhere so if there was a film where no actor had a previous metascore then there was no value to report. I dropped these null values. Even without the values in the table for anaylsis the Metascores of the films were still being utilized when actors would appear in their next and all following films. 

The last bit of work I had to do getting my dataset ready for analysis was creating dummy variables. I had production companies, languages, genres, mpaa ratings, and release dates. There was a total of 10,377 production companies so I decided it was best to exclude them for the time being. I made language dummies and binned together all of the languages that weren't in the 5 most used languages: English, Spanish, French, and German. For the genre categories I kept comedy and drama separate and then binned the other genres into action and adventure, suspense, and others. Lastly, I used the release month and kept the month of release and binned the months into seasons. 

## Feature Selection
I ran an inital regression of my data using StatsModels linear regression. The condition number was high and indicated that multicolinearity was having an effect on the model. The R^2 was .52 for my initial model.

For feature selection the main goal that I had was reducing mulitcolinearity and heteroskedasticity. I found the variance inflation factor for each feature to identify where the severity of multicolinearity was coming from. The whole cast metascore and whole cast user score averages as well as the MPAA rating R had the highest VIF quotients. After I removed those three features and ran the variance inflation factor test again all of the VIF quotients were below three and almost all of them were under 2.5 which provided some security that there was less colinearity. 

## Modeling 

data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAjQAAAGACAYAAAC6OPj9AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjMsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAgAElEQVR4nOzdeVyU5f7/8deAgApKuKTmFqOppOICHSC33E6kYmW5QI5b5lfLTmqmKGqkR9PEPIWppJVHskCN02mzU255XCBFO0ouKOWWKGSooDksc//+8OcUiVsiOPB+Ph4+Hsw9931dn7kYnPdc9zVzmwzDMBARERFxYE6lXYCIiIjIrVKgEREREYenQCMiIiIOT4FGREREHJ4CjYiIiDg8BRoRERFxeBVKuwARR9e0aVOaNGmCk9Nv7w9atGjBzJkz/1R7u3fvZvXq1UyfPr24SrxC06ZN2bZtG9WqVbttfRRl1apV5Obm8tRTT5Vov7ciJyeH4cOHk52dzQsvvMBf//rXK/bZv38/w4cPZ/PmzfZtJ06c4JVXXuHUqVMUFBQwYcIEOnTocMWxFouFn376iSpVqhTa/u9///tP1Zudnc1zzz3H8uXL/9TxJWndunVs27aNKVOmFEt7Xbp0wcXFhYoVK2IymcjNzcXJyYkJEybQsWPHa/bXq1cvpk6dSkBAQLHUIiVPgUakGPzzn/8stnBw6NAhTp06VSxt3WmSk5O57777SruMm7Jv3z5Onz7N119/fcV9+fn5vP/++yxZsoQLFy4Uum/kyJEMGDCAsLAw9u7dy+DBg9myZQuurq5XtDNhwgSCg4OLpd6zZ8+yZ8+eYmnrduvatStdu3Yt1jajoqJo2bKl/faXX37J5MmT2bx5823pT+4cCjQit1FaWhozZ87kzJkzFBQUYLFYePLJJ7HZbMyaNYv//e9/nD9/HsMw+Pvf/84999zDm2++SXZ2NpMmTeKxxx5jxowZfPbZZwAkJSXZb0dHR/Pdd9+RkZFB06ZNiYqKYtGiRXz11VfYbDbq1q3Lyy+/TK1ata5a3/Hjxxk8eDDt2rUjJSWFgoIC/va3vxEfH88PP/xAixYteP311zlx4gQWi4UOHTrwv//9D8MwmDZtGv7+/uTl5TF79my2bduGs7Mzvr6+TJo0CQ8PD7p06YKvry8HDhxg3LhxrF+/ni1btlCxYkUefvhhpk2bxunTp8nMzKRu3br84x//oHr16nTp0oXHH3+cbdu2kZ6ezqOPPsqYMWMAWL16Ne+99x5OTk54eXkxZ84c6tSpw/r161m0aBF5eXlUrFiRiRMn0qZNG9LS0oiIiCA3NxfDMHjyySeLnCFau3YtCxYswGaz4e7ubn8MkydP5tSpUzz66KPEx8dTsWJF+zF79+7lwIEDLFiwgGHDhtm379u3j7NnzxIWFgbA/fffzwcffIDJZLqp5092djYzZ84kNTWVvLw8goKCmDBhAhUqVGD16tXEx8eTl5fH2bNneeaZZwgLC2PSpElcvHiRRx99lISEBO6///5Cs3GXZ+cOHjzIzJkzqVy5MufPn+ejjz5i8+bNf3oMjx8/TkhICLt27bridmZmJhMnTiQrKwuATp06MWbMGBISEvjPf/5DTEwMFouF1q1bs3PnTtLT0wkKCmLGjBk4OTmRkJDA22+/TcWKFQkMDGT58uXs3bv3uuNnGAbHjx/H09MToFB/hw4dYvLkyfz666+YzeZCgfRa/d3s35iUIENEbkmTJk2MXr16Gb1797b/+/nnn428vDyjR48eRkpKimEYhnHu3DnjkUceMXbt2mXs3LnTeP75542CggLDMAwjJibG+L//+z/DMAzjo48+MkaMGGEYhmEkJiYaPXv2tPf1+9tvvvmm8fDDDxt5eXmGYRjGv/71L2PMmDH223Fxccbw4cOvWvPp06eNY8eOGU2aNDHWrl1rGIZhTJs2zejcubORnZ1tXLx40WjXrp2RnJxs3++TTz4xDMMwNm7caLRr187Izc013njjDWP06NFGbm6uUVBQYISHhxtTp041DMMwOnfubCxYsMDe78SJE42lS5cahmEYy5YtM2JiYgzDMAybzWYMHz7ceOedd+zHzZ492zAMwzh58qTRsmVL4+jRo8a+ffuMgIAA48SJE4ZhGMZ7771nTJ061fjxxx+NXr16Gb/88othGIaRmppqtGvXzjh//rwxadIkez8ZGRnGmDFj7ON+2aFDh4wHH3zQOHr0qGEYhrF161ajXbt2RnZ29hW/g6IcO3bMaN26tf32559/boSGhhqzZs0ynnzySaN///7Gli1bijx24MCBRufOnQs9fzZu3GgYhmGEh4cby5cvNwzDMPLz843x48cbb7/9tpGTk2P069fP/nh3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8eJNjIKIiEjZV2YDTXZ2Nm+++SYbN24EYOjQoRiGAYDJZLpi/yZNmrBr1y46derE//73v2KtpXHjxsTGxmKz2cjPz2fv3r1F7peRkcH333/PW2+9hdVqpVOnTjz66KNXrVlEREQuKVOBZsuWLfTp08d+u1WrVjz++ONUrlyZqlWrkpGRQb169Yo8dvz48UyePJl3332XKlWqUKHCtYfm8imn31uyZEmR+zZt2pROnTrRr18/vLy8cHFxKbL9mjVrkpmZyWOPPUblypUZNmzYdesQERGRMhRoAgIC+Pbbb29438sur0f57rvvmDlzJg0bNmTVqlXs3Lnzmsdv27atyPt+v5A4NDQUgNOnT1O1alVWr15Nbm4uPXv2pE6dOjz//PNX1DR9+vQr2ly/fr395/Hjx9/IQxQRESlXykyguVV16tRh7NixVKpUCScnJ2bNmkVkZCRpaWlX7LtkyRL72psb4eXlRUpKCk888QQmk4m+fftyzz33FGf5IiIi5ZoCzf/3wAMPkJCQUGhbZGRksbTt5OTEq6++WixtiYiIyJUUaESuY+ID991yG8nJycVQiYiIXE2Z/h4aERERKR8UaERERMThKdCIiIiIw9MaGpHr2J9YDH8mLkm33oaIiFyVZmhERETE4SnQiIiIiMNToBERERGHV6yBJikpiaCgICwWCxaLhX79+hW6FADApk2biI+Pv6l2ExISWLdu3VXvt1gsRX6j7/UcPHiQESNGYLFYeOKJJ3jzzTftF7C8UWfOnLnulbm7dOmC1Wq1305LS7viOlAiIiLy5xX7ouDAwEDmz58PQG5uLsHBwTz66KNUrVoVgI4dO950m7+/4GRxOXfuHOPGjSM6Opp7772XgoICXnjhBeLi4uzXYLoRBw4cYP369YSEhBR7jSIiInJjbuunnHJycnBycmLIkCHUq1ePc+fO0bNnT44cOcKAAQN48cUXqV27NseOHaNly5a88sornD59mvDwcLKzszEMgzlz5vDpp59So0YNzGYzixcvxsnJiczMTPr3789TTz1l7y87O5uIiAiysrIAmDJlCk2bNi2ytnXr1hEQEMC9994LgLOzM3PmzMHFxYWCggKmTZvGyZMnycrKomPHjowZM4avvvrq/7V353FVV/kfx18gSwoMoDGOpDVcd0vHIpPcktSi6OqouJEY2maTLVrJbuQUgag0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CDTmda8+jfnlPt/s/ze9kzh06BAxMTG12rt06cLzzz9vh4pERETqDwWaayQwMJCsrCx7lyEX0KWsyt4lUFBQYO8SREScmlaZioiIiMNToBERERGHp0AjIiIiDk9raMQpLNgQa+8SLqljwyH2LkFExKlphkZEREQcngKNiIiIODwFGhEREXF4CjQiIiLi8BRoRERExOE5VKDJz8/n3nvvJSoqiqioKIYOHfqzvp03JyeHGTNmXIcKL+z+++/HYrHYXu/evZuoqKg6619ERMTZOdyvbYeEhJCRkQFARUUFYWFhDBgwgF/96ld2rkxERETsxeECzU+VlZXh6upKdHQ0zZs359SpU7z77rskJCRw4MABqqurGT16NA8//DCbNm0iJSUFX19fXF1d6dy5MwcPHmTChAnk5uYCMHToUKZPn07Dhg2JjY3l9OnTGIZBWloaTZo0ISEhgePHjwOQmJhI27ZtCQ0NxWQyYTKZSEhIuOr3kJGRQV5eHlarlfDwcKKjo9m5cyevv/46AH5+fqSkpLBt2zamTp2Ku7s7Q4cO5fe///21G0gREREH53CBJi8vj6ioKFxcXHB3dycpKYm5c+diNpvp168f2dnZ+Pv7k56eTllZGYMGDSIkJIQ333yTadOmERQUxKuvvnrJPmbNmsX999/PiBEj+PLLL9myZQs7d+4kJCSEyMhI9u3bR1xcHDk5ORw+fJhly5bh7+//s97P8uXLyc7OpmnTpixbtgyApKQkUlJSaNWqFUuWLGHu3Ll069YNi8XCkiVLflY/IiIizszhAs1PHzmdN3fuXIKCgoBz61O6desGgLe3Ny1btuTAgQMcPXrUds5dd93F999/X+vehmEAsHfvXiIiIgC49957AXjyySfJy8tj5cqVAJw6dQoAf3//y4YZT09PKioq8PT0BODMmTPcdNNNAEyfPp3p06dTUlJCz549be/htddeA6CystJW9/l/ioiISE0OF2guxsXFBYCWLVuyadMm+vXrR1lZGUVFRTRv3pyAgAB2795Ny5YtKSwsxNfXF09PT0pLS6murqa8vJyDBw/a7lFYWEi7du3YuHEjn332GSaTif79+2M2myktLbXNlLi6Xn5ddYcOHfj0009tIWn9+vV07NiRiooKPvnkE6ZPn45hGISHhxMeHk5QUBBpaWkEBgZSUFDAsWPHrrgvERGR+shpAs15Q4cOJSkpiREjRmCxWBg3bhxNmjQhPT2dmJgYvLy88PLywtfXl4CAALp3705ERAS33nort912GwBjx44lPj6ejz76CICUlBS8vb1JSEggNzeXsrIyxo0bd8U1TZw4kaSkJHJycnBzc6NFixa89tpreHh44Ovry4ABA/D19aV79+4EBgaSnJxMTEwM1dXVALzxxhsUFxdf+8ESERFxEi7G+ecs4hQsFgtbt27ljjvusD3i+l8FBQUEBwfXcWXXlyNsTulsY36jc8af8xudxrzu1acxv9znm9PN0NjL2rVrWbBgQa32UaNG0a9fv7ovSEREpB5RoLlG+vTpQ58+fexdRr0V3SPV3iVcUkFBgb1LEBFxalplKiIiIg5PgUZEREQcngKNiIiIODytoZHLavDS1W8AKjV9FdnB3iWIiDg1zdCIiIiIw1OgEREREYenQCMiIiIO74oDzbvvvkt0dDRjxozh8ccfZ+vWrdezrhoWL15MZWUl27dv589//vM1u+/JkyeJj4/n0UcfZfjw4YwfP57Tp09f9X2ys7MveTw2Npb169fXaOvevftV9yMiIiIXdkWBZteuXaxbt4758+fz3nvv8fLLLxMfH3+9a7PJzMzEarXSvn37q9pD6XImTJhAaGgoCxcuZNGiRfzud79j0qRJV32fWbNmXbOaRERE5Opd0W85NW7cmEOHDvHhhx/Sq1cv2rdvz4cffkhUVBTJycm0bNmSnJwcSkpKGDhwIC+88AIBAQEcPXqUXr16MX78eGJjYzEMg8OHD3PmzBnS0tJo2bIl7733Hv/4xz9wc3Pj7rvv5pVXXmHGjBls3ryZM2fOYDabOXbsGOPHj+exxx5j0aJFZGRk8MADD3DXXXexd+9emjRpwowZM6isrGTixIkUFxfTrFkzNm7cyIYNGy74nn744QdKSkpqbEsQFRXF4MGDgXOzLqtWraKqqgofHx9mzJjBDz/8QFxcHG5ubjRo0IApU6awbNkyTp48SXJyMsnJyVf9B7Bq1SrmzJmDm5sbt9xyC1OmTKG8vJyEhASOHz8OQGJiIm3btiU0NBSTyYTJZCIhIeGq+xIREXFWVxxoZs2aRXZ2Nu+88w433XQT48ePv+j5P/zwA/PmzcPHx4fIyEi+++47AFq0aEFaWhqff/456enpjB8/npUrV7Jo0SLc3Nx47rnn+Oc//wmAyWQiMTERgHnz5pGRkcE333xj6+PAgQO8//77NGvWjOHDh1NYWMi3335L8+bNefvtt9m9ezePPPLIRWssLi6mefPmNdoaNGiAj48PVquVEydOsGDBAlxdXXn88ccpLCxkx44d3H777cTGxrJp0yZOnjzJM888Q3Z29lWHGRcXFwBWrFhBdHQ04eHhLF++nLKyMjIzMwkJCSEyMpJ9+/YRFxdHTk4Ohw8fZtmyZfj7+19VXyIiIs7uigLN/v378fb25s033wSgsLCQp556iptvvtl2zk837W7Xrh1+fn4AdOrUib179wIQEhICwJ133klKSgp79uzhd7/7He7u7gDcfffd/Oc//wEgKCjokjX5+/vTrFkzAJo1a4bFYmH37t306tULgJYtW9K4ceOLXh8YGMiRI0dqtFVWVvLJJ59gNptxd3dnwoQJNGrUiCNHjlBVVUVERARz5szhiSeewMfH55Kh7qc8PT2pqKio0VZVVQVAXFwcmZmZ5OTkYDKZ6Nu3L0VFReTl5bFy5UoATp06ZXvPCjMiIiK1XdEamp07d5KcnIzFYgHOhQ0fHx/8/Pw4duwYANu2bbOdv3v3bs6ePUt1dTVbtmyhVatWALaZmq+//prWrVtjMpnYsmULVVVVGIbBxo0bbUHG1fW/pbm4uGC1WmvUdH6G46fatGnD5s2bAfj+++9tj2wupGnTpvj7+7NmzRpb21/+8hfWrFnDjh07WLNmDW+99RZJSUlYrVYMw2Dt2rUEBwfz/vvvExYWxty5c4GaYe5Cbr/9dlavXm17vWnTJtuYLF68mOeee862sHj16tWYTCaio6PJysrirbfewmw21xoTERER+a8rmqF54IEH2L17N0OGDKFRo0YYhsHEiRNxd3dn8uTJNGvWjF//+te2893d3XnhhRcoKSkhLCyMdu3aAbB+/XrWrl2L1WrlzTffpEWLFjz00EOMGDECq9VKcHAwffv2ZceOHTX6v/vuu3nqqad49tlnL1lnREQEsbGxPProowQGBuLp6XnJ86dMmcLkyZN57733qKys5NZbb+X111/Hzc2Nhg0bMmjQIDw8PAgICKC4uJjOnTvb1vi4uroSFxcHnJsNevnll5k6deoF+xk4cCDbt29nwIABeHl52cYNzs1gjR49Gj8/P7y8vOjduze9e/cmISGB3NxcysrKrulCaBEREWfkYlxu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%0A

I used 



