import time
import random
import os
from datetime import datetime

#constants
password = "astraindia"
threat_level = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

missile_type = ["Interception", "Surface-to-Air", "Heat-Seeker"]
log_file = "defence_log.txt"
radar_size = 20

# initialize log
with open(log_file, "w") as f:
    f.write("=== GMW Missile Defence Log ===\n")
    f.write(f"Session Started: {datetime.now()}\n\n")

def log_event(msg):
    print(msg)
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def authenticate():
    attempts = 3
    while attempts > 0:
        pwd = input("Enter v 3.0 system password: ")
        if pwd == password:
            log_event("Access granted to system.")   
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempt(s) left.") 
    log_event("Access denied. System locked.")
    return False

def generate_threats(n):
    threat = []
    for i in range(n):
        tid = f"TGT-{random.randint(100, 999)}" 
        x, y = random.randint(0, radar_size-1), random.randint(0, radar_size-1)   
        level = random.choice(threat_level)
        countdown = random.randint(8, 20)  
        missile = random.choice(missile_type)   
        threat.append({"id": tid, "x":x, "y":y, "level": level, "countdown": countdown, "missile": missile, "neutralized": False})
    return threat
    
def draw_radar(threats):
    grid = [["-" for _ in range(radar_size)]for _ in range(radar_size)] 
    for t in threats:
        if not t["neutralized"]:
            grid[t["y"]][t["x"]] = "x"
    grid[radar_size//2][radar_size//2]= "0"
    print("\n--- Radar Map ---")
    for row in grid:
        print(" ".join(row))
    print("-----------------\n")            

def ask_permission(threat):
    permission = input(f"Permission to launch at {threat['id']} (yes/no)? ").strip().lower()
    if permission == "yes":
        log_event(f"Permission granted to launch at {threat['id']}.")
        return True
    else:
        log_event(f"Permission denied for {threat['id']}. Threat still active!") 
        return False 
# time.sleep(2) 

def launch_missile(threat):
    print(f"\aLaunching {threat['missile']} missile at {threat['id']} ({threat['x']}, {threat['y']})...")  
    time.sleep(4)  
    print("Target neutralized.")
    log_event(f"Missile launched at {threat['id']} using {threat['missile']}. Target neutralized.")
    threat["neutralized"]= True

#main
if authenticate():
    threat = generate_threats(random.randint(2,10))
    log_event(f"{len(threat)} threats detected on radar.")
    print("\nInitializing radar...")
    time.sleep(4)

    while any(not t["neutralized"] and t["countdown"] > 0 for t in threat):
        draw_radar(threat)
        for t in threat:
            if not t["neutralized"]:
                print(f"{t['id']} | Coords: ({t['x']}, {t['y']}) | Level: {t['level']} | Countdown: {t['countdown']}s") 
                
                
                if t["level"] == "CRITICAL":    
                    log_event(f"CRITICAL danger detected from {t['id']}. Auto-launch engaged.")   
                    launch_missile(t)
                elif t["countdown"] <= 9:
                    log_event(f"Critical countdown on {t['id']}. Auto-launch engaged.")
                    launch_missile(t)
                else:
                    if ask_permission(t):
                        launch_missile(t)
                t["countdown"] -= 1
        time.sleep(4)

print("\n--- SESSION ENDED ---")
log_event("All threas neutralized or countdown expired.")
log_event("Defence system shutting down.\n")

input("\nPress enter to exit....")                            
