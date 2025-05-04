#!/usr/bin/env python3

import os
import importlib.util
import sys


def load_module_from_file(file_path):
    """
    Load a Python module from a file path
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return None

    # Get the module name from the file path
    module_name = os.path.basename(file_path).replace('.py', '')
    
    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        print(f"Error: Could not load module specification from {file_path}")
        return None
    
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module {module_name}: {str(e)}")
        return None


def check_file_format(module):
    """
    Check if the module has the expected format (contains vague_messages)
    """
    if not hasattr(module, 'vague_messages'):
        print(f"Error: Module {module.__name__} does not contain 'vague_messages'")
        return False
    return True


def find_duplicates():
    """
    Find duplicate messages across the three mapping files
    """
    # Files to compare
    base_file = "messages_mappings100.py"
    compare_files = ["messages_mappings200.py", "messages_mappings200_2.py"]
    
    # Load the base module
    base_module = load_module_from_file(base_file)
    if base_module is None or not check_file_format(base_module):
        return
    
    base_messages = base_module.vague_messages
    print(f"Loaded {len(base_messages)} messages from {base_file}")
    
    # Store duplicates
    all_duplicates = []
    
    # Compare with each file
    for compare_file in compare_files:
        compare_module = load_module_from_file(compare_file)
        if compare_module is None or not check_file_format(compare_module):
            continue
            
        compare_messages = compare_module.vague_messages
        print(f"Loaded {len(compare_messages)} messages from {compare_file}")
        
        # Find duplicates
        duplicates = []
        for i, msg in enumerate(compare_messages):
            if msg in base_messages:
                base_idx = base_messages.index(msg)
                duplicates.append({
                    "compare_file": compare_file,
                    "compare_idx": i,
                    "base_idx": base_idx,
                    "message": msg
                })
        
        print(f"Found {len(duplicates)} duplicates in {compare_file}")
        all_duplicates.extend(duplicates)
    
    return all_duplicates


def main():
    """
    Main function
    """
    print("Searching for duplicate messages...")
    duplicates = find_duplicates()
    
    if not duplicates:
        print("No duplicates found or an error occurred")
        return
    
    print("\nDuplicate messages:")
    print("=" * 80)
    
    # Group duplicates by file
    by_file = {}
    for dup in duplicates:
        compare_file = dup["compare_file"]
        if compare_file not in by_file:
            by_file[compare_file] = []
        by_file[compare_file].append(dup)
    
    # Print duplicates by file
    for file, file_dups in by_file.items():
        print(f"\nDuplicates in {file}:")
        print("-" * 50)
        for dup in file_dups:
            print(f"  Index in {file}: {dup['compare_idx']}")
            print(f"  Index in messages_mappings100.py: {dup['base_idx']}")
            print(f"  Message: \"{dup['message']}\"")
            print()
    
    # Summary
    print("\nSummary:")
    print("=" * 80)
    for file, file_dups in by_file.items():
        print(f"{file}: {len(file_dups)} duplicates")
    print(f"Total duplicates: {len(duplicates)}")


if __name__ == "__main__":
    main() 