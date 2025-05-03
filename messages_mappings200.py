
# Python lists of vague messages and their correct mappings

vague_messages = [
    "We'd like to know if there's a way to make our anniversary extra special without a lot of fuss.",
    "I'm curious about how we can manage our final day given our unusual departure situation.",
    "Our plans changed unexpectedly and I'm trying to figure out if we need to adjust anything with you.",
    "I'm looking at ways to make our arrival smoother considering we're traveling with quite a bit of luggage.",
    "I'm planning for our upcoming visit and would like to know more about the first part of our stay.",
    "We're trying to coordinate a special dining experience during our stay. What might be possible?",
    "Wondering if there's anything we should know about transport links from the property to the city center.",
    "I need some information about the connectivity at your property for planning my work schedule during our stay.",
    "We're arriving with our small dog and wanted to check if there's anything special we need to arrange.",
    "We'd like to explore some relaxation options during our stay. What would you recommend?",
    "I'm curious about any fees that might appear on our final bill that haven't been mentioned yet.",
    "Could you help me understand the situation with our room? Something doesn't seem right based on what I'm seeing online.",
    "I need to finalize some arrangements for when we leave the property. What are our options?",
    "Our family has some specific needs that I want to make sure are addressed during our stay.",
    "What are the options for keeping our valuables safe during our stay?",
    "I'm not sure if our current arrangement will work with our schedule. Can we discuss alternatives?",
    "We'd like to ensure a peaceful stay. Are there quiet areas or times we should be aware of?",
    "Could you clarify what's included in our package? I'm trying to budget for extras.",
    "I'd like to know more about the area around the property for planning daily activities.",
    "We might need to adjust the number of people in our party. How should we handle this?",
    "I'm planning my work schedule during our stay and need to understand the facilities better.",
    "What's the protocol if we end up running late on the day we're supposed to arrive?",
    "I need to understand our options for our morning departure as we have an early flight.",
    "I'd like to know if there's a way to arrange some privacy during our stay for a small business meeting.",
    "Could you explain the process of settling our account? We have some specific requirements.",
    "I'm trying to coordinate with other members of our group about our accommodation details.",
    "What's the procedure if we need some assistance with personal items during our stay?",
    "I'd like to know more about your environmental practices as this influences our booking decisions.",
    "Could you give me some information about accessibility at your property? We have someone with mobility issues.",
    "I'm trying to plan out our daily routine during our stay and need to know about the timing of certain services.",
    "We might need to make a change to our plans. What's the best way to handle this with you?",
    "I'd like to ensure our room meets some specific criteria for our comfort.",
    "What options do we have for our last day regarding our belongings?",
    "I'm trying to work out the logistics of our first day at your property.",
    "Could you tell me more about how you accommodate guests with various dietary preferences?",
    "I'm trying to determine if your property can provide what we need for a small gathering.",
    "What's involved in the process of verifying our stay details before arrival?",
    "I'm concerned about the timing of our departure and how that aligns with your procedures.",
    "We've had a change in our travel arrangements and I'm wondering how that affects our booking.",
    "Could you help me understand what entertainment options are available nearby?",
    "I'm not familiar with how things work at your property and want to make sure we're prepared.",
    "We might need to arrange a special setup in our room. Is that something you can help with?",
    "I'm curious about what might be possible for a surprise for my partner during our stay.",
    "What's the procedure if we need to communicate some specific requirements for our stay?",
    "I'm trying to budget for our stay and need to understand all potential costs.",
    "Could you give me some information about the scheduling of housekeeping services?",
    "We're planning a late evening activity and need to know how this works with your property.",
    "I need to know more about how you handle guests with multiple rooms and different arrangements.",
    "What's your process for handling any issues that might arise during our stay?",
    "I'd like to understand more about the neighborhood and what we can expect during our visit.",
    "We may need to reconsiider some aspects of our booking. What are the implications?",
    "Could you provide some information about any special services for business travelers?",
    "I'm trying to decide if we need to make any advance arrangements for our visit.",
    "What options do we have if our plans change suddenly during our stay?",
    "I need some information about vehicle accommodations at your property.",
    "Could you explain how you handle the coordination of room assignments for group bookings?",
    "I'm trying to figure out the timing of our movement between the airport and your property.",
    "What's the best approach to ensure we get the type of accommodation we're hoping for?",
    "I need to understand your approach to managing unexpected changes to guest needs.",
    "Could you share some information about the morning arrangements at your property?",
    "I'm curious about how flexible your property is with adjustments to existing bookings.",
    "What's your approach to ensuring guests have everything they need during their stay?",
    "I need some guidance on planning our daily schedule while staying at your property.",
    "Could you explain how you accommodate unexpected needs that arise during a stay?",
    "I'm trying to plan our meals during our stay and need to understand the options.",
    "What's the protocol for addressing any concerns about our accommodation?",
    "I need to understand the options for our group to enjoy some downtime together.",
    "Could you give me some information about how we confirm our arrangements prior to arrival?",
    "I'm planning how to handle our last few hours at your property and need some advice.",
    "What's your policy on adjustments to arrangements based on unexpected circumstances?",
    "I need to coordinate some aspects of our stay with your team. How do I do that?",
    "Could you share some information about how your property handles special occasions?",
    "I'm trying to decide if we need to bring certain items or if they're provided by you.",
    "What's the process for ensuring our specific preferences are noted for our stay?",
    "I need to understand if there are any restrictions we should be aware of before arrival.",
    "Could you explain how your property manages the various needs of different guests?",
    "I'm curious about the provisions for our comfort in the evenings during our stay.",
    "What's your approach to handling feedback from guests about their experience?",
    "I need to know more about navigating your property and the surrounding area.",
    "Could you provide some clarity on the kind of atmosphere we can expect?",
    "I'm trying to determine if your property is the right fit for our particular situation.",
    "What's the best way to ensure our experience meets our expectations?",
    "I need to understand how flexible your arrangements can be for our particular needs.",
    "Could you explain how your property addresses any unexpected issues that arise?",
    "I'm wondering about the accommodations for different members of our party with varying preferences.",
    "What's your process for managing guest expectations throughout their stay?",
    "I need to know more about how you ensure guest satisfaction with their accommodations.",
    "Could you share some information about the morning services available to guests?",
    "I'm trying to plan the most efficient use of our time during our stay.",
    "What's the best way to communicate any specific needs we might have during our visit?",
    "I need to understand the options for adjusting our arrangements if necessary.",
    "Could you explain how you handle situations where guests need something unexpected?",
    "I'm curious about what provisions are made for guests with various requirements.",
    "What's your approach to ensuring guests have a comfortable arrival experience?",
    "I need to know more about the ways we can enhance our experience at your property.",
    "Could you share some information about how guests typically manage their belongings?",
    "I'm trying to determine the best approach for our family to enjoy your facilities.",
    "What's your policy on accommodating guests who need to make adjustments to their stay?",
    "I need to understand how your property handles various payment arrangements.",
    "Could you explain the options for ensuring our specific room preferences are met?",
    "I'm wondering about the processes in place for addressing any concerns during our stay.",
    "What's the best way to ensure we have all the information we need before arrival?",
    "I need some guidance on planning the logistics of our departure from your property.",
    "Could you provide some insight into how your property manages guest expectations?",
    "I'm trying to decide the best timing for various aspects of our stay.",
    "What's your approach to handling situations where guests have specific timing needs?",
    "I need to know more about the provisions for our comfort in the room.",
    "Could you explain how your property ensures guests have a pleasant departure experience?",
    "I'm curious about the ways in which your property accommodates various guest preferences.",
    "What's the protocol for handling any special requirements we might have?",
    "I need to understand how your property manages guest valuables during their stay.",
    "Could you share some information about the final steps of the guest experience?",
    "I'm trying to determine if there are any aspects of our stay we need to plan for in advance.",
    "What's your policy on accommodating guests who need to adjust their departure plans?",
    "I need to know more about how you handle situations where guests have forgotten items.",
    "Could you explain the experience we can expect upon first arriving at your property?",
    "I'm wondering about the arrangements for ensuring guests have a smooth morning experience.",
    "What's the best approach for managing our personal items during our stay?",
    "I need to understand your property's approach to handling guest feedback.",
    "Could you explain how you accommodate guests who require specific sleeping arrangements?",
    "I'm trying to determine the best way to handle our morning routine during our stay.",
    "What's your policy on accommodating guests who need to work during their stay?",
    "I need to know more about how your property ensures guest security.",
    "Could you share some information about the staff availability throughout the day?",
    "I'm wondering about the customs and expectations at your property.",
    "What's the best approach for ensuring we have all necessary documentation for our stay?",
    "I need to understand how your property handles any disruptions to scheduled services.",
    "Could you explain the options for guests who need flexibility with their arrangements?",
    "I'm trying to figure out if your property can accommodate our particular situation.",
    "What's your approach to handling situations where guests need additional items?",
    "I need to know more about the resources available for guests during their stay.",
    "Could you share some information about the daily routines at your property?",
    "I'm curious about the arrangements for ensuring guest comfort throughout their stay.",
    "What's the protocol for addressing any questions we might have during our visit?",
    "I need to understand the options for managing our expenses during our stay.",
    "Could you explain how your property ensures guests have the amenities they need?",
    "I'm trying to determine if there are any special considerations for our type of stay.",
    "What's your policy on accommodating guests with varying schedule needs?",
    "I need to know more about how your property manages guest communications.",
    "Could you share some information about the systems in place for guest convenience?",
    "I'm wondering about the arrangements for guests who need specific room conditions.",
    "What's the best way to ensure we're prepared for our arrival at your property?",
    "I need to understand how your property accommodates guests with different needs.",
    "Could you explain the process for addressing any concerns with our accommodations?",
    "I'm trying to figure out the best timing for various aspects of our visit.",
    "What's your approach to ensuring guests have a positive arrival experience?",
    "I need to know more about the options for our daily routine during our stay.",
    "Could you share some information about the procedures for handling guest requests?",
    "I'm curious about what makes your property unique for guests like us.",
    "What's the protocol for ensuring our expectations are met during our stay?",
    "I need to understand how your property handles situations requiring flexibility.",
    "Could you explain the arrangements for guests who have specific daily requirements?",
    "I'm trying to determine if there are any aspects of our stay we should plan ahead for.",
    "What's your policy on accommodating guests with special celebration plans?",
    "I need to know more about how your property ensures guest satisfaction.",
    "Could you share some information about the experience we can expect on departure?",
    "I'm wondering about the arrangements for ensuring guests have everything they need.",
    "What's the best approach for managing our personal items when we're not in the room?",
    "I need to understand how your property handles situations requiring immediate attention.",
    "Could you explain the options for ensuring our specific preferences are accommodated?",
    "I'm trying to figure out if there are any special considerations for our visit.",
    "What's your approach to handling situations where guests need specific assistance?",
    "I need to know more about the provisions for our comfort in the bathroom.",
    "Could you share some information about the manner in which guest needs are addressed?",
    "I'm curious about the ways in which your property enhances the guest experience.",
    "What's the protocol for managing our expectations throughout our stay?",
    "I need to understand how your property handles guests with varying needs.",
    "Could you explain the process for ensuring our comfort during our visit?",
    "I'm trying to determine the best approach for our unique situation.",
    "What's your policy on accommodating guests with specific timing requirements?",
    "I need to know more about how your property ensures a smooth guest experience.",
    "Could you share some information about the systems in place for guest requests?",
    "I'm wondering about the arrangements for guests who prefer a contactless experience.",
    "What's the best way to ensure we have the optimal room setup for our needs?",
    "I need to understand how your property manages requests for additional services.",
    "Could you explain the options for guests who need assistance with their planning?",
    "I'm trying to figure out the most appropriate approach for our family's needs.",
    "What's your policy on managing situations where guest expectations aren't met?",
    "I need to know more about the ways in which guests typically handle their departure.",
    "Could you share some information about the approach to ensuring guest security?",
    "I'm curious about the arrangements for ensuring guests have a pleasant environment.",
    "What's the protocol for addressing any specific requirements we might have?",
    "I need to understand how your property handles guest-initiated changes to arrangements.",
    "Could you explain the process for ensuring our specific room is suitable for us?",
    "I'm trying to determine if there are any special provisions we should be aware of.",
    "What's your approach to handling situations requiring adjustment to standard procedures?",
    "I need to know more about how your property ensures guest privacy and security.",
    "Could you share some information about the daily operations that might affect guests?",
    "I'm wondering about the preparations we should make before our departure.",
    "What's the best way to address any issues that might arise unexpectedly during our stay?",
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
    20, # Request in-room amenities
    7,  # Request late check-out
    3,  # Modify reservation
    10, # Request luggage assistance
    6,  # Request early check-in
    12, # Book a table at a restaurant
    23, # Ask for taxi or shuttle service
    31, # Ask for Wi-Fi access or help
    34, # Ask about pet policy
    25, # Request spa or gym appointment
    27, # Query charges on the bill
    5,  # Check reservation status
    23, # Ask for taxi or shuttle service
    20, # Request in-room amenities
    24, # Ask about hotel policies
    3,  # Modify reservation
    24, # Ask about hotel policies
    27, # Query charges on the bill
    21, # Ask about local attractions or tours
    3,  # Modify reservation
    32, # Ask about facility opening hours
    8,  # Check-in online
    9,  # Check-out online
    12, # Book a table at a restaurant
    28, # Change payment method
    29, # Split bill
    19, # Request laundry service
    24, # Ask about hotel policies
    24, # Ask about hotel policies
    32, # Ask about facility opening hours
    3,  # Modify reservation
    17, # Request extra towels, toiletries, or pillows
    10, # Request luggage assistance
    6,  # Request early check-in
    13, # Request menu or dietary information
    12, # Book a table at a restaurant
    5,  # Check reservation status
    7,  # Request late check-out
    3,  # Modify reservation
    21, # Ask about local attractions or tours
    24, # Ask about hotel policies
    20, # Request in-room amenities
    20, # Request in-room amenities
    39, # Request human support or live agent
    27, # Query charges on the bill
    16, # Request room cleaning
    32, # Ask about facility opening hours
    29, # Split bill
    18, # Report an issue in the room
    21, # Ask about local attractions or tours
    4,  # Cancel reservation
    31, # Ask for Wi-Fi access or help
    8,  # Check-in online
    3,  # Modify reservation
    33, # Request parking information
    2,  # Make a reservation / Book a room
    23, # Ask for taxi or shuttle service
    1,  # Check room availability
    38, # Ask to speak to a manager
    14, # Ask for breakfast hours or availability
    3,  # Modify reservation
    17, # Request extra towels, toiletries, or pillows
    32, # Ask about facility opening hours
    39, # Request human support or live agent
    13, # Request menu or dietary information
    37, # Report a complaint
    21, # Ask about local attractions or tours
    5,  # Check reservation status
    7,  # Request late check-out
    4,  # Cancel reservation
    39, # Request human support or live agent
    20, # Request in-room amenities
    20, # Request in-room amenities
    8,  # Check-in online
    35, # Ask about smoking policy
    24, # Ask about hotel policies
    15, # Request minibar refill
    36, # Leave a review or feedback
    21, # Ask about local attractions or tours
    24, # Ask about hotel policies
    1,  # Check room availability
    38, # Ask to speak to a manager
    3,  # Modify reservation
    18, # Report an issue in the room
    2,  # Make a reservation / Book a room
    40, # Ask for help using the chatbot
    18, # Report an issue in the room
    14, # Ask for breakfast hours or availability
    32, # Ask about facility opening hours
    39, # Request human support or live agent
    3,  # Modify reservation
    39, # Request human support or live agent
    13, # Request menu or dietary information
    6,  # Request early check-in
    25, # Request spa or gym appointment
    10, # Request luggage assistance
    32, # Ask about facility opening hours
    3,  # Modify reservation
    28, # Change payment method
    2,  # Make a reservation / Book a room
    37, # Report a complaint
    5,  # Check reservation status
    23, # Ask for taxi or shuttle service
    40, # Ask for help using the chatbot
    32, # Ask about facility opening hours
    7,  # Request late check-out
    17, # Request extra towels, toiletries, or pillows
    9,  # Check-out online
    20, # Request in-room amenities
    39, # Request human support or live agent
    24, # Ask about hotel policies
    26, # Ask for invoice or receipt
    30, # Pre-authorize payment or deposit
    7,  # Request late check-out
    19, # Request laundry service
    8,  # Check-in online
    14, # Ask for breakfast hours or availability
    19, # Request laundry service
    36, # Leave a review or feedback
    17, # Request extra towels, toiletries, or pillows
    14, # Ask for breakfast hours or availability
    31, # Ask for Wi-Fi access or help
    24, # Ask about hotel policies
    32, # Ask about facility opening hours
    24, # Ask about hotel policies
    8,  # Check-in online
    37, # Report a complaint
    3,  # Modify reservation
    1,  # Check room availability
    17, # Request extra towels, toiletries, or pillows
    32, # Ask about facility opening hours
    16, # Request room cleaning
    16, # Request room cleaning
    39, # Request human support or live agent
    30, # Pre-authorize payment or deposit
    15, # Request minibar refill
    24, # Ask about hotel policies
    7,  # Request late check-out
    22, # Request a wake-up call
    40, # Ask for help using the chatbot
    20, # Request in-room amenities
    8,  # Check-in online
    13, # Request menu or dietary information
    18, # Report an issue in the room
    32, # Ask about facility opening hours
    6,  # Request early check-in
    14, # Ask for breakfast hours or availability
    39, # Request human support or live agent
    21, # Ask about local attractions or tours
    38, # Ask to speak to a manager
    3,  # Modify reservation
    13, # Request menu or dietary information
    8,  # Check-in online
    20, # Request in-room amenities
    40, # Ask for help using the chatbot
    9,  # Check-out online
    11, # Order room service
    24, # Ask about hotel policies
    18, # Report an issue in the room
    20, # Request in-room amenities
    34, # Ask about pet policy
    39, # Request human support or live agent
    17, # Request extra towels, toiletries, or pillows
    39, # Request human support or live agent
    21, # Ask about local attractions or tours
    37, # Report a complaint
    13, # Request menu or dietary information
    16, # Request room cleaning
    38, # Ask to speak to a manager
    6,  # Request early check-in
    8,  # Check-in online
    40, # Ask for help using the chatbot
    8,  # Check-in online
    20, # Request in-room amenities
    11, # Order room service
    21, # Ask about local attractions or tours
    2,  # Make a reservation / Book a room
    37, # Report a complaint
    9,  # Check-out online
    24, # Ask about hotel policies
    35, # Ask about smoking policy
    39, # Request human support or live agent
    3,  # Modify reservation
    18, # Report an issue in the room
    34, # Ask about pet policy
    38, # Ask to speak to a manager
    24, # Ask about hotel policies
    32, # Ask about facility opening hours
    9,  # Check-out online
    18  # Report an issue in the room
]

