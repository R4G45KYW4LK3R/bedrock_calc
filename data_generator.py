#data_generator.py

import boto3
import json
import time

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_qa_pairs(num_pairs=100):
    """Generate scientific Q&A pairs using Nova Pro"""
    
    prompt = """Generate 5 diverse scientific question-answer pairs. Cover topics like physics, chemistry, biology, astronomy, earth science, and general science. Make questions natural and conversational. Keep answers clear, accurate, and 1-2 sentences.

Format each pair EXACTLY like this (no extra spacing):
Q: [question]
A: [answer]

Example:
Q: Why do leaves change color in fall?
A: Leaves change color because chlorophyll breaks down in cooler temperatures, revealing yellow and orange pigments that were always present.

Now generate 5 different scientific Q&A pairs:"""

    all_pairs = []
    batches = num_pairs // 5  # Generate 5 at a time
    
    print(f"Generating {num_pairs} Q&A pairs using Nova Pro...")
    print("This will take a few minutes...\n")
    
    for i in range(batches):
        try:
            # Call Nova Pro via Bedrock API
            response = bedrock.invoke_model(
                modelId='us.amazon.nova-pro-v1:0',
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"text": prompt}]
                        }
                    ],
                    "inferenceConfig": {
                        "max_new_tokens": 1000,
                        "temperature": 0.8
                    }
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            generated_text = response_body['output']['message']['content'][0]['text']
            
            # Extract Q&A pairs
            pairs = parse_qa_pairs(generated_text)
            all_pairs.extend(pairs)
            
            print(f"Batch {i+1}/{batches} complete - Generated {len(all_pairs)} pairs so far")
            
            # Small delay to avoid rate limits
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in batch {i+1}: {str(e)}")
            continue
    
    return all_pairs[:num_pairs]  # Return exactly num_pairs

def parse_qa_pairs(text):
    """Parse Q&A pairs from generated text"""
    pairs = []
    lines = text.strip().split('\n')
    
    current_q = None
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            current_q = line[2:].strip()
        elif line.startswith('A:') and current_q:
            answer = line[2:].strip()
            pairs.append({'question': current_q, 'answer': answer})
            current_q = None
    
    return pairs

def format_for_bedrock(qa_pairs):
    """Convert Q&A pairs to Bedrock distillation format"""
    formatted_data = []
    
    for pair in qa_pairs:
        formatted_data.append({
            "schemaVersion": "bedrock-conversation-2024",
            "system": [{
                "text": "A chat between a curious User and an artificial intelligence Bot. The Bot gives helpful, detailed, and polite answers to the User's questions."
            }],
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": pair['question']}]
                },
                {
                    "role": "assistant",
                    "content": [{"text": pair['answer']}]
                }
            ]
        })
    
    return formatted_data

def main():
    # Generate pairs
    qa_pairs = generate_qa_pairs(100)
    
    print(f"\n✓ Successfully generated {len(qa_pairs)} Q&A pairs!")
    
    # Format for Bedrock
    formatted_data = format_for_bedrock(qa_pairs)
    
    # Save to JSONL file (one JSON object per line)
    output_file = 'distillation_training_data.jsonl'
    with open(output_file, 'w') as f:
        for item in formatted_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"✓ Saved to {output_file}")
    print(f"\nYou can now upload this file to your S3 bucket!")
    print("\nFirst 3 examples:")
    for i, pair in enumerate(qa_pairs[:3], 1):
        print(f"\n{i}. Q: {pair['question']}")
        print(f"   A: {pair['answer']}")

if __name__ == "__main__":
    main()