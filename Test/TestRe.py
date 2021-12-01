import re

s=re.match('【.*】', '【第五章】水电费')
s=s.group(0)
print(type(s))