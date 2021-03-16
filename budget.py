class Category:
    # lists and dicts are 'remembered' across instances so declare them in the constructor
    def __init__(self, name):
        self.type = name
        self.ledger = []

    def __repr__(self):
        title = '{:*^{width}}'.format(self.type, width=30) + '\n'
        transaction = ''
        total = 'Total: '+'{:,.2f}'.format(self.get_balance())

        for entry in self.ledger:
            description = entry['description'][:23]
            amount = '{:>{width}}'.format(str('{:,.2f}'.format(entry['amount'])), width=30-len(description))
            transaction+=description + amount + '\n'

        return title + transaction + total

    # description is defined, else an empty string
    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount) == True:
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for entry in self.ledger:
            balance+=entry['amount']
        return balance

    def transfer(self, amount, budget):
        if self.check_funds(amount) == True:
            self.withdraw(amount, f'Transfer to {budget.type}')
            budget.deposit(amount, f'Transfer from {self.type}')
            return True
        return False

    def check_funds(self, amount):
        return True if self.get_balance() >= amount else False



food = Category('food')
entertainment = Category('entertainment')
business = Category('business')

food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")

food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)



import re

def create_spend_chart(categories):

    graphstr = 'Percentage spent by category\n'

    # formatData() takes in the all instance data and returns them in the appropriate format
    (totalWithdrawls, budgetWithdrawlTotals, budgetTitles) = formatData(categories)

    # yAxis() creates the y-axis, its labels, and the bar chart
    graphstr += yAxis(budgetWithdrawlTotals)

    # create the x-axis (a dashed line appropriately sized to the number of budgets)
    width = len(budgetTitles)*3+1
    graphstr+='{:>{width}}'.format('-'*width, width=4+width) + '\n'

    # xAxis() formats all the budget titles into vertical columns and returns them as one string
    graphstr+=xAxis(budgetTitles)

    # format whitespace to pass the fCC tests
    graphstr = graphstr.rstrip() + '  '

    #print(repr(graphstr))
    #print(graphstr)

    return graphstr

def formatData(categories):
    totalWithdrawls = 0
    budgetWithdrawlTotals = []
    budgetTitles = []

    for entry in categories:
        subtotal = 0
        entry = str(entry).split()
        budgetTitles.append(''.join(re.findall('\w', entry[0])))

        for elem in entry:
            if elem.startswith('-'):
                subtotal+=float(elem)
                totalWithdrawls+=float(elem)

        budgetWithdrawlTotals.append(subtotal)

    for i in range(len(budgetWithdrawlTotals)):
        budgetWithdrawlTotals[i] = '{:,.2f}'.format(budgetWithdrawlTotals[i]/totalWithdrawls * 100)

    return totalWithdrawls, budgetWithdrawlTotals, budgetTitles

def yAxis(budgetWithdrawlTotals):
    y = 100
    line = ''
    while y >= 0:
        line+='{:>4}'.format(f'{y}|') + ' '
        for val in budgetWithdrawlTotals:
            if float(val) >= y:
                line+='{:<2}'.format('o') + ' '
            # add blank spaces or the graph will auto arrange from greatest to least budget spending
            else:
                line+='{:<2}'.format('') + ' '
        line+='\n'
        y-=10
    return line

alternateWithWhileLoop = '''def xAxis(budgetTitles):
    longestTitle = max(budgetTitles, key=len)
    x = 0
    line = ''
    while x <= len(longestTitle):
        subline = ''
        for title in budgetTitles:
            try:
                subline+=str(title[x]) + '  '
            except:
                subline+='   '
                pass
        x+=1
        line+='     '+subline+'\n'
    return line'''

def xAxis(budgetTitles):
    longestTitle = max(budgetTitles, key=len)
    line = ''

    for x in range(len(longestTitle)):
        subline = ''
        for title in budgetTitles:
            try:
                subline+=str(title[x]) + '  '
            except:
                subline+='   '
                pass
        line+='     '+subline+'\n'
    return line