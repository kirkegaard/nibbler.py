import sys
import re
from cobe.brain import Brain

b = Brain(sys.argv[1])
b.start_batch_learning()

line_re = re.compile(r"\[.*\] <.*> (?P<message>.*)")

with open(sys.argv[2]) as f:
    for line in f:
        m = line_re.search(line)
        if not m:
            continue

        data = m.groupdict()
        content = re.sub(r'<@.*?>', '', data['message']).strip()
        print(content)
        b.learn(content)

b.stop_batch_learning()
