import gradio as gr
import torch
import torch.nn as nn
import numpy as np
import pandas as pd

# ==============================================================
# STEP 1: Load the Vocabulary and Model Components
# ==============================================================

# Load the dataset (ensure urdu_poetry.csv is in the working directory)
df = pd.read_csv("urdu_poetry.csv", encoding="utf-8")

def is_valid_row(text):
    if isinstance(text, str):
        text = text.strip()
        return text and not text.startswith("###")
    return False

poetry_lines = df["poetry"][df["poetry"].apply(is_valid_row)].tolist()
text_corpus = "\n".join(poetry_lines)

print(f"Total characters in dataset: {len(text_corpus)}")

# Create character-level vocabulary and mappings
chars = sorted(set(text_corpus))
vocab_size = len(chars)
print(f"Vocabulary size: {vocab_size}")

char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for ch, i in char_to_idx.items()}

# ==============================================================
# STEP 2: Define the Model Architecture (StackedLSTM)
# ==============================================================

class StackedLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers):
        super(StackedLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden):
        x = self.embedding(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden

    def init_hidden(self, batch_size, device):
        # Note: num_layers and hidden_dim are taken from global variables set below
        return (torch.zeros(num_layers, batch_size, hidden_dim).to(device),
                torch.zeros(num_layers, batch_size, hidden_dim).to(device))

# Hyperparameters for the model (should match training)
embedding_dim = 128
hidden_dim = 256
num_layers = 2

# Set device and initialize the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = StackedLSTM(vocab_size, embedding_dim, hidden_dim, num_layers).to(device)

# Load the trained model weights (ensure the file exists in the working directory)
model.load_state_dict(torch.load("poetry_generator_epoch_20.pth", map_location=device))
model.eval()

# ==============================================================
# STEP 3: Define the Text Generation Function
# ==============================================================

def generate_text_interface(start_text, length, temperature):
    """
    Generates Roman Urdu poetry using the trained StackedLSTM model.
    
    Parameters:
    - start_text: The prompt to start the poetry.
    - length: The number of characters to generate.
    - temperature: Controls creativity; higher values yield more diverse outputs.
    
    Returns:
    - generated_text: The complete generated poetry.
    """
    model.eval()
    if not start_text:
        start_text = "Mohabbat"
    # Limit starting text to 100 characters to avoid long inputs
    start_text = start_text.strip()[:100]
    
    # Convert the starting text into tensor indices
    input_seq = torch.tensor([char_to_idx.get(ch, 0) for ch in start_text], dtype=torch.long).unsqueeze(0).to(device)
    hidden = model.init_hidden(1, device)
    generated_text = start_text

    for _ in range(length):
        output, hidden = model(input_seq, hidden)
        # Adjust logits by temperature for creativity control
        logits = output[:, -1, :] / temperature
        probs = torch.softmax(logits, dim=-1).detach().cpu().numpy().ravel()
        next_idx = np.random.choice(len(probs), p=probs)
        next_char = idx_to_char[next_idx]
        generated_text += next_char
        # Update input sequence with a sliding window approach
        input_seq = torch.cat([input_seq, torch.tensor([[next_idx]], dtype=torch.long).to(device)], dim=1)[:, 1:]
    
    return generated_text

# ==============================================================
# STEP 4: Build the Extensive Gradio UI Frontend
# ==============================================================

with gr.Blocks(title="Roman Urdu Poetry Generator") as demo:
    gr.Markdown("## Roman Urdu Poetry Generator")
    gr.Markdown(
        """
        Welcome to the Roman Urdu Poetry Generator! This application uses a pre-trained Stacked LSTM model 
        to generate beautiful, creative poetry in Roman Urdu. 
        Simply enter a starting phrase, adjust the parameters, and click **Generate Poetry**.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            start_text_input = gr.Textbox(label="Starting Phrase", placeholder="Enter a starting phrase (e.g., 'Mohabbat')", lines=1)
            length_slider = gr.Slider(label="Poetry Length (Characters)", minimum=100, maximum=1000, value=300, step=50)
            temperature_slider = gr.Slider(label="Temperature (Creativeness)", minimum=0.1, maximum=2.0, value=1.0, step=0.1)
            generate_btn = gr.Button("Generate Poetry", variant="primary")
        with gr.Column(scale=2):
            output_text = gr.Textbox(label="Generated Poetry", lines=15)
    
    with gr.Accordion("Advanced Options", open=False):
        gr.Markdown(
            """
            **Advanced Options:**
            - **Temperature:** A higher temperature (e.g., 1.5 or 2.0) makes the output more diverse and creative,
              but may also produce less coherent results.
            - **Poetry Length:** Adjust the total number of characters to be generated.
            """
        )
    
    gr.Markdown("### Example Starting Phrases")
    gr.Examples(
        examples=[
            ["Mohabbat"],
            ["Ishq ka"],
            ["Dil mein"],
        ],
        inputs=start_text_input,
        label="Click on an example to auto-fill the starting phrase."
    )
    
    generate_btn.click(
        fn=generate_text_interface,
        inputs=[start_text_input, length_slider, temperature_slider],
        outputs=output_text
    )
    
    gr.Markdown(
        """
        **Instructions:**
        1. Enter a starting phrase in Roman Urdu.
        2. Adjust the length and temperature sliders as desired.
        3. Click **Generate Poetry** to produce new poetry.
        4. Enjoy the generated text and share your creations!
        """
    )

# ==============================================================
# STEP 5: Launch the Gradio Interface
# ==============================================================

if __name__ == "__main__":
    demo.launch(share=True, server_name="127.0.0.1", server_port=7860)
