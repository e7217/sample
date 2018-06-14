import os
import time

cmd1 = "sudo sed -i 's/www.google.com/172.16.0.1/g' ./raw_2.py"
cmd2 = 'sudo python -m py_compile raw_2.py'
cmd3 = 'sudo mv raw_2.pyc ../raw_.pyc'
cmd4 = 'cd ..'

os.system(cmd1)
# time.sleep(1)
os.system(cmd2)
# time.sleep(1)
os.system(cmd3)
# time.sleep(1)
os.system(cmd4)