# Example of how to use these lists:
# for i, (message, mapping) in enumerate(zip(vague_messages, correct_mappings), 1):
#     print(f"{i}. Message: {message}")
#     print(f"   Correct Mapping: {mapping}")
#     print()

# Dictionary mapping intention numbers to intention names
intention_names = {
    1: "Check room availability",
    2: "Make a reservation / Book a room",
    3: "Modify reservation",
    4: "Cancel reservation",
    5: "Check reservation status",
    6: "Request early check-in",
    7: "Request late check-out",
    8: "Check-in online",
    9: "Check-out online",
    10: "Request luggage assistance",
    11: "Order room service",
    12: "Book a table at a restaurant",
    13: "Request menu or dietary information",
    14: "Ask for breakfast hours or availability",
    15: "Request minibar refill",
    16: "Request room cleaning",
    17: "Request extra towels, toiletries, or pillows",
    18: "Report an issue in the room",
    19: "Request laundry service",
    20: "Request in-room amenities",
    21: "Ask about local attractions or tours",
    22: "Request a wake-up call",
    23: "Ask for taxi or shuttle service",
    24: "Ask about hotel policies",
    25: "Request spa or gym appointment",
    26: "Ask for invoice or receipt",
    27: "Query charges on the bill",
    28: "Change payment method",
    29: "Split bill",
    30: "Pre-authorize payment or deposit",
    31: "Ask for Wi-Fi access or help",
    32: "Ask about facility opening hours",
    33: "Request parking information",
    34: "Ask about pet policy",
    35: "Ask about smoking policy",
    36: "Leave a review or feedback",
    37: "Report a complaint",
    38: "Ask to speak to a manager",
    39: "Request human support or live agent",
    40: "Ask for help using the chatbot"
}
