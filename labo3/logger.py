# Imports
import os.path
import time
import sys

# Logger class
class Logger():
	def __init__(self):
		self.yes = set(['yes', 'y', ''])
		self.no = set(['no', 'n'])
		self.i = 0
		f = open('AlarmLog.txt', 'r')
		self.logLines = f.readlines()
		f.close

	def askForAction(self):
		self.action = int(input('Please choose what action you want to execute: \n[1] Display the entries line per line.\n[2] Enter a range of dates to remove from the log.\n'))
		if self.action == 1:
			while self.i < len(self.logLines):		
				self.askToDeleteSingleEntry()
			self.saveRemainingEntries()
		elif self.action == 2:
			self.askForRange()
		else:
			print('Please respond with: [1/2]')
			self.askForAction()

	def askToDeleteSingleEntry(self):
		# print remaining amount of entries
		print('\nRemaining entries: ', len(self.logLines) - self.i)
		# show the next available entry to the user and ask if he wants to delete it
		print('Current entry: ', self.logLines[self.i])
		print('Would you like to delete this entry?')
		self.userInput = input('[yes/no]: ').lower()
		if self.userInput in self.yes:
			self.userInput = True
			deletedEntry = self.logLines.pop(self.i)
			print('Following entry has been deleted', deletedEntry)
		elif self.userInput in self.no:
			self.userInput = False
			self.i = self.i + 1
			print('Entry not removed')
		else:
			print('Please respond with: [yes/no]')
			self.askToDeleteSingleEntry()

	def askForRange(self):
		print('Please provide the start & end date to delete all the entries between them')
		print('Format: dd-mm-yy')
		self.startDate = input('Start date: ')
		self.startDate = time.strptime(self.startDate, '%d-%m-%y')
		self.endDate = input('End date: ')
		self.endDate = time.strptime(self.endDate, '%d-%m-%y')
		self.deleteRange()

	def deleteRange(self):
		count = 0
		while self.i < len(self.logLines):		
			currentDate = time.strptime(self.logLines[self.i][:8], '%d-%m-%y')
			if currentDate >= self.startDate and currentDate <= self.endDate:
				self.logLines.pop(self.i)
				count += 1
			else:
				self.i = self.i + 1
		print(count, ' entries deleted')
		self.saveRemainingEntries()


	def saveRemainingEntries(self):
		f = open('AlarmLogAfterManipulation.txt', 'w')
		f.write(''.join(self.logLines))
		f.close
		print('New log file has been saved')


def main():
    try:
    	logger = Logger()
    	logger.askForAction()
    except KeyboardInterrupt:
	    pass
    finally:
	    print('Exit program')

# main segment
if __name__ == "__main__":
    main()