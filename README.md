Roman Urdu Poetry Generator
Welcome to the Roman Urdu Poetry Generator repository! This project is an end-to-end solution that scrapes Roman Urdu poetry from Rekhta.org, trains a deep learning model (Stacked LSTM) to learn poetic patterns, and deploys an interactive Gradio UI for text generation.

Features
Data Scraping: Python script that extracts poetry from Rekhta.org and stores it in urdu_poetry.csv.
Data Preprocessing: Combines and cleans scraped data, builds a character-level vocabulary.
Deep Learning Model: A Stacked LSTM architecture implemented in PyTorch with mixed precision training and gradient clipping.
Interactive UI: A Gradio-based frontend that allows users to generate poetry by providing a starting phrase and adjusting parameters like length and temperature.

How to Run

Clone the Repository:
git clone https://github.com/yourusername/RomanUrduPoetryGenerator.git
cd RomanUrduPoetryGenerator

Install Dependencies:
pip install -r requirements.txt

Data Scraping:
Run the scraping script to generate urdu_poetry.csv:
python scraping_code.py

Model Training:
Train the model using the provided Jupyter Notebook or training script:
python train_model.py
This will generate a file named poetry_generator_epoch_20.pth in the working directory.

Launch the UI:
Start the Gradio UI:
python PoetryGeneratorGradioUI.py

Open the provided URL in your browser to interact with the poetry generator.
Contributing
Feel free to submit pull requests or open issues. Feedback and contributions are welcome!
