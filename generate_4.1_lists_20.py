import os
import openai
import json
from datetime import datetime
import time

openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=openai_api_key)

# Function to generate vague messages using GPT-4.1
def generate_vague_messages(num_messages=20):
    """
    Generate vague messages using GPT-4.1 that would be difficult for GPT-4o-mini to map correctly.

    Args:
        num_messages (int): Number of messages to generate

    Returns:
        dict: A dictionary containing generated messages and their correct mappings
    """

    system_prompt = """You are an expert in creating challenging test cases for AI language models. 
   Your task is to generate vague, ambiguous messages that would be difficult for a hospitality chatbot (specifically GPT-4o-mini) to correctly classify.
   
   For each message:
   1. Create a vague user message for a hotel chatbot that contains subtle context clues pointing to a specific intention
   2. The message should be deliberately ambiguous and indirect, avoiding obvious keywords
   3. The message might include distractions or multiple possible interpretations
   4. Specify which ONE of the 40 intentions listed below is the correct mapping
   5. Briefly explain why this is the correct intention (this will be hidden from the test)
   
   Format your response as a JSON list of objects with the following structure:
   [
       {
           "message": "The vague message text...",
           "correct_mapping": "X - Intention name",
           "explanation": "Brief explanation of why this is the correct mapping"
       },
       ...
   ]
   
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

    user_prompt = f"""Generate {num_messages} challenging, vague messages that would be difficult for a hospitality chatbot (GPT-4o-mini) to classify correctly.

   These messages should:
   - Be ambiguous enough that the correct intention is not immediately obvious
   - Contain subtle clues to the true intention
   - Avoid direct mention of the intention name or obvious keywords
   - Include potential distractions or red herrings
   - Appear realistic as something a hotel guest might actually write
   
   Make sure to select a diverse range of intentions from the list of 40 provided.
   
   Return your response in the exact JSON format specified in the system prompt."""

    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,  # Higher temperature for more creative variations
            max_tokens=3000,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.2
        )

        # Extract the response text
        response_text = response.choices[0].message.content

        # Clean up the response to ensure it's valid JSON
        # Find the JSON part of the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx >= 0 and end_idx > start_idx:
            json_text = response_text[start_idx:end_idx]
            result = json.loads(json_text)
            return result
        else:
            # Try to find JSON objects if not in expected format
            import re
            json_pattern = r'\{.*?\}'
            matches = re.findall(json_pattern, response_text, re.DOTALL)
            if matches:
                combined = "[" + ",".join(matches) + "]"
                try:
                    result = json.loads(combined)
                    return result
                except:
                    pass

            print("Failed to parse JSON from response")
            print("Response:", response_text)
            return None

    except Exception as e:
        print(f"Error generating messages: {str(e)}")
        return None

# Function to test the hospitality chatbot with the generated messages
def test_chatbot_with_messages(messages_data, model="gpt-4o-mini"):
    """
    Test the hospitality chatbot with the generated vague messages.

    Args:
        messages_data (list): List of dictionaries containing messages and correct mappings
        model (str): The model to test (default: gpt-4o-mini)

    Returns:
        dict: Test results
    """
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
      - Finally, respond appropriately to the user's request based on the identified intention

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"hospitality_chatbot_test_results_{timestamp}.txt"

    print(f"Testing hospitality chatbot with {len(messages_data)} vague messages...")
    print(f"Results will be saved to {results_file}")

    # Dictionary to store results
    results = {
        "total_messages": len(messages_data),
        "correct_mappings": 0,
        "incorrect_mappings": 0,
        "detailed_results": []
    }

    # Process each message
    for i, message_data in enumerate(messages_data):
        message = message_data["message"]
        correct_mapping = message_data["correct_mapping"]

        print(f"\nProcessing message {i+1}/{len(messages_data)}")

        # Extract the correct intention number
        correct_number = correct_mapping.split(' ')[0]

        try:
            # Send the message to the chatbot
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # Extract the response text
            chatbot_response = response.choices[0].message.content

            # Extract the intention from the response
            extracted_intention = extract_intention(chatbot_response)

            # Determine if the mapping is correct
            is_correct = extracted_intention == correct_number if extracted_intention else False

            # Add delay to avoid rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Error testing message: {str(e)}")
            chatbot_response = f"Error: {str(e)}"
            extracted_intention = None
            is_correct = False

        # Store the result
        result_entry = {
            "message": message,
            "correct_mapping": correct_mapping,
            "explanation": message_data.get("explanation", ""),
            "chatbot_response": chatbot_response,
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
        print(f"Correct mapping: {correct_mapping}")
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
            f.write(f"Explanation: {result['explanation']}\n")
            f.write(f"Extracted intention: {result['extracted_intention']}\n")
            f.write(f"Is correct: {result['is_correct']}\n")
            f.write(f"Chatbot response:\n{result['chatbot_response']}\n\n")

    # Also save raw messages and correct mappings to reuse
    messages_only = [item["message"] for item in messages_data]
    mappings_only = [item["correct_mapping"] for item in messages_data]

    with open(f"vague_messages_{timestamp}.py", 'w') as f:
        f.write("# Generated vague messages and their correct mappings\n\n")
        f.write("vague_messages = [\n")
        for msg in messages_only:
            f.write(f"    \"{msg}\",\n")
        f.write("]\n\n")

        f.write("correct_mappings = [\n")
        for mapping in mappings_only:
            f.write(f"    \"{mapping}\",\n")
        f.write("]\n")

    print(f"\nTesting completed!")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Complete results saved to {results_file}")
    print(f"Messages and mappings saved to vague_messages_{timestamp}.py")

    return results

def extract_intention(response):
    """
    Extract the intention number from the chatbot's response.

    Args:
        response (str): The chatbot's response

    Returns:
        str: The extracted intention number or None if not found
    """
    # Look for patterns like "INTENTION: #16 - Request room cleaning" or variations
    import re

    # Try different patterns
    patterns = [
        r"INTENTION:\s*#?(\d+)",
        r"intention:\s*#?(\d+)",
        r"#(\d+)\s*-",
        r"intention\s*(?:is|:)?\s*(?:number)?\s*#?(\d+)",
        r"intention\s*(?:is|:)?\s*(?:to)?\s*#?(\d+)",
        r"(\d+)\s*-\s*[A-Za-z]"
    ]

    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            return match.group(1)

    # If we can't find it with regex, try line by line
    lines = response.split('\n')
    for line in lines:
        if "INTENTION:" in line or "intention:" in line or "#" in line:
            parts = line.split('#')
            if len(parts) > 1:
                # Extract the number after #
                intention_part = parts[1].strip()
                # If there's a space or dash, get just the number
                if ' ' in intention_part:
                    intention_number = intention_part.split(' ')[0]
                elif '-' in intention_part:
                    intention_number = intention_part.split('-')[0]
                else:
                    intention_number = intention_part
                return intention_number.strip()

    return None

def main():
    # Generate vague messages
    print("Generating vague messages using GPT-4.1...")
    generated_data = generate_vague_messages(20)

    if not generated_data:
        print("Failed to generate messages. Exiting.")
        return

    print(f"Successfully generated {len(generated_data)} messages.")

    # Save the generated data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"generated_messages_{timestamp}.json", 'w') as f:
        json.dump(generated_data, f, indent=2)

    print(f"Generated messages saved to generated_messages_{timestamp}.json")

    # Extract messages and mappings for Python lists
    vague_messages = [item["message"] for item in generated_data]
    correct_mappings = [item["correct_mapping"] for item in generated_data]

    # Print the Python lists
    print("\n# Python lists of vague messages and correct mappings:")
    print("vague_messages = [")
    for msg in vague_messages:
        print(f"    \"{msg}\",")
    print("]")
    print()
    print("correct_mappings = [")
    for mapping in correct_mappings:
        print(f"    \"{mapping}\",")
    print("]")

    # Print the messages and mappings
    print("\nGenerated Messages and Mappings:")
    for i, (message, mapping) in enumerate(zip(vague_messages, correct_mappings)):
        print(f"\n{i+1}. {message}")
        print(f"   Correct mapping: {mapping}")

    # Ask if testing should proceed
    test_now = input("\nDo you want to test these messages with GPT-4o-mini now? (y/n): ")

    if test_now.lower() == 'y':
        # Test the chatbot with the generated messages
        test_results = test_chatbot_with_messages(generated_data)
        print("\nMessages that GPT-4o-mini got wrong:")
        for result in test_results["detailed_results"]:
            if not result["is_correct"]:
                print(f"\nMessage: {result['message']}")
                print(f"Correct mapping: {result['correct_mapping']}")
                print(f"GPT-4o-mini mapped to: {result['extracted_intention']}")
    else:
        print("Testing skipped. You can run the test later using the saved messages.")

if __name__ == "__main__":
    main()