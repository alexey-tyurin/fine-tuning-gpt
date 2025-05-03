import os
import json
import time
import argparse
from openai import OpenAI

# Initialize the OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

# System prompt from test_intent_4o-mini_200.py
SYSTEM_PROMPT = """You are an advanced hospitality chatbot for a premium hotel chain. Your primary function is to analyze user messages and accurately identify their main intention from a predefined list of 40 possible intentions. Follow these guidelines:

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

# File to store IDs for each step
IDS_FILE = "openai_eval_ids.json"

def load_ids():
    """Load previously saved IDs from file"""
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"eval_id": None, "data_id": None, "run_id": None}
    return {"eval_id": None, "data_id": None, "run_id": None}

def save_ids(ids_dict):
    """Save IDs to file for later use"""
    with open(IDS_FILE, 'w') as f:
        json.dump(ids_dict, f, indent=2)

def create_eval():
    """
    Create an evaluation task for the hospitality intent classification
    Reference: https://platform.openai.com/docs/api-reference/evals/create
    """
    print("Creating eval task...")
    
    # Define the eval task according to the OpenAI API reference
    eval_task = {
        "name": "Hospitality Intent Classification",
        "metadata": {
            "usecase": "chatbot"
        },
        "data_source_config": {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "input_text": {"type": "string"},
                    "correct_label": {"type": "string"}
                },
                "required": ["input_text", "correct_label"]
            },
            "include_sample_schema": True
        },
        "testing_criteria": [
            {
                "type": "string_check",
                "name": "Match output to human label",
                "input": "{{ sample.output_text }}",
                "operation": "eq",
                "reference": "{{ item.correct_label }}"
            }
        ]
    }
    
    try:
        response = client.evals.create(**eval_task)
        eval_id = response.id
        
        # Print all returned fields
        print("\nEval created successfully:")
        print(f"ID: {eval_id}")
        print(f"Name: {response.name}")
        print(f"Created at: {response.created_at}")
        
        # Save the ID for later use
        ids = load_ids()
        ids["eval_id"] = eval_id
        save_ids(ids)
        
        return eval_id
    except Exception as e:
        print(f"Error creating eval task: {str(e)}")
        return None

def upload_test_data():
    """
    Upload the test data from evals.jsonl to the eval task
    """
    
    print(f"Uploading test data ...")
    
    try:
        # Upload the data to the eval
        response = client.files.create(
            file=open("evals10.jsonl", "rb"),
            purpose="evals"
        )

        data_id = response.id
        
        # Print all returned fields
        print("\nData uploaded successfully:")
        print(f"Data ID: {data_id}")
        print(f"Status: {response.status}")
        print(f"Created at: {response.created_at}")
        
        # Save the ID for later use
        ids = {}
        ids["data_id"] = data_id
        save_ids(ids)
        
        return data_id
    except Exception as e:
        print(f"Error uploading test data: {str(e)}")
        return None

def create_eval_run(eval_id=None, data_id=None):
    """
    Create an evaluation run using the gpt-4o-mini model
    Reference: https://platform.openai.com/docs/api-reference/evals/createRun
    """
    if eval_id is None or data_id is None:
        ids = load_ids()
        eval_id = ids.get("eval_id") if eval_id is None else eval_id
        data_id = ids.get("data_id") if data_id is None else data_id
        
        if not eval_id or not data_id:
            print("Missing eval_id or data_id. Please create an eval and upload data first.")
            return None
    
    print(f"Creating eval run for eval ID: {eval_id} and data ID: {data_id}...")
    
    # Define the eval run configuration according to the OpenAI API reference
    eval_run_config = {
        "eval_id": eval_id,
        "name": "gpt-4o-mini 10",
        "data_source": {
            "type": "completions",
            "model": "gpt-4o-mini",
            "input_messages": {
                "type": "template",
                "template": [
                    {
                        "role": "developer",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": "{{item.input_text}}"
                    }
                ]
            },
            "sampling_params": {
                "seed": 42
            },
            "source": {
                "type": "file_id",
                "id": data_id
            }
        }
    }
    
    try:
        response = client.evals.runs.create(**eval_run_config)
        run_id = response.id
        
        # Print all returned fields
        print("\nEval run created successfully:")
        print(f"Run ID: {run_id}")
        print(f"Eval ID: {response.eval_id}")
        print(f"Data ID: {response.data_id}")
        print(f"Model: {response.model}")
        print(f"Status: {response.status}")
        print(f"Created at: {response.created_at}")
        
        # Save the ID for later use
        ids = load_ids()
        ids["run_id"] = run_id
        save_ids(ids)
        
        return run_id
    except Exception as e:
        print(f"Error creating eval run: {str(e)}")
        return None

def check_run_status(run_id=None):
    """
    Check the status of the evaluation run
    """
    if run_id is None:
        ids = load_ids()
        run_id = ids.get("run_id")
        if not run_id:
            print("No run ID provided or found in saved IDs. Please create a run first.")
            return None
    
    print(f"Checking status for run ID: {run_id}...")
    
    try:
        while True:
            response = client.evaluations.get_run(run_id=run_id)
            status = response.status
            print(f"Run status: {status}")
            
            if status in ["completed", "failed", "cancelled"]:
                # Print details when status changes to completed or failed
                print("\nRun details:")
                print(f"Run ID: {response.id}")
                print(f"Status: {response.status}")
                print(f"Started at: {response.started_at}")
                print(f"Completed at: {response.completed_at}")
                if hasattr(response, 'error'):
                    print(f"Error: {response.error}")
                return status
            
            # Wait for 10 seconds before checking again
            time.sleep(10)
    except Exception as e:
        print(f"Error checking run status: {str(e)}")
        return None

def extract_intention_number(response):
    """
    Extract the intention number from the model's response
    """
    # Look for patterns like "INTENTION: #16 - Request room cleaning" or variations
    lines = response.split('\n')
    for line in lines:
        if "INTENTION:" in line or "intention:" in line:
            parts = line.split('#')
            if len(parts) > 1:
                # Extract the number after the #
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

def analyze_results(run_id=None):
    """
    Analyze the results of the evaluation run
    """
    if run_id is None:
        ids = load_ids()
        run_id = ids.get("run_id")
        if not run_id:
            print("No run ID provided or found in saved IDs. Please create a run first.")
            return None
    
    print(f"Analyzing results for run ID: {run_id}...")
    
    try:
        # Get the results of the run
        response = client.evaluations.list_records(run_id=run_id)
        records = response.data
        
        total_records = len(records)
        correct = 0
        incorrect = 0
        processed_records = []
        
        # Process each record
        for record in records:
            expected = record.expected_output
            actual_response = record.output
            
            # Extract the intention number from the response
            extracted_intention = extract_intention_number(actual_response)
            
            # Check if the intention is correct
            is_correct = extracted_intention == expected
            
            if is_correct:
                correct += 1
            else:
                incorrect += 1
            
            # Store the record details
            processed_record = {
                "id": record.id,
                "input_text": record.input_messages[1].content if len(record.input_messages) > 1 else "",
                "expected_intention": expected,
                "model_response": actual_response,
                "extracted_intention": extracted_intention,
                "is_correct": is_correct
            }
            
            processed_records.append(processed_record)
        
        # Calculate accuracy
        accuracy = correct / total_records if total_records > 0 else 0
        
        # Create a results summary
        results = {
            "run_id": run_id,
            "total_records": total_records,
            "correct": correct,
            "incorrect": incorrect,
            "accuracy": accuracy,
            "records": processed_records
        }
        
        # Save the results to a file
        results_file = f"eval_results_{run_id}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nAnalysis completed!")
        print(f"Total records: {total_records}")
        print(f"Correct: {correct}")
        print(f"Incorrect: {incorrect}")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Detailed results saved to {results_file}")
        
        return results
    
    except Exception as e:
        print(f"Error analyzing results: {str(e)}")
        return None

def run_all():
    """
    Run all steps in sequence
    """
    print("Starting complete OpenAI Evaluation Process...")

    # Step 1: Upload the test data
    data_id = upload_test_data()
    if not data_id:
        return

    # Step 2: Create the eval task
    eval_id = create_eval()
    if not eval_id:
        return
    
    # Step 3: Create and start the eval run
    run_id = create_eval_run(eval_id, data_id)
    if not run_id:
        return
    
    # Step 4: Check the status of the run
    status = check_run_status(run_id)
    if status != "completed":
        print(f"Run did not complete successfully. Status: {status}")
        return
    
    # Step 5: Analyze the results
    analyze_results(run_id)

def main():
    """
    Main function to parse arguments and run the appropriate step
    """
    parser = argparse.ArgumentParser(description='OpenAI Evaluation Process')
    
    # Add arguments for each step
    parser.add_argument('--upload', action='store_true', help='Upload test data')
    parser.add_argument('--create', action='store_true', help='Create an eval task')
    parser.add_argument('--run', action='store_true', help='Create and start an eval run')
    parser.add_argument('--check', action='store_true', help='Check the status of a run')
    parser.add_argument('--analyze', action='store_true', help='Analyze the results of a run')
    parser.add_argument('--all', action='store_true', help='Run all steps in sequence')
    
    # Add arguments for IDs
    parser.add_argument('--eval-id', type=str, help='Eval ID for operations that require it')
    parser.add_argument('--data-id', type=str, help='Data ID for operations that require it')
    parser.add_argument('--run-id', type=str, help='Run ID for operations that require it')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any([args.create, args.upload, args.run, args.check, args.analyze, args.all]):
        parser.print_help()
        return
    
    # Run the appropriate step based on the arguments
    if args.all:
        run_all()
    else:
        if args.upload:
            upload_test_data()

        if args.create:
            create_eval()
        
        if args.run:
            create_eval_run(args.eval_id, args.data_id)
        
        if args.check:
            check_run_status(args.run_id)
        
        if args.analyze:
            analyze_results(args.run_id)

if __name__ == "__main__":
    main() 