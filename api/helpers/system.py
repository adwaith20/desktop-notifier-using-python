import psutil

def get_battery_info():
    battery = psutil.sensors_battery()
    
    if battery is None:
        return "Battery information not available"
    
    percent = battery.percent
    power_plugged = battery.power_plugged
    secsleft = battery.secsleft
    
    if power_plugged:
        status = "Plugged In"
    else:
        status = "Not Plugged In"
    
    return {
        "percent": percent,
        "power_plugged": power_plugged,
        "status": status,
        "seconds_left": secsleft
    }

if __name__ == "__main__":
    battery_info = get_battery_info()
    print(battery_info)
