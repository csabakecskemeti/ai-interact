aiHub Manager 1.0 beta
built by devquasar.com

Configuration 
- API: set your LLM API.
- Shortcut: currently not used
- Prompt prefix: the prefix you wanted to precede the captured information (like: 'fix this', 'summarize this')
Note: to apply new configuration you have to stop and restart the aiHub within the aiHub Manager

  Capture
    Navigate to the desired screen area you're looking for help with
    Hit the [shift] [F1] key combination
    Define the rectangle to capture with your mouse click (click on the 2 imaginary diagonal of the rectangle)
    The prompt will appear in the text area of the app with USER: prefix.
    Status "led" turn orange while LLM is working
  Response
    The response will appear in the text area of the app with BOT: prefix.
    Status "led" turn green on response

What LLM to use?
The tool is agnostic of the LLM. We suggest to leverage local LLM inference with LM Studio <lmstudio.ai>. 

Project readme:
https://github.com/csabakecskemeti/ai-interact/blob/main/README.md
