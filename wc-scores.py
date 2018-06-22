import time
import datetime
import os
import requests
import json
import sys
'''
Quick and dirty way to get wc scores in the terminal. This python script uses the World Cup API from Software for Good (https://softwareforgood.com/) to get live updates about a match and other
matches happening today. This script querries info on the current match and the other matches happening today and displays in the terminal. 
Script then clears the terminal (WINDOWS) with displays the latest updated data every 70 seconds. 

May need to install these packages:pip install json, pip install requests
To run the script: /path/to/script/python wc-scores.py
To end the script: ctrl-c
'''

def waitForIt(secs = 70):
	time.sleep(secs)

def getStartingMatchTime(utc_match_time):
    # TODO 	
	# utc = datetime.utcnow()
	#utc to local timezone coversion
	utc_now = datetime.datetime.utcnow()

	#positive means UTC is ahead by x time
	utc_diff_factor = datetime.datetime.utcnow() - datetime.datetime.now()

	#utc_time_diff = utc_now - utc_match_time
	

	#if negative time has passed it's in the past, but assume match time is in the future
	return utc_match_time.strftime("%Y-%m-%d");

	#pass

if __name__ == "__main__":
	
	print('\n')

	# print(getStartingMatchTime("2018-06-22 20:00:00"));

	# sys.exit(-1);

	while True:
		try:		
			t = json.loads(requests.get('http://worldcup.sfg.io/matches/today').text)
			r = json.loads(requests.get('http://worldcup.sfg.io/matches/current').text)

			if r :
				print("______________________")
				print("\nCurrent Match LIVE!")
				print("______________________\n")
				for match in r:		
					print('Home Team: ',match['home_team']['code'], ' (', match['home_team']['goals'],'): ')
					events = match['home_team_events']
					if events:
						for event in events:
							print('\n  @', event['time'], ': ', event['type_of_event'],' for ', event['player'])

					print('\nVistor Team: ',match['away_team']['code'], ' (', match['away_team']['goals'],')')
					
					events = match['away_team_events']
					if events:
						for event in events:
							print('\n  @', event['time'], ': ',event['type_of_event'], ' for ', event['player'])

					print('\nGame Time:',match['time'])
					print('\nStatus: ',match['status'])
					print('\nVenu: ', match['venue'])
			else:
				print('Sorry, No Live Match at the Moment :( ')
			
			if t:
				print("\n________________")
				print("\nMatches Today:")
				print("__________________\n")
				for match in t:
					
					status = ''
					start_time = ''
					if match['status'] == 'future' :
						status = 'Yet To Play @ ' #+ getStartingMatchTime(match['datetime'])
						#start_time = 
						#status = 'Yet To Play'
					elif match['status'] == 'completed':
						status = 'DONE!'
					else:
						status = match['status'] #+' @ ' + getStartingMatchTime(match['datetime'])
						#print(match['datetime'])
						#status = match['datetime']
					
					print(match['home_team']['code'], "(", match['home_team']['goals'], ")"," vs ", match['away_team']['code'], "(", match['away_team']['goals'], ") - [" , status, "]")			

			else:
				print('No Matches Today!')

			currentDT = datetime.datetime.now().strftime("%A, %B-%d-%Y %H:%M")

			print('\nCurrent Local Time: ', str(currentDT))

			waitForIt(70)

			#clear screen (windows)
			the_cls = os.system("cls")
			#use: os.system('clear') - for *nix systems
		except KeyboardInterrupt:
			print("\n\n=== Thank You for Tracking WC 2018 Scores! Good Bye! :) ===")
			sys.exit(-1)
		except:
			print('Could not read from API Endpoint . . . retrying in 30 secs')
			waitForIt(30)
