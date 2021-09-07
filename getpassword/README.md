Create your password file with the following format:

all:root:default_root_pw
all:admin:default_admin_pw
all:enable:default_enable_pw
device1:admin:dev1_pw
device2:backup_user:dev2_pw

"all" will be used if there is no specific match for the device. Specific passwords need to be populate for each device that does not use a default password.

invoke as follows:
password = get_password('device1','account-name')

getpasswordsenc uses an encrypted file. Specify the input file in clear text (same structure as the file used for getpassword.py) and run the module, it will detect the new file and encrypt and remove the old file (with prompts).
