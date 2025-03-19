# Conversational Chatbot

This project is a Streamlit-based conversational chatbot that uses OpenAI's API to generate responses. The chatbot can transcribe audio input, generate text responses, and convert text responses back to audio.

## Features

- **Audio Input**: Record audio input using your microphone.
- **Speech-to-Text**: Convert audio input to text using OpenAI's Whisper model.
- **Conversational AI**: Generate responses using OpenAI's GPT-3.5-turbo model.
- **Text-to-Speech**: Convert text responses to audio using OpenAI's TTS model.
- **Interactive UI**: Built with Streamlit for a user-friendly interface.

## Prerequisites

- Python 3.7 or higher
- An OpenAI API key

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/conversational-chatbot.git
   cd conversational-chatbot

2. **Create a virtual environment (optional but recommended)**:

```BASH

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required packages**:

```BASH

pip install -r requirements.txt
```

## Configuration
1. **Set up your OpenAI API key**:
you can enter the API key directly in the Streamlit app when prompted.

## Running the Chatbot
1. **Start the Streamlit app**:

```BASH

streamlit run app.py
```

2. **Interact with the chatbot**:

- Enter your OpenAI API key when prompted.
- Use the microphone to record your question or statement by clicking the 'Click to Record' button.
- The chatbot will transcribe your audio, generate a response, and play the response back to you.

## Troubleshooting
- Ensure your OpenAI API key is valid and has the necessary permissions.
- Check your internet connection, as the app requires access to OpenAI's API.
- If you encounter issues with audio recording, ensure your microphone is properly configured.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments
Streamlit for the interactive UI framework.
OpenAI for the powerful language models and APIs.
