# ASTRA (AIR SHEILDING & THREAT RESPONSE ALGORITHM) Version 2.0

import time
import random

def print_separator():
    print("\n" + "-"*50 + "\n")

print("Initializing Multi-Missile Radar Defence System..." )
time.sleep(3)
print("Scanning airspace for unidentified objects...\n")
time.sleep(3)

# Generate random number of incoming missile(2 t0 12)
missile_count = random.randint(2,12)
print(f"ALERT: {missile_count} Incoming Missile(s) Detected!\n")
time.sleep(2)

#status logs
intercepted = 0
failed = 0
denied = 0

#handel each missile
for i in range(1, missile_count + 1):
    print_separator()
    print(f"Target Accquired")
    time.sleep(1)

    #assign threat level
    threat_level = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    print(f"AI Analysis: Threat Level = {threat_level}")
    time.sleep(1)

    if threat_level in ["HIGH", "CRITICAL"]:
        print("Attempting Lock-On...")
        time.sleep(2)
        lock_success = True

        if lock_success:
            print("Target LOCKED.")
            time.sleep(1)
            print("Requesting Launch Permision...")
            permission = input("Grant Permission? (yes/no): ").strip().lower()

            if permission == "yes":
                print("\nLaunching Interceptor Missile...")
                for count in range(5, 0, -1):
                    print(f"Launching in {count}...")
                    time.sleep(1)
                    intercept_success = random.choice([True, True, True, False])
                    if intercept_success:
                        print("Target Neutralized Successfully.")
                        intercepted += 1
                        break
                    else:
                        print("Interceptor Missed. Impact Likely.") 
                        failed += 1
                else:
                    print("\nReloading")  
                    
        else:
            print("Locked Failed. Unable to Track Traget.")
            failed += 1
    else:
        print("Threat Level LOW. Monitoring without engagement.") 
        time.sleep(2)       

print_separator()
print("Final Defence Report:")
print(f"Intercepted Threats: {intercepted}")
print(f"Failed to Intercept: {failed}")
print(f"Denied Launches: {denied}")
print("Airspace Monitoring Countinoues...")
print("System Standby Mode Activated.")

input("\npress enter to exit...")