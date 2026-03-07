from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import inspect

def test():
    app = App(token="xoxb-test")
    @app.event("app_mention")
    async def handler(event, say):
        pass
    print("Works")
test()
