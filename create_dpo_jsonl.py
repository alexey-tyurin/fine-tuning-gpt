#!/usr/bin/env python3

import json
import random
import os

# Import vague_messages and correct_mappings from messages_mappings200_2.py
try:
    from messages_mappings200_2 import vague_messages, correct_mappings, intention_names
except ImportError:
    print("Error: Could not import from messages_mappings200_2.py")
    exit(1)

# Get SYSTEM_PROMPT from openai_eval.py
SYSTEM_PROMPT = """You are an advanced hospitality chatbot for a premium hotel chain. Your primary function is to analyze user messages and accurately identify their main intention from a predefined list of 40 possible intentions. Follow these guidelines:

1. CORE FUNCTION: For each user message, identify exactly ONE primary intention from the list of 40 intentions provided below.

2. ANALYSIS APPROACH:
   - Carefully analyze the entire message for explicit and implicit requests
   - Look for action verbs and specific service mentions
   - Consider context clues and hospitality-specific terminology
   - Identify the most urgent or primary need if multiple are present
   - Focus on what the user wants to accomplish, not just what they're asking about
   - Identify the intention number and name (e.g., "INTENTION: #16 - Request room cleaning")

3. RESPONSE FORMAT:
   - Respond with only intention number (e.g., 16)

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

def get_non_preferred_label(preferred_label):
    """
    Get a non-preferred label that is close in meaning to the preferred label
    """
    # Group intention numbers by semantic similarity
    similar_intentions = {
        # Reservation related
        1: [2, 3, 5],  # Check availability - Make reservation, Modify, Status
        2: [1, 3, 5],  # Make reservation - Check availability, Modify, Status  
        3: [1, 2, 4, 5],  # Modify - Availability, Make, Cancel, Status
        4: [3, 5],  # Cancel - Modify, Status
        5: [1, 2, 3, 4],  # Status - Availability, Make, Modify, Cancel
        
        # Check-in/out related
        6: [7, 8],  # Early check-in - Late check-out, Check-in online
        7: [6, 9],  # Late check-out - Early check-in, Check-out online
        8: [6, 9],  # Check-in online - Early check-in, Check-out online
        9: [7, 8],  # Check-out online - Late check-out, Check-in online
        
        # Room service/amenities
        10: [20],  # Luggage assistance - In-room amenities
        11: [12, 13, 14, 15],  # Room service - Restaurant, Menu, Breakfast, Minibar
        12: [11, 13, 14],  # Restaurant table - Room service, Menu, Breakfast
        13: [11, 12, 14],  # Menu info - Room service, Restaurant, Breakfast
        14: [11, 12, 13],  # Breakfast - Room service, Restaurant, Menu
        15: [11],  # Minibar - Room service
        
        # Room maintenance
        16: [17, 18],  # Room cleaning - Extra towels, Report issue
        17: [16, 18, 20],  # Extra towels - Cleaning, Report issue, In-room amenities
        18: [16, 17],  # Report issue - Cleaning, Extra towels
        19: [16, 17],  # Laundry - Cleaning, Extra towels
        20: [10, 17],  # In-room amenities - Luggage assistance, Extra towels
        
        # Information and services
        21: [23, 32],  # Local attractions - Taxi service, Facility hours
        22: [14],  # Wake-up call - Breakfast hours
        23: [21, 33],  # Taxi service - Local attractions, Parking
        24: [34, 35],  # Hotel policies - Pet policy, Smoking policy
        25: [21],  # Spa appointment - Local attractions
        
        # Billing related
        26: [27, 28, 29, 30],  # Invoice - Charges, Payment method, Split bill, Pre-auth
        27: [26, 28, 29, 30],  # Charges - Invoice, Payment method, Split bill, Pre-auth
        28: [26, 27, 29, 30],  # Payment method - Invoice, Charges, Split bill, Pre-auth
        29: [26, 27, 28, 30],  # Split bill - Invoice, Charges, Payment method, Pre-auth
        30: [26, 27, 28, 29],  # Pre-auth - Invoice, Charges, Payment method, Split bill
        
        # Facilities and policies
        31: [20, 24],  # Wi-Fi - In-room amenities, Hotel policies
        32: [21, 25],  # Facility hours - Local attractions, Spa appointment
        33: [23],  # Parking - Taxi service
        34: [24, 35],  # Pet policy - Hotel policies, Smoking policy
        35: [24, 34],  # Smoking policy - Hotel policies, Pet policy
        
        # Feedback and support
        36: [37],  # Review - Complaint
        37: [36, 38],  # Complaint - Review, Manager
        38: [37, 39],  # Manager - Complaint, Human support
        39: [38, 40],  # Human support - Manager, Help with chatbot
        40: [39]   # Help with chatbot - Human support
    }
    
    # Get similar intentions for the preferred label
    similar = similar_intentions.get(preferred_label, [])
    
    # If no similar intentions are found, pick a random one with 5 distance
    if not similar:
        # Get a random label that is at least 2 numbers away from preferred
        possible_labels = [i for i in range(1, 41) if abs(i - preferred_label) >= 2]
        return random.choice(possible_labels)
    
    # Return a random similar intention
    return random.choice(similar)

def create_dpo_jsonl():
    """
    Create JSONL file for DPO training
    """
    output_file = "dpo_tests.jsonl"
    
    with open(output_file, "w") as f:
        for i, (message, label) in enumerate(zip(vague_messages, correct_mappings)):
            # Get preferred and non-preferred labels
            preferred_label = str(label)
            non_preferred_label = str(get_non_preferred_label(label))
            
            # Create DPO sample
            sample = {
                "input": {
                    "messages": [
                        {"role": "developer", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": message}
                    ]
                },
                "preferred_output": [
                    {"role": "assistant", "content": preferred_label}
                ],
                "non_preferred_output": [
                    {"role": "assistant", "content": non_preferred_label}
                ]
            }
            
            # Write as single line JSON
            f.write(json.dumps(sample) + "\n")
    
    print(f"Created DPO JSONL file: {output_file} with {len(vague_messages)} samples")
    
    # Print a few examples
    with open(output_file, "r") as f:
        examples = [json.loads(f.readline()) for _ in range(min(3, len(vague_messages)))]
    
    print("\nExample entries:")
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"User message: {example['input']['messages'][1]['content']}")
        print(f"Preferred label: {example['preferred_output'][0]['content']}")
        print(f"Non-preferred label: {example['non_preferred_output'][0]['content']}")

if __name__ == "__main__":
    create_dpo_jsonl() 