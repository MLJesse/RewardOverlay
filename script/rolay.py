import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import tkinter
from tkinter import StringVar
from time import sleep
import threading

# Locks variables so functions can't step on each other.
lock = threading.Lock()

# Pilot for tkinter.
root = tkinter.Tk()

# What text is being displayed in the overlay.
stringLabel = StringVar(root)

# Variable counters for luck.
goodLuck = 0
badLuck = 0

# Variable for new incoming rewards.
rewardsListNew = []

# Watches the rewardsListNav variable for new entries, scans to see if they are of a reward type.
def run_watcher():
	# Global declarations, to reference the above variables.
	global rewardsListNew
	global lock
	global goodLuck
	global badLuck
	global stringLabel
	global root
	global driver
	
	# Run indefinitely.
	while (1==1):
		# Give some breathing room in between scans.
		sleep(5)
		#print('Waiting for quiet chrome scan')
		lock.acquire()
		#print('Acquired read rights')
		index = 0
		rewardsListLen = len(rewardsListNew)
		#print('Here is length ' + str(rewardsListLen))
		
		# Loop through all of the rewards redeemed.
		while (index < rewardsListLen):
			# Grabbing the element in the array.
			elem = rewardsListNew[index]
			index += 1
			#print(elem.get_attribute('id'))
			if (elem.get_attribute('id') == 'overlay_ready'):
				# Try and split the info from the string.
				try:
					print('Scanning new rewards...')
					setAttrScript = 'return arguments[0].setAttribute(\'id\', \'overlay_parsed\')'
					driver.execute_script(setAttrScript, elem)
					rewardInfo = elem.get_attribute('innerText')
					print(rewardInfo)
					exclamationPointIndex = rewardInfo.find('!')
					goodPointAmountIndex = rewardInfo.find('1,000')
					badPointAmountIndex = rewardInfo.find('2,000')
					colonIndex = rewardInfo.find(':')
					#print('Indexes Scanned')
					#print(goodPointAmountIndex)
					#print(badPointAmountIndex)
					#print(colonIndex)
					#print (exclamationPointIndex)
					decision = 'N/A'
					# If our information was found appropriately. (-1 means it didn't find it)
					if (goodPointAmountIndex != -1 or badPointAmountIndex != -1):
						print('Luck Reward Claimed')
						# Currently disabled by request (not added to string below) - Decider, who sent the reward.
						if (goodPointAmountIndex != -1):
							decider = rewardInfo[goodPointAmountIndex+5:colonIndex]
						if (badPointAmountIndex != -1):
							decider = rewardInfo[badPointAmountIndex+5:colonIndex]
						# More information found checking.
						if(exclamationPointIndex != -1):
							# If it was good or bad luck, increment the appropriate variable.
							goodLuckIndex = rewardInfo.find('good')
							badLuckIndex = rewardInfo.find('bad')
							if (goodLuckIndex != -1):
								decision = 'Good'
								goodLuck += 1
							if (badLuckIndex != -1):
								decision = 'Bad'
								badLuck += 1
						# Set the string.
						luckString = 'Jhreks Luck: '
						luckString += '| Good: ' + str(goodLuck) + ' | Bad: ' + str(badLuck) + ' | '
						#luckString += 'Decider: ' + decider + ' - ' + decision + ' | ' 
						
						print(luckString)
						stringLabel.set(luckString)
						
						# Signal that the overlay should update it's text.
						root.update_idletasks()
				except Exception as e:
					# If you see this message me immediately, there is a bug in the code.
					print('Something bad happened')
					print(e)
		#print('Watcher releasing')
		rewardsListNew = []
		lock.release()
def run_quiet_chrome():
	try:
		global lock
		global rewardsListNew
		global driver
		# Setting up our browserless chrome.
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)  
		# Your twitch chat url is loaded.
		driver.get("https://www.twitch.tv/popout/superscientistjhrek/chat?popout=")
		
		# Run indefinitely.
		while (1 == 1):
			# Breathing room timer.
			sleep(5)
			try:
				#print('Scanner scanning...')
				# Grabs the items that are channel point reward elements, they have a special class.
				magnifying_glass = driver.find_elements_by_class_name("channel-points-reward-line")
				# If some were found.
				if (len(magnifying_glass) > 0):
					#print('Scanner acquiring rights')
					# Lock the variable since we're writing
					lock.acquire()
					# List to store unparsed rewards.
					newList = []
					#print('Scanner acquired rights')
					# Loops through all the new rewards and checks to see if they've been parsed.
					for i in range(0, len(magnifying_glass)):
						id = magnifying_glass[i].get_attribute('id')
						#`print(id)
						if (id != 'overlay_parsed' and id != 'overlay_ready'):
							#print('Running the script, as ID\'s are not equal.')
							setAttrScript = 'arguments[0].setAttribute(\'id\', \'overlay_ready\')'
							driver.execute_script(setAttrScript, magnifying_glass[i])
							newList.append(magnifying_glass[i])
							#print(magnifying_glass[0].get_attribute('innerText'))
					#print('Scanner Released Rights')
					rewardsListNew = newList
					lock.release()
			except:
				print('Nothing found yet')
				sleep(1)
	except Exception as e:
		print(e)
# Here the initial code is ran that sets up the overlay panels design.
try:
	# Starting Label.
	stringLabel.set('Jhrek Is At Peace')
	
	# Start the chrome scanner
	threading.Thread(target=run_quiet_chrome).start()
	print('Setting up label')
	# Setting up the label, you can make font adjustments here.
	label = tkinter.Label(root, textvariable=stringLabel, font=('Arial','12', 'bold'), fg='black', bg='whitesmoke', highlightbackground="black")
	label.master.overrideredirect(True)
	label.master.geometry("+10+10")
	label.master.lift()
	label.master.wm_attributes("-topmost", True)
	label.master.wm_attributes("-disabled", True)
	label.master.wm_attributes("-transparentcolor", "white")
	print('Packing')
	label.pack()
	# Running the reward watcher.
	threading.Thread(target=run_watcher).start()
except Exception as e:
	print(e)
tkinter.mainloop()