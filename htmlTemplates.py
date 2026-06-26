# htmlTemplates.py के अंदर इन दोनों टेम्पलेट्स को ऐसे अपडेट करें:

css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
    align-items: flex-start;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
/* 💡 यह फिक्स है: मैसेज बॉक्स हमेशा नॉर्मल टेक्स्ट की तरह बहेगा */
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
  white-space: normal; /* शब्दों को नीचे बिखरने से रोकता है */
  word-break: break-word;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''