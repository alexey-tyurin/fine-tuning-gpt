#!/usr/bin/env python3

import os
import json
import time
import argparse
from openai import OpenAI
from datetime import datetime

# Initialize the OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

# File to store IDs for each step
IDS_FILE = "openai_dpo_ids.json"

def load_ids():
    """Load previously saved IDs from file"""
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"file_id": None, "job_id": None}
    return {"file_id": None, "job_id": None}

def save_ids(ids_dict):
    """Save IDs to file for later use"""
    with open(IDS_FILE, 'w') as f:
        json.dump(ids_dict, f, indent=2)

def upload_training_file():
    """
    Upload DPO training data file to OpenAI API
    Reference: https://platform.openai.com/docs/api-reference/files
    """
    print("Uploading DPO training file...")
    
    try:
        # Upload the data to OpenAI
        response = client.files.create(
            file=open("dpo_tests.jsonl", "rb"),
            purpose="fine-tune"
        )

        file_id = response.id
        
        # Print all returned fields
        print("\nFile uploaded successfully:")
        print(f"File ID: {file_id}")
        print(f"Status: {response.status}")
        print(f"Created at: {response.created_at}")
        
        # Save the ID for later use
        ids = load_ids()
        ids["file_id"] = file_id
        save_ids(ids)
        
        return file_id
    except Exception as e:
        print(f"Error uploading training file: {str(e)}")
        return None

def create_fine_tuning_job(file_id=None):
    """
    Create a DPO fine-tuning job using the uploaded file
    Reference: https://platform.openai.com/docs/api-reference/fine-tuning/create
    """
    print("Creating DPO fine-tuning job...")
    
    # Use file_id from parameter or load from saved IDs
    if file_id is None:
        ids = load_ids()
        file_id = ids.get("file_id")
        if not file_id:
            print("Error: No file ID available. Please upload a file first.")
            return None
    
    try:
        # Create fine-tuning job with DPO hyperparameters
        response = client.fine_tuning.jobs.create(
            training_file=file_id,
            model="ft:gpt-4o-mini-2024-07-18:personal:sft200:BTfrZIAI",  # Specify the model to fine-tune
            method={
                "type": "dpo",
                "dpo": {
                    "hyperparameters": {
                        "n_epochs": 1,
                        "batch_size": 1,
                        "learning_rate_multiplier": 0.3,
                        "beta": 0.1
                    },
                },
            },
            seed=42,
            suffix="dpo"
        )
        
        job_id = response.id
        
        # Print all returned fields
        print("\nDPO fine-tuning job created successfully:")
        print(f"Job ID: {job_id}")
        print(f"Model: {response.model}")
        print(f"Status: {response.status}")
        print(f"Created at: {response.created_at}")
        
        # Save the ID for later use
        ids = load_ids()
        ids["job_id"] = job_id
        save_ids(ids)
        
        return job_id
    except Exception as e:
        print(f"Error creating DPO fine-tuning job: {str(e)}")
        return None

def check_fine_tuning_status(job_id=None):
    """
    Check the status of a DPO fine-tuning job
    Reference: https://platform.openai.com/docs/api-reference/fine-tuning/retrieve
    """
    print("Checking DPO fine-tuning job status...")
    
    # Use job_id from parameter or load from saved IDs
    if job_id is None:
        ids = load_ids()
        job_id = ids.get("job_id")
        if not job_id:
            print("Error: No job ID available. Please create a fine-tuning job first.")
            return None
    
    try:
        # Get job status
        response = client.fine_tuning.jobs.retrieve(job_id)
        
        # Print job details
        print(f"\nJob ID: {job_id}")
        print(f"Status: {response.status}")
        print(f"Created at: {response.created_at}")
        
        if response.finished_at:
            print(f"Finished at: {response.finished_at}")
        
        # Print training metrics if available
        if hasattr(response, "training_metrics") and response.training_metrics:
            print("\nTraining metrics:")
            for key, value in response.training_metrics.items():
                print(f"{key}: {value}")
        
        # Check if the job is still in progress
        if response.status in ["validating_files", "queued", "running"]:
            print("\nJob is still in progress. Check back later for results.")
            return response
        
        # If job is completed
        if response.status == "succeeded":
            print(f"\nDPO fine-tuning job completed successfully!")
            print(f"Fine-tuned model ID: {response.fine_tuned_model}")
            return response
        
        # If job failed
        if response.status in ["failed", "cancelled"]:
            print(f"\nDPO fine-tuning job {response.status}.")
            if hasattr(response, "error") and response.error:
                print(f"Error: {response.error}")
            return response
        
        return response
    except Exception as e:
        print(f"Error checking fine-tuning job status: {str(e)}")
        return None

