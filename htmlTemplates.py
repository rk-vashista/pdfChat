css = '''
<style>
body {
    background-color: #f0f2f6;
    font-family: 'Roboto', sans-serif;
}
.chat-message {
    padding: 1.5rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    display: flex;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 15%;
}
.chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff;
}
.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #fff;
    font-size: 1rem;
    line-height: 1.5;
}
.stTextInput > div > div > input {
    background-color: #f0f2f6;
    color: #2b313e;
    border-radius: 0.5rem;
}
.stButton > button {
    border-radius: 0.5rem;
    font-weight: 500;
}
.stTextArea > div > div > textarea {
    background-color: #f0f2f6;
    color: #2b313e;
    border-radius: 0.5rem;
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
        <img src="https://ibb.co/NKHKd96">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''