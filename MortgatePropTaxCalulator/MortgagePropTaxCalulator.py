'''
Loan calculator for a home.
It includes:
- An exponential Loan calculator
	- Demonstrates cost over time and splits out the interest vs principal payments over time
- A Tax Calculator
	- That ideally adjusts for 2% property tax increase over time
- An Effective cost calculator
	- Combinining the tax and interest cost for an effective cost rate
- A tax break calculator
	- That shows the effective tax incentives over time.

Outputs should be some .csv and .txt files that can be handed over to Farzana for warm fuzzy comparison

TODO - Some plot visuals of interest vs principal might be nice.  People like pictures.  

Let's see how this goes.

HOW TO USE:
- Scroll down to the bottom past `if __name__ == "__main__":`

- Input your home loan parameters.  All inputs should be formatted as lists.

TODO - I didn't architect this very well.  Reorganizing math and csv functions into their own files, plus having a separate parameter file the user calls would
	   be a cleaner implementation.  

TODO - Clean up extraneous comments

TODO - Clean up print statements into 'if debug: print(x)' type architecture.

'''

import math
import csv
import os

# def loanCalc():
# 									# IS THIS STILL RELEVANT?
# 	# Loan Amout = Payment / (interest rate) * [1 - 1/[(1 + interest rate) ^ (length of loan)]
# 	pass

# def adjustedPaymentCalc():
# 									# IS THIS STILL RELEVANT?
# 	pass

# def principalDiff():
# 									# IS THIS STILL RELEVANT?
# 	pass

