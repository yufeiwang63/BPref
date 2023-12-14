import os
os.system("rsync -avrz --exclude='__pycache__' --exclude='data' --exclude='exp/' ./ autobot:/project_data/held/yufeiw2/BPref/")
