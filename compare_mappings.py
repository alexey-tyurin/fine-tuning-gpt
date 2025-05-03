import os

def read_messages_from_file(file_path):
    """Read vague_messages from a file by directly parsing the file contents"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Find where vague_messages starts
        start_index = content.find("vague_messages = [")
        if start_index == -1:
            print(f"Could not find vague_messages in {file_path}")
            return None
            
        # Find where correct_mappings starts (this marks the end of vague_messages)
        end_index = content.find("correct_mappings = [", start_index)
        if end_index == -1:
            print(f"Could not find correct_mappings in {file_path}")
            return None
            
        # Extract the vague_messages part
        messages_str = content[start_index:end_index].strip()
        
        # Parse the messages from the string
        messages = []
        # Skip the first line which is "vague_messages = ["
        lines = messages_str.split('\n')[1:]
        
        for line in lines:
            line = line.strip()
            if line.startswith('"') or line.startswith("'"):
                # Remove the comma at the end and the quotes
                message = line.rstrip(',').strip('"\'')
                messages.append(message)
            elif line == "]," or line == "]":
                # End of the list
                break
                
        print(f"Successfully read {len(messages)} messages from {file_path}")
        return messages
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def read_mappings_from_file(file_path):
    """Read correct_mappings from a file by directly parsing the file contents"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Find where correct_mappings starts
        start_index = content.find("correct_mappings = [")
        if start_index == -1:
            print(f"Could not find correct_mappings in {file_path}")
            return None
        
        # Extract the content after correct_mappings
        mappings_content = content[start_index:]
        
        # Find where the list ends - either end of file or next major section
        # Looking for closing bracket followed by new line
        end_pattern = "]\n\n"
        end_index = mappings_content.find(end_pattern)
        if end_index == -1:
            # Try alternative pattern - end of list at end of file
            end_pattern = "]\n"
            end_index = mappings_content.find(end_pattern)
            if end_index == -1:
                # Just take everything until end if we can't find a clean end
                end_index = len(mappings_content)
            else:
                end_index += len(end_pattern)
        else:
            end_index += len(end_pattern)
            
        # Extract the mappings section
        mappings_section = mappings_content[:end_index].strip()
        
        # Parse the mappings
        mappings = []
        # Skip the first line which is "correct_mappings = ["
        lines = mappings_section.split('\n')[1:]
        
        for line in lines:
            line = line.strip()
            # Extract the number at the beginning of the line
            if line and line[0].isdigit():
                # Extract just the number part
                if ',' in line:
                    mapping = line.split(',')[0].strip()
                else:
                    mapping = line.strip()
                    
                if mapping.isdigit():
                    mappings.append(mapping)
            elif line == "]" or line == "],":
                # End of the list
                break
        
        print(f"Successfully read {len(mappings)} mappings from {file_path}")
        return mappings
    except Exception as e:
        print(f"Error reading mappings from {file_path}: {e}")
        return None

# File paths
file_100 = 'messages_mappings100.py'
file_200 = 'messages_mappings200.py'
file_200_2 = 'messages_mappings200_2.py'

# Read messages from files
print("Reading messages from files...")
messages_100 = read_messages_from_file(file_100)
messages_200 = read_messages_from_file(file_200)
messages_200_2 = read_messages_from_file(file_200_2)

# Read mappings from files
print("\nReading mappings from files...")
mappings_100 = read_mappings_from_file(file_100)
mappings_200 = read_mappings_from_file(file_200)
mappings_200_2 = read_mappings_from_file(file_200_2)

if not all([messages_100, messages_200, messages_200_2, mappings_100, mappings_200, mappings_200_2]):
    print("Failed to read messages or mappings from one or more files. Exiting.")
    exit(1)

print(f"\nFile summary:")
print(f"- messages_mappings100.py: {len(messages_100)} messages, {len(mappings_100)} mappings")
print(f"- messages_mappings200.py: {len(messages_200)} messages, {len(mappings_200)} mappings")
print(f"- messages_mappings200_2.py: {len(messages_200_2)} messages, {len(mappings_200_2)} mappings")

# Find duplicates between messages_100 and messages_200
duplicates_200 = []
for i, msg in enumerate(messages_200):
    if msg in messages_100:
        j = messages_100.index(msg)
        duplicates_200.append((i, j, msg, mappings_200[i], mappings_100[j]))

# Find duplicates between messages_100 and messages_200_2
duplicates_200_2 = []
for i, msg in enumerate(messages_200_2):
    if msg in messages_100:
        j = messages_100.index(msg)
        duplicates_200_2.append((i, j, msg, mappings_200_2[i], mappings_100[j]))

# Print results
print('\n=== Duplicates in messages_mappings200.py ===')
if duplicates_200:
    print(f"Found {len(duplicates_200)} duplicates")
    for i, j, msg, mapping_200, mapping_100 in duplicates_200:
        print(f'Index in file_200: {i}, Index in file_100: {j}')
        print(f'Message: "{msg}"')
        print(f'Mapping in file_200: {mapping_200}, Mapping in file_100: {mapping_100}')
        print()
else:
    print('No duplicates found')

print('\n=== Duplicates in messages_mappings200_2.py ===')
if duplicates_200_2:
    print(f"Found {len(duplicates_200_2)} duplicates")
    for i, j, msg, mapping_200_2, mapping_100 in duplicates_200_2:
        print(f'Index in file_200_2: {i}, Index in file_100: {j}')
        print(f'Message: "{msg}"')
        print(f'Mapping in file_200_2: {mapping_200_2}, Mapping in file_100: {mapping_100}')
        print()
else:
    print('No duplicates found') 