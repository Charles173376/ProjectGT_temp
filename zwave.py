import rest

base_url = 'http://192.168.1.120:8083'

# login credentials, to be replaced with the right ones
# N.B. authentication can be disabled from the configuration of the 'Z-Wave Network Access' app
# from the website available at 'base_url'
username = "admin"
password = "raspberry"

# get z-wave devices
all_devices = rest.send(url=base_url + '/ZWaveAPI/Data/0', auth=(username, password))

# without auth, omit the last parameter
#print the lumicity
lumVal = all_devices['devices']['3']['instances']['0']['commandClasses']['49']['data']['3']['val']['value']
