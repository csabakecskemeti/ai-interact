# [aihub](https://devquasar.com/aihub/)
aihub project intends to change the way how do we interact with LLMs. Today many tools offer integration to all different models, and various chat applications are available online and locally.
This provides a very scattered picture for end users and applications without AI integration require extra effort to get help with. aihub offers a more natural way to interface with generative AI 
models that are app agnostic, by sharing a screen portion with the model where the user seeks help. 

How it works
===================
A small Python application with a minimal GUI runs in the background. The application is API-integrated with an LLM of your choice (our recommendation for local inference is [LMStudio](https://lmstudio.ai/))
and running a keyboard listener.
With the [SHIFT][F1] keyboard shortcut the user initiates the capture mode. By defining an imaginary rectangle with 2 mouse clicks (define 2 diagonal corners of the rectangle) the code captures an image
from anywhere on the screen. Then these images are processed by a locally running text extraction model: Tesseract, and the result text will be sent to the LLM with the preconfigured prefix.
We've found that LLMs can handle the not perfect text extraction of Tesseract.  

Examples
===================
### Coding issue

![demo_problem2](https://github.com/csabakecskemeti/ai-interact/assets/12419949/3b88ce31-d606-493b-80e9-75262d642d5c)
![demo_result2](https://github.com/csabakecskemeti/ai-interact/assets/12419949/34adb9ec-cb3c-4911-857f-7422e00b2aa4)

### Summarization

![demo_summary_problem](https://github.com/csabakecskemeti/ai-interact/assets/12419949/95cd5e1f-df86-407e-93aa-8a7358362401)
![demo_summary_result](https://github.com/csabakecskemeti/ai-interact/assets/12419949/941a2d9c-7d8b-430f-a113-266499697177)



Supported Platforms
===================

  * MacOS

Requirements
============

  * Python 3.11.7
  * Tesseract
  * Open AI API compatible LLVM service access

Install
=======

  * Install dependencies:
```
$ brew install pyenv tesseract
```
  * Setup `pyenv`: Please follow the instructions described at https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv

  * Install Python environment:
```
$ pyenv install 3.11.7
$ pyenv virtualenv 3.11.7 aihub
$ pyenv activate aihub
$ pip install -r requirements.txt
```

  * Generate the Protocol Buffer Python stubs:

```
python -m grpc_tools.protoc -I. --python_out=./aihub --pyi_out=./aihub --grpc_python_out=./aihub aihub.proto
```

  * Configure LLVM service access:
```
$ vi aihub/config.json
[Perform necessary edit]
```

  * Start the app:
```
$ cd aihub && python -m aihub_bootstrap
```

Usage
=====

  * Press `Shift + F1`
  * Click the top left, then the bottom right corner of an error message
  * Read the solution in UI window

### Config via GUI

![aihub_config](https://github.com/csabakecskemeti/ai-interact/assets/12419949/887a290a-e628-4187-94f3-b7e98110f1e4)