class Loan:
	def __init__(self,homePrice,downPayment,points,intRate,loanTerm,addedPayment):
		
		# Initial Parameters
		self.homePrice = homePrice
		self.downPayment = downPayment
		self.loanTerm = loanTerm
		self.addedPayment = addedPayment
		self.points = points
		self.breakEvenMonth = 0
		self.intRate = intRate - 0.25*points # Each point purchased reduces loan interest rate by 0.25%	
		self.loanAmount = homePrice - downPayment
		self.pointCost = self.loanAmount * 0.01 * points # Assumes each loan point cost 1% of the loan

		# Find minimum monthly payment and add any optional payments for a total payment
		self.monthlyPayment = self.monthlyPayments(self.loanAmount,self.intRate,self.loanTerm)
		self.totalPayment = self.monthlyPayment + self.addedPayment
		
		# Run ammortizer fnc to generate the payment schedule
		[self.months, self.principalList, self.principalDelta, self.interestList] = self.ammortizer(homePrice,downPayment,self.intRate,self.loanTerm,self.totalPayment)
		
		# Factor in property taxes
		[self.taxList,self.adjustedTaxList] = self.propTax(homePrice,loanTerm)

		# Calculate the total interest cost of the loan
		self.totalIntCost = round(sum(self.interestList),2)
		print('Total interest cost of loan = $' + str(self.totalIntCost))


	def monthlyPayments(self, loanAmount, intRate, loanTerm):
		'''
		This function calculates the fixed monthly payment in order to pay off a loan in a specific amount of time.
			homePrice expected in dollars
			downPayment expected in dollars
			intRate expected preformatted as a percent (3.5% = 3.5 - not 0.035)
			loanTerm expected in years
				This function checks good with an online calculator! Yay math!
		'''
		i = intRate/12/100 # Assumes monthly compounding
		n = loanTerm * 12 # The plus 1 comes from 0 indexing

		monthlyPayment = loanAmount * i * (1+i)**n / ((1 + i)**n - 1)
		monthlyPayment = round(monthlyPayment,2)
		return monthlyPayment


			


	def ammortizer(self, homePrice,downPayment,intRate,loanTerm,totalPayment):
		'''
		This function generates the loan ammortization schedule.  It breaks down each monthly payment into the interest and principal components

			homePrice expected in dollars
			downPayment expected in dollars
			intRate expected preformatted as a percent (3.5% = 3.5 - not 0.035)
			loanTerm is expected in years
			totalPayment expected in dollars

		Returns 4 lists:
			months - list of sequential months cover loan term
			principalList - list of the remaining principal balance each month
			principalDelta - list of how much principal was paid down from the previous month (basically the principal payment component)
			interestList - list of how much interest was paid in that month
		'''
		principalList = []
		principalDelta = []
		interestList = []
		loanTermMonths = loanTerm * 12
		months = range(loanTermMonths + 1)
		# print(months)

		for i in months:
			principalList.append(self.principalCalc(homePrice,downPayment,intRate,i,totalPayment))

			if i == 0:
				principalDelta.append(0)
				interestList.append(0)

			else:
				principalDelta.append(round((principalList[i] - principalList[i-1]) * -1,2))
				interestList.append(round(intRate / 12 / 100 * principalList[i-1],2))

			# print(str(i+1) + ": " + str(principalList[i]) + " " + str(principalDelta[i]) + " " + str(interestList[i]))

		return [months, principalList, principalDelta, interestList]



	def propTax(self,homePrice,loanTerm):
		'''
		This function estimates California property taxes over the course of a loan term.  
		It takes in the homePrice (dollars) and loanTerm (months) and returns 2 lists.
		The first list - taxList - is a static, estimated tax cost based on the initial home value
		The second list - adjustedTaxList - increases the home value (and thereby increases tax) by 2% each year to account for "CA Prop 13"
		Both lists return a monthly cost

		NOTE - taxList is NOT used in the rest of this script since it's likely not realistic that property tax will remain static
		'''
		taxList = []
		adjustedTaxList = []
		loanTermMonths = loanTerm * 12
		taxRate = 1.25

		for i in range(loanTermMonths+1):
			tax = (round((taxRate/12/100 * homePrice),2))
			# print(tax)
			taxList.append(tax)
			year = math.floor(i/12) 
			adjustedTaxList.append(round((1.02**(year)*taxList[0]),2)) 
			# print(str(i+1) + ": " + str(taxList[i]) + " " + str(adjustedTaxList[i]))
		return [taxList, adjustedTaxList]

	def csvWriteOut(self):
		# TODO - Create a timestamped directory to add all the csv files to.  Keeps it organized
		# TODO - Add a path for the creation of things.  It probably shouldn't just generate in the script location.  Keeps git organized.
		# TODO - Create a summary csv with just the headerStack information in the cases of multiple csv generation.
		
		# It would probably be useful to have something generate a summary file


		def headerWrite(self, csvFile, writer):
			headerStack = []
			
			headerStack.append(['Starting Parameters:'])
			headerStack.append(['House Price',self.homePrice])
			headerStack.append(['Down Payment',self.downPayment])
			headerStack.append(['Loan Amount',self.loanAmount])
			headerStack.append(['Points',self.points])
			headerStack.append(['Interest Rate (%)',self.intRate])
			headerStack.append(['Loan Term (years)',self.loanTerm])
			headerStack.append(['Additional Payment Per Month',self.addedPayment])
			
			headerStack.append([''])
			headerStack.append(['Loan Costs:'])
			headerStack.append(['Total Interest Cost of Loan',self.totalIntCost])
			headerStack.append(['Points Cost (#buggy?)',self.pointCost])
			headerStack.append(['Point Break Even Month',self.breakEvenMonth])



			headerStack.append([''])
			headerStack.append(['End-Of-Year (EOY) Values:'])
			headerStack.append(['Monthly Property Tax EOY 1', round(self.adjustedTaxList[12],2)])
			headerStack.append(['Monthly Property Tax EOY 2', round(self.adjustedTaxList[24],2)])
			headerStack.append(['Monthly Property Tax EOY 5', round(self.adjustedTaxList[60],2)])
			headerStack.append(['Monthly Property Tax EOY 10', round(self.adjustedTaxList[120],2)])

			headerStack.append([''])
			headerStack.append(['Monthly Interest Cost EOY 1',round(self.interestList[12])])
			headerStack.append(['Monthly Interest Cost EOY 2',round(self.interestList[24])])
			headerStack.append(['Monthly Interest Cost EOY 5',round(self.interestList[60])])
			headerStack.append(['Monthly Interest Cost EOY 10',round(self.interestList[120])])

			headerStack.append([''])
			headerStack.append(['Monthly Principal Payment EOY 1',round(self.principalDelta[12])])
			headerStack.append(['Monthly Principal Payment EOY 2',round(self.principalDelta[24])])
			headerStack.append(['Monthly Principal Payment EOY 5',round(self.principalDelta[60])])
			headerStack.append(['Monthly Principal Payment EOY 10',round(self.principalDelta[120])])
		
			headerStack.append([''])
			headerStack.append([''])

			headerStack.append(['Month','Loan Principal','Total Payment','Principal Payment','Interest Payment','Added Payment','Adjusted Property Tax'])

			writer.writerows(headerStack)

		def rowWriter(self, csvFile, writer):
			months = self.months
			principalList = self.principalList 
			interestList = self.interestList
			adjustedTaxList = self.adjustedTaxList
			addedPayment = self.addedPayment
			principalDelta = self.principalDelta

			for m in self.months:
				# row = [months[m],principalList[m],round(principalDelta[m]+interestList[m]+addedPayment,2),principalDelta[m],interestList[m],addedPayment,adjustedTaxList[m]]
				row = [months[m],principalList[m],round(principalDelta[m]+interestList[m],2),principalDelta[m],interestList[m],addedPayment,adjustedTaxList[m]]
				writer.writerow(row)
			pass
		title=str(self.homePrice) + str(self.downPayment) + str(self.intRate).replace(".","_") + str(self.loanTerm) + str(self.addedPayment) +'.csv'
		with open(title,'w') as csvFile:
			writer = csv.writer(csvFile)

			headerWrite(self, csvFile, writer)
			rowWriter(self, csvFile, writer)
			# do some aggregation
			pass

		
			
	def principalCalc(self,homePrice, downPayment, intRate, time, payment):
		'''
		# This function calculates the principal balance remaining on a loan as a function of time, based on a fixed payment.

		# homePrice expected in dollars
		# downPayment expected in dollars
		# intRate expected preformatted as a percent (3.5% = 3.5 - not 0.035)
		# time is expected as months

		# Returns P - remaining principle in dollars 
		'''

		P0 = homePrice - downPayment # Initial principal
		i = intRate/12/100 # Assumes monthly compounding
		r = i + 1 # Loan interest multiple
		# time = time+! # accounting for 0 indexing

		P = P0 * r**time - payment * (r**time - 1) / (r - 1)
		P = round(P,2)
		
		if P < 0:
			P = 0
		
		# dP = r**time*(P-payment/(r-1)*math.log(r))  CURRENTLY BROKEN.  NEED TO FIGURE THIS OUT


		return P

