import faust
from streaming import events


app = faust.App(id="consumer", broker="kafka://localhost:9092", store="rocksdb://")
# Input topic, NOT managed by Faust
input_topic = app.topic('numtest', internal=False, value_type=events.Tweet)
# Faust will create this topic for us
analyze_topic = app.topic('analyze-topic', internal=True, value_type=events.Sports)
