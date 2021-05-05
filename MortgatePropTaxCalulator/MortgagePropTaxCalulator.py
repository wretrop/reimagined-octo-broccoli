# This is hopefully going to be my master loan calculator for a home.
# It should include:
# - An exponential Loan calculator
# 	- Demonstrates cost over time and splits out the interest vs principal payments over time
# - A Tax Calculator
# 	- That ideally adjusts for 2% property tax increase over time
# - An Effective cost calculator
# 	- Combinining the tax and interest cost for an effective cost rate
# - A tax break calculator
# 	- That shows the effective tax incentives over time.

# Outputs should be some .csv and .txt files that can be handed over to Farzana for warm fuzzy comparison ( I <3 yuuuuuu! )

# Let's see how this goes.

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
		self.homePrice = homePrice
		self.downPayment = downPayment
		self.loanTerm = loanTerm
		self.addedPayment = addedPayment
		self.points = points
		self.breakEvenMonth = 0


		self.intRate = intRate - 0.25*points
		
		self.loanAmount = homePrice - downPayment
		self.pointCost = self.loanAmount * 0.01 * points


		self.monthlyPayment = self.monthlyPayments(self.loanAmount,self.intRate,self.loanTerm)
		

		self.totalPayment = self.monthlyPayment + self.addedPayment
		
		


		[self.months, self.principalList, self.principalDelta, self.interestList] = self.ammortizer(homePrice,downPayment,self.intRate,self.loanTerm,self.totalPayment)
		[self.taxList,self.adjustedTaxList] = self.propTax(homePrice,loanTerm)

		self.totalIntCost = round(sum(self.interestList),2)
		print(self.totalIntCost)

	def monthlyPayments(self, loanAmount, intRate, loanTerm):
		# This function calculates the fixed monthly payment in order to pay off a loan in a specific amount of time.

		# homePrice expected in dollars
		# downPayment expected in dollars
		# int rate expected already as a percent 3.5 not 0.035
		# loan length expected in years
		#  This function checks good with online calculator!

		i = intRate/12/100 # Assumes monthly compounding
		n = loanTerm * 12 # The plus 1 comes from 0 indexing

		monthlyPayment = loanAmount * i * (1+i)**n / ((1 + i)**n - 1)
		monthlyPayment = round(monthlyPayment,2)
		return monthlyPayment


			


	def ammortizer(self, homePrice,downPayment,intRate,loanTerm,totalPayment):
		principalList = []
		principalDelta = []
		interestList = []
		loanTermMonths = loanTerm * 12 + 1
		months = range(loanTermMonths)
		# print(months)

		for i in range(loanTermMonths+1):
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
		taxList = []
		adjustedTaxList = []
		loanTermMonths = loanTerm * 12

		for i in range(loanTermMonths+1):
			# taxList.append(round((1.25/12/100 * homePrice),2))
			# taxList.append(round((1.1/12/100 * homePrice),2))
			tax = (round((1.1/12/100 * homePrice),2))
			print tax
			taxList.append(tax)
			year = math.floor(i/12) 
			adjustedTaxList.append(round((1.02**(year)*taxList[0]),2)) # Plus 1 because tax still gets charged the first year
			# print(str(i+1) + ": " + str(taxList[i]) + " " + str(adjustedTaxList[i]))
		return [taxList, adjustedTaxList]

	def csvWriteOut(self):
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
			headerStack.append(['Costs'])
			headerStack.append(['Total Interest Cost of Loan',self.totalIntCost])
			headerStack.append(['Points Cost',self.pointCost])
			headerStack.append(['Point Break Even Month',self.breakEvenMonth])



			headerStack.append([''])
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

			# headerStack.append(['Property Tax EOY 2  + Interest Cost EOY 2',round(self.interestList[24] + self.adjustedTaxList[24],2)]) # 24
			# headerStack.append(['Property Tax EOY 5  + Interest Cost EOY 5',round(self.interestList[60] + self.adjustedTaxList[60],2)]) # 60
			# headerStack.append(['Property Tax EOY 10 + Interest Cost EOY 10',round(self.interestList[120] + self.adjustedTaxList[120],2)]) # 120
		
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
		# This function calculates the principal balance remaining on a loan as a function of time, based on a fixed payment.

		# This will get plugged into some for loop later to generate amortization schedule!

		# homePrice expected in dollars
		# downPayment expected in dollars
		# int rate expected already as a percent 3.5 not 0.035
		# time is expected as months
		

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

	homePrice = [1660000] # Total cost of home (dollars)
	downPayment = [homePrice[0]*0.2] # Total down payment (dollars)
	intRate = [2.875] # Interest rate (2.875 = 2.875%)
	loanTerm = [30] # Number of years of the loan (years)
	addedPayment = [270] # Additional monthly payments on top of minimum (dollars)
	points = [0] # Loan points applies 


	for price in homePrice:
		downPayment = [price*0.2]
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


