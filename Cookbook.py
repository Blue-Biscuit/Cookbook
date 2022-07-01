from argparse import ArgumentError
from ast import List

#########################
##### CLASSES
#########################

class Ingredient:
    """An ingredient with an amount."""

    def __init__(self, name: str, unit: str, amount: float):
        self.name = name
        self.unit = unit
        self.amount = amount
    
    def __str__(self):
        return self.__dict__

class Recipe:
    """A recipe, made up of ingredients and step-by-step instructions."""

    def __init__(self, name, ingredients, steps):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
    
    def numberedSteps(self) -> str:
        """Returns a newline-delineated list of steps to create the recipe."""
        
        result = ""

        for i in range(0,len(self.steps)):
            result += f"{i + 1}. {self.steps[i]}\n"
        
        return result

#########################
##### CONSTANTS
#########################

APP_DATA = {
    "name" : "Cookbook.py",
    "version" : 0,
    "subversion" : 0,
    "author" : "Andrew Huffman"
}

#########################
##### GLOBALS
#########################

UserData = {
    "recipes" : [],
    "stock" : []
}

#########################
##### HELPERS
#########################

def isEmpty(string: str) -> bool:
    return string.strip() == ""

def canFloat(string: str) -> bool:
    try:
        float(string)
        return True
    except:
        return False

#########################
##### COMMANDS
#########################

def commandHelp(uIn):
    global COMMANDS

    print("Commands:")
    for cmdName in COMMANDS.keys():
        print(f"{cmdName:<100}{ COMMANDS[cmdName]['help'] }")

def commandExit(uIn):
    exit()

def commandAppInfo(uIn):
    global APP_DATA

    print(f'{APP_DATA["name"]}, v. {APP_DATA["version"]}.{APP_DATA["subversion"]}')
    print(f'By {APP_DATA["author"]}')

def newRecipeCommand(uIn):
    """Creates a new recipe instance."""

    global UserData

    ingredients = []
    steps = []
    name = None

    ##################################################
    ##### Algorithm:
    ##### 1. Get the name of the recipe.
    ##### 2. Get the ingredients.
    ##### 3. Get the steps.
    ##################################################

    ##### 1. Get the name of the recipe.

    if (len(uIn) < 2):
        # Prompt for name
        while True:
                name = input("Enter recipe name >> ")

                if isEmpty(name):
                    print("Name cannot be empty.")
                    print()
                else:
                    break
    else:
        # Parse from uIn
        name = uIn[1]

        if isEmpty(name):
            print("Name cannot be empty.")
            print()

            while True:
                name = input("Enter recipe name >> ")

                if isEmpty(name):
                    print("Name cannot be empty.")
                    print()
                else:
                    break

    ##### 2. Get the ingredients.

    i = 1
    while True:
        ingredientName = input(f"Enter a name for ingredient {i} >> ")

        if (isEmpty(ingredientName)):
            break

        ingredientStockString = input(f"Enter how much of the ingredient {i} is necessary (amt unit) >> ").split(" ")

        ingredientStockVal = None
        if canFloat(ingredientStockString[0]):
            ingredientStockVal = float(ingredientStockString[0])
        else:
            print("Invalid amount input: not a value.")
            print()
            continue
    
        ingredientStockUnit = None
        if len(ingredientStockString) > 1:
            ingredientStockUnit = ingredientStockString[1]
        else:
            print("Invalid amount input: no unit provided.")
            print()
            continue

        ingredients.append(Ingredient(ingredientName, ingredientStockUnit, ingredientStockVal))
        i += 1
    
    ##### 3. Get the steps.

    i = 1
    while True:
        step = input(f"Enter step {i} >> ")

        if (isEmpty(step)):
            break

        steps.append(step)
        i += 1
    
    UserData["recipes"].append(Recipe(name, ingredients, steps))
    print(f'Successfully created recipe "{name}"')

def recipesCommand(uIn):
    global UserData

    for x in UserData["recipes"]:
        print(x.name)

