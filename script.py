import requests
from datetime import datetime
import hashlib
import pandas as pd

# h = hashlib.new('sha256')
# b = bytes('secret', 'utf-8')
# h.update(b)
# print(h.hexdigest())
# #
# response = requests.get(f'https://mrcool-greenbank.herokuapp.com/clients/auth?login=nick&password=12314')
# data = response.json()
#
data = pd.DataFrame(columns=('number', 'type', 'amount'))
data['bank'] = 1

print(data)

#print(datetime.now().month .strftime("%Y-%m-%d"))