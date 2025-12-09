from openai import OpenAI
import re
# import os  # recommended if you store the key in env vars

# Azure OpenAI endpoint MUST include /openai/v1/
ENDPOINT = "https://ai-ajayrathi0811ai883120795644.cognitiveservices.azure.com/openai/v1"
DEPLOYMENT_NAME = "gpt-5-mini"  # this is the *deployment* name in Azure

API_KEY = "Fsdk2dZqKMl8Fkcnp8hszx7licSorXzvmIrPXjxnpT2Eh4Q2tuYwJQQJ99BKACHYHv6XJ3w3AAAAACOGR7n8"

client = OpenAI(
    api_key=API_KEY,
    base_url=ENDPOINT,
)

def smart_response_generation(text: str):
    try:
        prompt = (
            "Generate 3 responses to the email content provided below "
            "with less than 5 words each. "
            "Return the replies as double-quoted strings.\n\n"
            f"EMAIL:\n{text}"
        )

        completion = client.chat.completions.create(
            model=DEPLOYMENT_NAME,          # Azure deployment name
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        ai_text = completion.choices[0].message.content.strip()
        print("AI Response:", ai_text)

    except Exception as e:
        print("ERROR:", e)
        return [
            "More info soon.",
            "Thanks, will reply.",
            "Will get back.",
        ]

    # Extract up to 3 strings inside double quotes
    matches = re.findall(r'"(.*?)"', ai_text)
    return matches[:3]


if __name__ == "__main__":
    sample_text = "Could you please provide an update on the project status?"
    import time
    start_time = time.time()
    replies = smart_response_generation(sample_text)
    print(replies)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")