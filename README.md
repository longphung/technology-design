# Swinburne Technology Design Group Project: AI FAQ Answerer

## Introduction
Example of fetching faq from Swinburne online.
Attached is example.gif: ![Swinburne FAQ Fetch](./example.gif "Swinburne FAQ Fetch")

### Requirements:
- Python 3.6+
- Virtualenv (recommended)

## Installation
**Note:** This project uses Python 3.6+. If you have multiple versions of Python installed, you may need to use `python3` and `pip3` instead of `python` and `pip` in the following instructions.
The following steps are instructions for Linux and macOS. If you are using Windows, you may need to adapt these instructions.

1. Clone this repository:

```bash
git clone git@github.com:longphung/technology-design.git
cd technology-design
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage
The default Flask port is 5000. I had to use 8000 because macOS uses port 5000 for Apple Airplay Receiver.

1. Run the application:

```bash
python app.py
```

By default, the application will run on localhost with port 8000.
Open a web browser and go to http://localhost:8000 to use the chat interface.
To access the FAQs, go to http://localhost:8000/faqs.

