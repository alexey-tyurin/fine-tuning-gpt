# GPT-4o-mini Fine-tuning for Hospitality Chatbot Intent Classification

This project demonstrates how to fine-tune GPT-4o-mini models for accuracy and latency optimization
 to achieve higher accuracy than with GPT-4.1 with much lower cost.
It uses real life scenario - intent classification for hospitality chatbots working with ambiguous guest queries.

## 🎯 Project Goal

The primary goal is to improve the accuracy and efficiency of hospitality chatbots in identifying the correct intent behind guest requests, even when those requests are ambiguously phrased. By fine-tuning smaller models like GPT-4o-mini, we can achieve performance comparable to larger models while reducing latency and costs.

## 🔍 Intent Classification Problem

Hospitality chatbots often struggle with correctly interpreting guest requests that are vague or ambiguous. For example, when a guest says "I'm concerned about my belongings after I officially conclude my stay," the chatbot needs to correctly identify this as a "Request late check-out" intent rather than confusing it with luggage storage or other services.

This project addresses this challenge by fine-tuning models to better recognize 40 different hospitality-related intents.

## 💼 Benefits of this project

- **Complete Fine-tuning Workflow**: Working code for synthetic data generation, fine-tuning, evaluation
- **Automated Data Generation**: Scripts to generate synthetic training data for supervised fine-tuning (SFT)
- **Fine-tuning Optimization**: Techniques to balance accuracy and latency
- **Large-to-Small Model Distillation**: Leverage knowledge from larger models to improve smaller ones
- **OpenAI Fine-tuning API Integration**: Structured fine-tuning framework to improve models
- **OpenAI Evals API Integration**: Structured evaluation framework to measure model performance
- **Real-world Use Case**: Addresses an actual problem faced by production chatbots

## 📊 Fine-tuning Benefits vs Prompting

| Aspect | Fine-tuning Advantage                                     |
|--------|-----------------------------------------------------------|
| Latency | Faster responses                                          |
| Cost | Reduced token usage and model size                        |
| Stability | More consistent results across various phrasings          |
| Accuracy | Better performance on domain-specific tasks               |
| Efficiency | Achieve same accuracy with a smaller model                |
| Scale | Can train on thousands of examples (beyond prompt limits) |
| Token Economy | Shorter prompts reduce token consumption                  |

## 🛠️ Project Structure

```
├── README.md                     # Project documentation
├── create_jsonl.py               # Script to create file with test data (e.g. tests200_2.jsonl) out of mapping file to be used for SFT
├── evals100.jsonl                # 100 ambiguous messages and their correct intents to be used with OpenAI Evals
├── generate_4.1_lists_20.py      # Script to generate vague messages using GPT-4.1 and test them with gpt-4o-mini locally
├── messages_mappings100.py       # 100 ambiguous messages and their correct intents
├── messages_mappings200.py       # 200 ambiguous messages and their correct intents
├── messages_mappings200_2.py     # Additional 200 ambiguous messages for testing
├── openai_eval.py                # Script to run evaluations through OpenAI API
├── openai_ft.py                  # Script to perform supervised fine-tuning (SFT)
├── requirements.txt              # Requirements for this project
├── test_intent_4o-mini_200.py    # Script to generate responses with gpt-4o-mini and compare them with correct ones locally
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key with access to fine-tuning capabilities
- pip packages: openai

### Setup

1. Clone this repository
```bash
git clone https://github.com/alexey-tyurin/fine-tuning-gpt.git
cd gpt4o-mini-finetuning
```

2. Set up your OpenAI API key as an environment variable
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Install required dependencies
```bash
pip install -r requirements.txt
```

### Supervised Fine-tuning (SFT)

1. Run the fine-tuning script
```bash
python openai_ft.py --all
```

Or run steps individually:
```bash
python openai_ft.py --upload      # Upload training data
python openai_ft.py --create      # Create fine-tuning job
python openai_ft.py --status      # Check status
python openai_ft.py --analyze     # Analyze results
```

### Evaluation

Run the evaluation to test model performance:
```bash
python openai_eval.py --all
```


## 📝 Results

Our experiments show that fine-tuned GPT-4o-mini models can achieve:
- 130% accuracy improvement on intent classification tasks
- Reduced token consumption and associated costs
- More consistent responses across various query phrasings

## 🔄 Workflow

1. **Data Preparation**: Create training data with ambiguous messages and correct intent mappings
2. **Initial Fine-tuning**: Perform supervised fine-tuning using the OpenAI API
3. **Evaluation**: Test the model against a held-out test set
4. **Deployment**: Integrate the fine-tuned model into your chatbot


## 🙏 Acknowledgements

- OpenAI for providing fine-tuning capabilities

## Contact Information

For any questions or feedback, please contact Alexey Tyurin at altyurin3@gmail.com.

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
