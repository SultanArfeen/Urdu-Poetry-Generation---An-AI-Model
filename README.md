# Roman Urdu Poetry Generator

Welcome to my Roman Urdu Poetry Generator project. In this project, I explore how traditional Urdu poetry can be generated using modern generative AI techniques. I scraped data from Rekhta.org for a rich collection of poetry, trained a custom AI model using a Stacked LSTM architecture, and built an interactive user interface with Gradio. The application is deployed on Hugging Face Spaces, and the complete code is available on GitHub. I have also documented the entire process on my Medium blog post and shared a summary on LinkedIn.

## Project Overview

In this project, I undertook the following steps:
- **Data Collection:** I developed a Python script to scrape poetry from Rekhta.org and stored the data in a CSV file named `urdu_poetry.csv`.
- **Model Training:** I trained a character-level language model using a Stacked LSTM. The model's weights are saved in `poetry_generator_epoch_20.pth`.
- **Interactive Interface:** I built a Gradio-based user interface that allows users to input a starting phrase, adjust parameters such as output length and temperature, and generate unique Roman Urdu poetry.
- **Deployment:** The application is deployed on Hugging Face Spaces, making it publicly accessible.

## How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SultanArfeen/Urdu-Poetry-Generation---An-AI-Model.git
   cd Urdu-Poetry-Generation---An-AI-Model
   
2. **Install Dependencies:**
 ```bash
pip install -r requirements.txt
```
The requirements.txt file includes all necessary libraries such as Gradio, Torch, Transformers, Pandas, NumPy, BeautifulSoup4, and Requests.

3. **Run the Gradio Interface:**
```bash
python app.py
```
This will launch the application locally (typically accessible at http://127.0.0.1:7860). When deployed on Hugging Face Spaces, the app is launched automatically without specifying server parameters.
Example Generated Output

An example of generated poetry might be:
```bash
Ishq ki shab, dil ka alam,
Raat bhar noor hai, subah se pehle hi.
```
Each generation produces a unique output based on the provided prompt and parameters.

Deployment
Hugging Face Spaces:
The live demo of the application is available at:
https://huggingface.co/spaces/ArfeenSKD/roman-urdu-poetry-generator
GitHub Repository:
The complete project code and details can be found at:
https://github.com/SultanArfeen/Urdu-Poetry-Generation---An-AI-Model
Medium Blog Post:
A detailed account of the project, including data scraping, model training, and deployment insights, is available here:
https://medium.com/@sultanularfeen/urdu-poetry-generation-an-ai-model-52118c57f7b5
LinkedIn Post:
A summary of the project and my key learnings is available on LinkedIn:

Contributing
Contributions, suggestions, and improvements are welcome. Please feel free to open issues or submit pull requests in this repository.

License
This project is licensed under the MIT License.

Thank you for exploring my Roman Urdu Poetry Generator project. I hope it inspires you to explore the creative potential of generative AI.
