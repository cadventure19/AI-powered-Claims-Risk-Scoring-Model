import os
import pandas as pd
from openai import OpenAI

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.environ.get("OPENROUTER_API_KEY")
)

# Provide the path to your CSV file here
#csv_file_path = "final_data_prompt_response.csv" 
csv_file_path = "low_score_final.csv"

try:
    df = pd.read_csv(csv_file_path)
    print(f"Successfully loaded {len(df)} claims. Processing audits...\n")
except Exception as e:
    print(f"⚠️ Error reading CSV file: {e}")
    exit()

# Add the new column if it doesn't already exist (initialized with blank text)
if "llm_response" not in df.columns:
    df["llm_response"] = ""

# System prompt enforcing your strict rules
system_prompt = (
    "You are an expert healthcare risk auditor. Your task is to summarize claim risk using the provided data "
    "into a layman-friendly explanation of exactly 2 lines.\n"
    "Line 1: State the risk score, tier, and a brief, plain-English summary of why the claim is a risk based on its "
    "top features (using their raw/scaled values).\n"
    "Line 2: Provide a direct, actionable next step on what needs to be done to resolve or audit this specific case.\n"
    "Do not include any introductory or concluding text. Strictly output exactly 2 lines."
)

# Process each row in the CSV
for index, row in df.iterrows():
    # If this row was already processed in a previous run, skip it (optional safety check)
    if pd.notna(df.at[index, "llm_response"]) and str(df.at[index, "llm_response"]).strip() != "":
        continue

    # Convert the row data (excluding our new column) into a readable string format for the AI
    row_data_string = row.drop("llm_response").to_string()
    
    print(f"--- Auditing Claim Row {index + 1} / {len(df)} ---")
    
    try:
        response = client.chat.completions.create(
            model="openrouter/free", # Automatically balances across available free models
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this claim data:\n{row_data_string}"}
            ],
            temperature=0.2
        )

        bot_reply = response.choices[0].message.content.strip()
        
        # Save the result directly into the DataFrame's new column
        df.at[index, "llm_response"] = bot_reply
        print(bot_reply)
        print()

    except Exception as e:
        print(f"⚠️ Error processing row {index + 1}: {e}\n")
        # Save whatever progress we have so far before exiting
        df.to_csv(csv_file_path, index=False)
        exit()

# Save the finalized DataFrame back into the original CSV file
try:
    df.to_csv(csv_file_path, index=False)
    print(f"🎉 Success! All responses saved back to '{csv_file_path}' under the column 'llm_response'.")
except Exception as e:
    print(f"⚠️ Error saving the updated CSV file: {e}")