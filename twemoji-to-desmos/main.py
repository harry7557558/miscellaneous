import json

start = "var s=Calc.getState();s['expressions']['list']="
end = ";Calc.setState(s);"

content = open(".desmos", "r").read()
content = content[len(start):len(content)-len(end)]
content = json.loads(content)
print(len(content))
content = content[:12000]
content = json.dumps(content).replace(' ', '')
content = start + content + end
open(".desmos1", "w").write(content)