def analyze_results(job_id=None):
    """
    Analyze the results of the DPO fine-tuning job
    """
    print("Analyzing DPO fine-tuning job results...")
    
    # Use job_id from parameter or load from saved IDs
    if job_id is None:
        ids = load_ids()
        job_id = ids.get("job_id")
        if not job_id:
            print("Error: No job ID available. Please create a fine-tuning job first.")
            return None
    
    try:
        # Retrieve job details
        response = client.fine_tuning.jobs.retrieve(job_id)
        
        # Check if job has completed
        if response.status != "succeeded":
            print(f"Job status is '{response.status}', not 'succeeded'. Cannot analyze results yet.")
            return None
        
        # Get fine-tuned model ID
        fine_tuned_model = response.fine_tuned_model
        if not fine_tuned_model:
            print("No fine-tuned model ID found.")
            return None
        
        print(f"\nFine-tuned model ID: {fine_tuned_model}")
        
        # Get training metrics
        if hasattr(response, "training_metrics") and response.training_metrics:
            print("\nTraining metrics:")
            for key, value in response.training_metrics.items():
                print(f"{key}: {value}")
        
        # Get result files if available
        if hasattr(response, "result_files") and response.result_files:
            print("\nResult files:")
            for file_id in response.result_files:
                print(f"File ID: {file_id}")
                # Download and analyze result files if needed
        
        # Test the fine-tuned model on a few examples
        print("\nTesting DPO fine-tuned model on examples...")
        
        # Load a few test examples from dpo_tests.jsonl for testing
        try:
            with open("dpo_tests.jsonl", "r") as f:
                test_examples = [json.loads(line) for line in f][:5]  # Use first 5 examples
            
            # Test each example with the fine-tuned model
            correct_count = 0
            total_count = 0
            
            for idx, example in enumerate(test_examples):
                # Extract messages from the example
                messages = example["input"]["messages"]
                system_message = messages[0]["content"]
                user_message = messages[1]["content"]
                preferred_label = example["preferred_output"][0]["content"]
                
                total_count += 1
                
                print(f"\nExample {idx+1}:")
                print(f"Input: {user_message}")
                print(f"Preferred label: {preferred_label}")
                
                # Query the fine-tuned model
                try:
                    completion = client.chat.completions.create(
                        model=fine_tuned_model,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=10,
                        temperature=0.0  # Use deterministic output for testing
                    )
                    
                    # Get the model's prediction
                    prediction = completion.choices[0].message.content.strip()
                    print(f"Model prediction: {prediction}")
                    
                    # Check if prediction matches preferred label
                    is_correct = prediction == preferred_label
                    if is_correct:
                        correct_count += 1
                    print(f"Correct: {is_correct}")
                    
                except Exception as e:
                    print(f"Error testing example: {str(e)}")
            
            print(f"\nTesting accuracy: {correct_count}/{total_count} ({correct_count/total_count*100 if total_count > 0 else 0:.2f}%)")
            
        except Exception as e:
            print(f"Error loading or testing examples: {str(e)}")
        
        # Save the analysis results to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"dpo_analysis_{timestamp}.json"
        
        analysis_results = {
            "job_id": job_id,
            "fine_tuned_model": fine_tuned_model,
            "status": response.status,
            "created_at": str(response.created_at),
            "finished_at": str(response.finished_at) if response.finished_at else None,
            "training_metrics": response.training_metrics if hasattr(response, "training_metrics") else None,
            "timestamp": timestamp
        }
        
        with open(result_file, "w") as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"\nAnalysis results saved to {result_file}")
        
        return analysis_results
        
    except Exception as e:
        print(f"Error analyzing DPO fine-tuning job results: {str(e)}")
        return None

def run_all():
    """
    Run all steps in sequence
    """
    print("Starting complete DPO fine-tuning process...")

    # Step 1: Upload training file
    file_id = upload_training_file()
    if not file_id:
        print("Failed to upload training file. Aborting.")
        return

    # Step 2: Create fine-tuning job
    job_id = create_fine_tuning_job(file_id)
    if not job_id:
        print("Failed to create DPO fine-tuning job. Aborting.")
        return
    
    # Step 3: Monitor the job status
    print("\nMonitoring DPO job status. This may take some time...")
    status = None
    max_checks = 30
    check_count = 0
    
    while check_count < max_checks:
        response = check_fine_tuning_status(job_id)
        if not response:
            print("Failed to check job status. Aborting.")
            return
        
        status = response.status
        
        # If job is complete or failed, break the loop
        if status in ["succeeded", "failed", "cancelled"]:
            break
        
        # Wait before checking again
        print("Waiting 60 seconds before checking again...")
        time.sleep(60)
        check_count += 1
    
    # Step 4: Analyze results if job succeeded
    if status == "succeeded":
        analyze_results(job_id)
    else:
        print(f"DPO fine-tuning job did not succeed (status: {status}). Skipping analysis.")
    
    print("DPO fine-tuning process completed.")

def main():
    """
    Main function to parse arguments and run the appropriate step
    """
    parser = argparse.ArgumentParser(description='OpenAI DPO Fine-Tuning Process')
    
    # Add arguments for each step
    parser.add_argument('--upload', action='store_true', help='Upload DPO training file')
    parser.add_argument('--create', action='store_true', help='Create a DPO fine-tuning job')
    parser.add_argument('--status', action='store_true', help='Check the status of a DPO fine-tuning job')
    parser.add_argument('--analyze', action='store_true', help='Analyze the results of a DPO fine-tuning job')
    parser.add_argument('--all', action='store_true', help='Run all steps in sequence')
    
    # Add arguments for IDs
    parser.add_argument('--file-id', type=str, help='File ID for operations that require it')
    parser.add_argument('--job-id', type=str, help='Job ID for operations that require it')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any([args.upload, args.create, args.status, args.analyze, args.all]):
        parser.print_help()
        return
    
    # Run the appropriate step based on the arguments
    if args.all:
        run_all()
    else:
        if args.upload:
            upload_training_file()

        if args.create:
            create_fine_tuning_job(args.file_id)
        
        if args.status:
            check_fine_tuning_status(args.job_id)
        
        if args.analyze:
            analyze_results(args.job_id)

if __name__ == "__main__":
    main() 