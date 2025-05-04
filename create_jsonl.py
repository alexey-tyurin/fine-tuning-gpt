import json

# System prompt from openai_eval.py
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

# Data from messages_mappings10.py
vague_messages = [
    "I need some assistance with my morning plans tomorrow. The timing might be tricky and I'm not sure how everything will work out with what I've scheduled.",
    "I have a situation that might need special attention. My elderly parent will be joining us and might need extra assistance during our visit.",
    "There's something different about our arrangements compared to what we booked. I noticed some inconsistencies when reviewing the confirmation.",
    "I'm wondering about the options we have for managing our things on the last day. We have activities planned before we leave.",
    "I noticed the information seems different from other places we've stayed. Could you explain how certain things work here?",
    "We had some challenges during our last stay that I wanted to discuss. I think it would be helpful if we could talk about it properly.",
    "I've been trying to find information about specific arrangements for our upcoming event. The details seem to be missing from the confirmation.",
    "I need to understand the requirements for our departure. There are some timing considerations that might affect our plans.",
    "I'm concerned about our schedule flexibility when we arrive. Our group has different preferences that might need accommodation.",
    "I notice the final documentation doesn't match my expectations. There are discrepancies that I'd like to address."
]

correct_mappings = [
    14, # Ask for breakfast hours or availability
    10, # Request luggage assistance
    3,  # Modify reservation
    7,  # Request late check-out
    40, # Ask for help using the chatbot
    39, # Request human support or live agent
    12, # Book a table at a restaurant
    7,  # Request late check-out
    6,  # Request early check-in
    27  # Query charges on the bill
]

# Create the JSONL data
with open('tests10.jsonl', 'w') as f:
    for i in range(len(vague_messages)):
        example = {
            "messages": [
                {"role": "developer", "content": SYSTEM_PROMPT},
                {"role": "user", "content": vague_messages[i]},
                {"role": "assistant", "content": str(correct_mappings[i])}
            ]
        }
        f.write(json.dumps(example) + '\n')

print("Created tests10.jsonl with 10 examples in the correct format.") 