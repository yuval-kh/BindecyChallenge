import frida
import sys

def on_message(message,data):
    print(message)



code="""Java.perform(function(){
   var Activity = Java.use("org.thoughtcrime.securesms.messages.MessageContentProcessor");
   Activity.shouldIgnore.overload("org.whispersystems.signalservice.api.messages.SignalServiceContent", "org.thoughtcrime.securesms.recipients.Recipient", "org.thoughtcrime.securesms.recipients.Recipient" ).implementation = function(a,b,c){

       const content = Java.cast(a, Java.use("org.whispersystems.signalservice.api.messages.SignalServiceContent"));
        const isTyping = content.getTypingMessage().isPresent();
        const dataIsPresent = content.getDataMessage().isPresent()
        var result = this.shouldIgnore(a,b,c);

        if(isTyping == false && result == false && dataIsPresent){
            console.log("New Message is receieved");
        }


        return result;
      }
      console.log("the code is successfully injected");
});
"""

session = frida.get_usb_device().attach("Signal");
script=session.create_script(code)
script.on('message',on_message)
print("executing js code")
script.load()
sys.stdin.read()
