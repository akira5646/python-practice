import time 
from tqdm import * 
# for i in tqdm(range(int(1000))):
#     print(i)

all = [n*n for n in tqdm(range(1000))]
print(all)