def breakEvenCalc(pointLoan,baseLoan):
	'''
	This function calculates the number of months until the initial cost of mortgage points breaks-even with the discounted interest rate

	BUG - This seems to always return 51 months... so it might be buggy... 
	'''
	breakPrice = 0
	pointCost = pointLoan.pointCost
	i = 0

	while (breakPrice <= pointCost):
		breakPrice = breakPrice + (baseLoan.interestList[i] - pointLoan.interestList[i])
		i+=1
	return i




if __name__ == "__main__":
	

# If you enter multiple values as lists, it will output individual .csvs for all the combinatorics.  Each csv is named after the combination used

	# homePrice = [1500000,1600000,1700000]
	# downPayment = [350000,400000,450000]
	# intRate = [3.1,3.3,3.5]
	# loanTerm = [20,30]
	# addedPayment = [00,200,400]

	homePrice = [1500000] # Total cost of home (dollars)
	downPayment = [200000] # Total down payment (dollars)
	intRate = [2.875] # Interest rate (2.875 = 2.875%)
	loanTerm = [30] # Number of years of the loan (years)
	addedPayment = [270] # Additional monthly payments on top of minimum (dollars)
	points = [2] # Number of loan points applied


	for price in homePrice:
		# downPayment = [price*0.2] # Uncomment to apply 20% down (or put whatever you want) to all combinations
		for down in downPayment:
			for rate in intRate:
				for term in loanTerm:
					for payment in addedPayment:
						for point in points:
							loan = Loan(price,down,point,rate,term,payment)

							if (point > 0):
								baseLoan = Loan(price,down,0,rate,term,payment)
								loan.breakEvenMonth = breakEvenCalc(loan,baseLoan)
							loan.csvWriteOut()


