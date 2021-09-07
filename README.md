Requires paramiko

Runs a list of commands on the F5 and writes the result to a file for each F5. The equivalent of a show run is here by default. Also runs a UCS backup weekly.

F5 login info is stored in code (list of dict rows). This is just to get you up and running with the basics. You can then fit this in with however you manage your device passwords - cli arg, env variables etc.

DOUCS = False - set this if you want to always get a ucs backup. By default this runs once a week.

UCSDAY = 5      # 5 == Saturday - the day to run the ucs on.

BACKUPS = r'C:\ConfigBackups\F5\backups' - where to copy the configs to on the local system.

UCSPATH = '/var/' - path on the F5 to store the ucs before copying it off.

By default the same filename is used so it just gets overwritten each time and thus prevents the f5 filling up with UCS files. You can change this to be a filename with the date and then run another command to clear off old ones. See the commented code at the end.

