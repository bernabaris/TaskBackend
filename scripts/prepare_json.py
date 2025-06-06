#!/usr/bin/env python3
import json
import os
from pathlib import Path

def process_json_file(file_path):
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        if not content:  # Skip empty files
            print(f"Skipping empty file: {file_path}")
            return
            
        # Remove any existing array brackets and extra whitespace
        content = content.strip()
        if content.startswith('['):
            content = content[1:]
        if content.endswith(']'):
            content = content[:-1]
        
        # Split content into documents
        documents = []
        current_doc = ""
        brace_count = 0
        in_string = False
        escape_next = False
        
        for char in content:
            if not escape_next and char == '"':
                in_string = not in_string
            elif not escape_next and char == '\\':
                escape_next = True
            else:
                escape_next = False
                
            current_doc += char
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Clean up the document and add it to the list
                        doc = current_doc.strip()
                        if doc:
                            documents.append(doc)
                        current_doc = ""
        
        if not documents:
            print(f"No valid documents found in: {file_path}")
            return
            
        # Combine documents into an array format
        formatted_content = "[\n  " + ",\n  ".join(documents) + "\n]"
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
            
        print(f"Successfully processed: {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    # Get the data directory path
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Process each JSON file
    for file_path in data_dir.glob('*.json'):
        print(f"\nProcessing: {file_path}")
        process_json_file(file_path)

if __name__ == "__main__":
    main() 