def newStockCommand(uIn):
    global UserData

    ##################################################
    ##### Algorithm:
    ##### 1. If not provided by argument, prompt for
    ##### the name.
    ##### 2. Load/create the ingredient.
    ##### 3. Prompt for the amount, listing the amount
    ##### already had.
    ##################################################

    ingredient = None
    name = None
    amount = 0
    unit = None

    ##### 1. If not provided by argument, prompt for
    ##### the name.

    if len(uIn) >= 2:
        name = uIn[1]

        if isEmpty(name):
            print("Ingredient name cannot be empty.")
            print()
        
            while True:
                name = input("Enter the name of the ingredient >> ")

                if isEmpty(name):
                    print("Ingredient name cannot be empty.")
                    print()
                else:
                    break
    else:
        while True:
            name = input("Enter the name of the ingredient >> ")

            if isEmpty(name):
                print("Ingredient name cannot be empty.")
                print()
            else:
                break

    ##### 2. Load/create the ingredient.

    for x in UserData["stock"]:
        if x.name == name:
            ingredient = x
            break
    
    if ingredient == None:
        while True:
            unit = input("What unit is this ingredient measured in? >> ")

            if isEmpty(unit):
                print("Unit name cannot be empty.")
                print()
            else:
                break
        ingredient = Ingredient(name, unit, 0.0)
        UserData["stock"].append(ingredient)

    ##### 3. Prompt for the amount, listing the amount
    ##### already had.

    while True:
        print(f"Current stock of {ingredient.name}: {ingredient.amount} {ingredient.unit}")
        print()

        inAmt = input("How much would you like to add? >> ")

        if canFloat(inAmt):
            amount = float(inAmt)
            break
        else:
            print("Input must be a value.")
            print()
    
    ingredient.amount += amount
    print(f"You have {ingredient.amount} {ingredient.unit} of {ingredient.name} in stock.")


COMMANDS = {
    "help" : {"help" : "Prints help for UI commands.", "function" : commandHelp},
    "exit" : {"help" : "Exits the program.", "function" : commandExit},
    "appinfo" : {"help" : "Displays information about the program.", "function" : commandAppInfo},
    "newrecipe" : {"help" : "Builds a new recipe.", "function" : newRecipeCommand},
    "recipes" : {"help" : "Prints the names of all loaded recipes.", "function" : recipesCommand},
    "newstock" : {"help" : "Adds to the existing stock of an ingredient. If not posessed, creates that ingredient.", "function" : newStockCommand}
}

#########################
##### UI HELPERS
#########################

def splitUserInput(uIn: str):
    """Splits the user input into a workable list of arguments."""

    ##################################################
    ##### ALGORITHM:
    ##### 1. Split by space.
    ##### 2. Comb through, joining into one term
    ##### those which begin with a quote, to those
    ##### which end with a quote.
    ##################################################


    ##### 1. Split by space.

    spaceDelin = uIn.split(" ")

    ##### 2. Comb through, joining into one term
    ##### those which begin with a quote, to those
    ##### which end with a quote.

    result = []
    openQuoteLoc = -1
    for i in range(0, len(spaceDelin)):
        x = spaceDelin[i]

        if openQuoteLoc == -1:
            if x.startswith('"'):
                if x.endswith('"'):
                    # Substring off the quotes.
                    result.append(x[1:(len(x) - 1)])
                else:
                    # Flag the beginning of a quote
                    openQuoteLoc = i
            else:
                # Add as normal.
                result.append(x)

        elif openQuoteLoc != -1:
            if x.endswith('"'):
                arg = " ".join(spaceDelin[openQuoteLoc:(i + 1)]) # Join those which have quotes
                arg = arg[1:(len(arg) - 1)] # Trim off quotes
                openQuoteLoc = -1

                result.append(arg)

    return result




def main():
    commandAppInfo("")
    print()

    while True:
        uIn = splitUserInput(input(">>> "))

        toRun = uIn[0].lower()

        for x in COMMANDS.keys():
            if toRun == x:
                COMMANDS[x]["function"](uIn)

        if (toRun != ""):
            print()

if __name__ == "__main__":
    main()