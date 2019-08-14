#Catfish nutrition linear programming problem
from pulp import *


#Create a list of ingredients
ingredients = ['maize','fishmeal','soymeal','ricebran','limestone']

#Create a dictionary of costs
costs = {'maize':2.15,'fishmeal':8.0,'soymeal':6.0,'ricebran':2.0,'limestone':0.4}
protein_percent = {'maize':9.0,'fishmeal':65,'soymeal':44,'ricebran':12,'limestone':0}
digestible_energy = {'maize':1.10,'fishmeal':3.90,'soymeal':2.57,'ricebran':1.99,'limestone':0.1}
calcium_percent = {'maize':0.02,'fishmeal':3.7,'soymeal':0.3,'ricebran':0.1,'limestone':38.0}

# The challenge is to minimise the cost 
model = LpProblem("The Catfish feeding problem", LpMinimize)

# Ingredients cannot be of a negative amount, set lowerbound to zero
ingredient_vars = LpVariable.dicts("Ingr",ingredients,0)

#print (ingredient_vars)

# Add the objective fucntion to the model
model += lpSum([costs[i]*ingredient_vars[i] for i in ingredients]), "Total Cost of Ingredients per can"

# Add constrints to the model
model += lpSum([ingredient_vars[i] for i in ingredients]) == 100, "Total weight of mix."
model += lpSum([protein_percent[i] * ingredient_vars[i]/100.0 for i in ingredients]) >= 30.0, "Total protein"
model += lpSum([digestible_energy[i] * ingredient_vars[i] for i in ingredients]) >= 250.0, "Total digestible energy"
model += lpSum([calcium_percent[i] * ingredient_vars[i]/100.0 for i in ingredients]) >= 0.5, "Min calcium"
model += lpSum([calcium_percent[i] * ingredient_vars[i]/100.0 for i in ingredients]) <= 1.5, "Max calcium"
model += ingredient_vars['fishmeal'] >= 8.0, "Fishmeal"
model += ingredient_vars['ricebran'] >= 20.0, "Ricebran"

#Print the problem
print (model)

#Solve the problem
model.solve()
print ("Status : ", LpStatus[model.status])

#Print our objective function value - Result (Target) cell
print ("Total Cost             = ", value(model.objective))

#Print the amounts of each feed needed
for v in model.variables():
    print (v)
    print (v.varValue)

