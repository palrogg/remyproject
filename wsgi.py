from flask import Flask, request
from fbmq import Page

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

try:
    PAGE_ACCESS_TOKEN
except NameError:
    print("Access token was NOT defined!")
    PAGE_ACCESS_TOKEN = 'dummy'
    
page = Page(PAGE_ACCESS_TOKEN)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
    page.handle_webhook(request.get_data(as_text=True))
    return "ok"

@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    page.send(sender_id, "merci! votre message est '%s'" % message)

@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")
  
if __name__ == "__main__":
    app.run()