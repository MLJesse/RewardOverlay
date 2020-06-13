import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import tkinter
from tkinter import StringVar
from time import sleep
import threading

lock = threading.Lock()
root = tkinter.Tk()
stringLabel = StringVar(root)
goodLuck = 0
badLuck = 0
foundElement = 0
rewardsListNew = []
def run_watcher():
	global rewardsListNew
	global lock
	global goodLuck
	global badLuck
	global stringLabel
	global root
	global driver
	
	while (1==1):
		sleep(5)
		print('Waiting for quiet chrome scan')
		lock.acquire()
		print('Acquired read rights')
		index = 0
		rewardsListLen = len(rewardsListNew)
		print('Here is length ' + str(rewardsListLen))
		
		while (index < rewardsListLen):
			elem = rewardsListNew[index]
			index += 1
			print(elem.get_attribute('id'))
			if (elem.get_attribute('id') == 'overlay_ready'):
				try:
					
					print('Scanning new Rewards')
					setAttrScript = 'return arguments[0].setAttribute(\'id\', \'overlay_parsed\')'
					driver.execute_script(setAttrScript, elem)
					rewardInfo = elem.get_attribute('innerText')
					print(rewardInfo)
					exclamationPointIndex = rewardInfo.find('!')
					goodPointAmountIndex = rewardInfo.find('1,000')
					badPointAmountIndex = rewardInfo.find('2,000')
					colonIndex = rewardInfo.find(':')
					print('Indexes Scanned')
					print(goodPointAmountIndex)
					print(badPointAmountIndex)
					print(colonIndex)
					print (exclamationPointIndex)
					decision = 'N/A'
					if (goodPointAmountIndex != -1 or badPointAmountIndex != -1):
						print('Luck Reward Claimed')
						if (goodPointAmountIndex != -1):
							decider = rewardInfo[goodPointAmountIndex+5:colonIndex]
						if (badPointAmountIndex != -1):
							decider = rewardInfo[badPointAmountIndex+5:colonIndex]

						if(exclamationPointIndex != -1):
							goodLuckIndex = rewardInfo.find('good')
							badLuckIndex = rewardInfo.find('bad')
							if (goodLuckIndex != -1):
								decision = 'Good'
								goodLuck += 1
							if (badLuckIndex != -1):
								decision = 'Bad'
								badLuck += 1
						
						luckString = 'Jhreks Luck: '
						luckString += '| Good: ' + str(goodLuck) + ' | Bad: ' + str(badLuck) + ' | '
						#luckString += 'Decider: ' + decider + ' - ' + decision + ' | ' 
						
						print(luckString)
						stringLabel.set(luckString)
						
						root.update_idletasks()
				except Exception as e:
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
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)  
		driver.get("https://www.twitch.tv/popout/superscientistjhrek/chat?popout=")
		while (1 == 1):
			sleep(5)
			try:
				print('scanner Scanning')
				magnifying_glass = driver.find_elements_by_class_name("channel-points-reward-line")
				if (len(magnifying_glass) > 0):
					#print('Scanner acquiring rights')
					lock.acquire()
					newList = []
					#print('Scanner acquired rights')
					for i in range(0, len(magnifying_glass)):
						id = magnifying_glass[i].get_attribute('id')
						#`print(id)
						if (id != 'overlay_parsed' and id != 'overlay_ready'):
							#print('Running the script, as ID\'s are not equal.')
							setAttrScript = 'arguments[0].setAttribute(\'id\', \'overlay_ready\')'
							driver.execute_script(setAttrScript, magnifying_glass[i])
							newList.append(magnifying_glass[i])
							print(magnifying_glass[0].get_attribute('innerText'))
					#print('Scanner Released Rights')
					rewardsListNew = newList
					lock.release()
			except:
				print('Nothing found yet')
				sleep(1)
	except Exception as e:
		print(e)
	
try:
	stringLabel.set('Jhrek Is At Peace')
	threading.Thread(target=run_quiet_chrome).start()
	print('Setting up label')
	label = tkinter.Label(root, textvariable=stringLabel, font=('Arial','12', 'bold'), fg='black', bg='whitesmoke', highlightbackground="black")
	label.master.overrideredirect(True)
	label.master.geometry("+10+10")
	label.master.lift()
	label.master.wm_attributes("-topmost", True)
	label.master.wm_attributes("-disabled", True)
	label.master.wm_attributes("-transparentcolor", "white")
	print('Packing')
	label.pack()
	threading.Thread(target=run_watcher).start()
except Exception as e:
	print(e)
tkinter.mainloop()