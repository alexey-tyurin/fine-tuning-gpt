import os
import openai
import json
from datetime import datetime
# from messages_mappings200 import vague_messages, correct_mappings, intention_names
# from messages_mappings200_2 import vague_messages, correct_mappings, intention_names
from messages_mappings100 import vague_messages, correct_mappings, intention_names

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=openai_api_key)

# System prompt for the hospitality chatbot
system_prompt = """You are an advanced hospitality chatbot for a premium hotel chain. Your primary function is to analyze user messages and accurately identify their main intention from a predefined list of 40 possible intentions. Follow these guidelines:

1. CORE FUNCTION: For each user message, identify exactly ONE primary intention from the list of 40 intentions provided below.

2. ANALYSIS APPROACH:
   - Carefully analyze the entire message for explicit and implicit requests
   - Look for action verbs and specific service mentions
   - Consider context clues and hospitality-specific terminology
   - Identify the most urgent or primary need if multiple are present
   - Focus on what the user wants to accomplish, not just what they're asking about

3. RESPONSE FORMAT:
   - First identify the intention number and name (e.g., "INTENTION: #16 - Request room cleaning")
   - Then explain your reasoning in 1-2 sentences

4. HANDLING AMBIGUITY:
   - If a message contains multiple possible intentions, prioritize based on:
     a) Explicit requests over implicit ones
     b) Time-sensitive needs over general inquiries
     c) Specific service requests over general information
   - Don't get distracted by pleasantries, background information, or storytelling
   - Focus on the actionable request within the message
   - If truly ambiguous, select the intention that addresses the most significant customer need

5. SPECIAL CASES:
   - For complex requests, break down the message to identify the core intention
   - For vague messages, look for context clues about the user's situation
   - For messages with multiple separate requests, identify the primary one first
   - If a request doesn't clearly match any intention, select the closest match or #39 (Request human support)

LIST OF INTENTIONS:
1. Check room availability  
2. Make a reservation / Book a room  
3. Modify reservation  
4. Cancel reservation  
5. Check reservation status  
6. Request early check-in  
7. Request late check-out  
8. Check-in online  
9. Check-out online  
10. Request luggage assistance  
11. Order room service  
12. Book a table at a restaurant  
13. Request menu or dietary information  
14. Ask for breakfast hours or availability  
15. Request minibar refill  
16. Request room cleaning  
17. Request extra towels, toiletries, or pillows  
18. Report an issue in the room  
19. Request laundry service  
20. Request in-room amenities (e.g., iron, hair dryer)  
21. Ask about local attractions or tours  
22. Request a wake-up call  
23. Ask for taxi or shuttle service  
24. Ask about hotel policies  
25. Request spa or gym appointment  
26. Ask for invoice or receipt  
27. Query charges on the bill  
28. Change payment method  
29. Split bill  
30. Pre-authorize payment or deposit  
31. Ask for Wi-Fi access or help  
32. Ask about facility opening hours  
33. Request parking information  
34. Ask about pet policy  
35. Ask about smoking policy  
36. Leave a review or feedback  
37. Report a complaint  
38. Ask to speak to a manager  
39. Request human support or live agent  
40. Ask for help using the chatbot"""

def send_prompt_to_gpt(prompt, system_message=system_prompt, model="gpt-4o-mini"):
    """
    Send a prompt to the GPT model and return the response.

    Args:
        prompt (str): The prompt to send to the model
        system_message (str): The system message to use
        model (str): The model to use (default: gpt-3.5-turbo)

    Returns:
        str: The model's response
    """
    try:
        # Create a chat completion request using the new API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            # temperature=0.7,
            max_tokens=1000,
            # top_p=1.0,
            # frequency_penalty=0.0,
            # presence_penalty=0.0
        )

        # Extract the response text
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        return f"Error: {str(e)}"

def extract_intention(response):
    """
    Extract the intention number from the chatbot's response.

    Args:
        response (str): The chatbot's response

    Returns:
        str: The extracted intention number or None if not found
    """
    # Look for patterns like "INTENTION: #16 - Request room cleaning" or variations
    lines = response.split('\n')
    for line in lines:
        if "INTENTION:" in line or "intention:" in line:
            parts = line.split('#')
            if len(parts) > 1:
                # Extract the number and text after the #
                intention_part = parts[1].strip()
                # If there's a space or dash, get just the number
                if ' ' in intention_part:
                    intention_number = intention_part.split(' ')[0]
                elif '-' in intention_part:
                    intention_number = intention_part.split('-')[0]
                else:
                    intention_number = intention_part
                return intention_number.strip()

    # If the above doesn't work, try to find any number preceded by #
    import re
    match = re.search(r'#(\d+)', response)
    if match:
        return match.group(1)

    return None

def main():
    # Timestamp for the results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"hospitality_chatbot_test_results_{timestamp}.txt"

    print(f"Testing hospitality chatbot with {len(vague_messages)} vague messages...")
    print(f"Results will be saved to {results_file}")

    # Dictionary to store results
    results = {
        "total_messages": len(vague_messages),
        "correct_mappings": 0,
        "incorrect_mappings": 0,
        "detailed_results": []
    }

    # Process each message
    for i, (message, correct_mapping) in enumerate(zip(vague_messages, correct_mappings)):
        print(f"\nProcessing message {i+1}/{len(vague_messages)}")

        # Get the correct intention name from the mapping number
        correct_number = str(correct_mapping)
        correct_name = intention_names.get(int(correct_number), "Unknown")
        correct_mapping_str = f"{correct_number} - {correct_name}"

        # Send the message to the chatbot
        response = send_prompt_to_gpt(message)

        # Extract the intention from the response
        extracted_intention = extract_intention(response)

        # Determine if the mapping is correct
        is_correct = extracted_intention == correct_number if extracted_intention else False

        # Store the result
        result_entry = {
            "message": message,
            "correct_mapping": correct_mapping_str,
            "chatbot_response": response,
            "extracted_intention": extracted_intention,
            "is_correct": is_correct
        }

        results["detailed_results"].append(result_entry)

        if is_correct:
            results["correct_mappings"] += 1
        else:
            results["incorrect_mappings"] += 1

        # Print progress
        print(f"Message: {message}")
        print(f"Correct mapping: {correct_mapping_str}")
        print(f"Extracted intention: {extracted_intention}")
        print(f"Is correct: {is_correct}")

    # Calculate accuracy
    accuracy = results["correct_mappings"] / results["total_messages"] if results["total_messages"] > 0 else 0
    results["accuracy"] = accuracy

    # Save results to file
    with open(results_file, 'w') as f:
        f.write(f"Hospitality Chatbot Test Results - {timestamp}\n")
        f.write(f"Total messages: {results['total_messages']}\n")
        f.write(f"Correct mappings: {results['correct_mappings']}\n")
        f.write(f"Incorrect mappings: {results['incorrect_mappings']}\n")
        f.write(f"Accuracy: {accuracy:.2%}\n\n")

        for i, result in enumerate(results["detailed_results"]):
            f.write(f"=== Message {i+1} ===\n")
            f.write(f"Message: {result['message']}\n")
            f.write(f"Correct mapping: {result['correct_mapping']}\n")
            f.write(f"Extracted intention: {result['extracted_intention']}\n")
            f.write(f"Is correct: {result['is_correct']}\n")
            f.write(f"Chatbot response:\n{result['chatbot_response']}\n\n")

    print(f"\nTesting completed!")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Complete results saved to {results_file}")

if __name__ == "__main__":
    main()