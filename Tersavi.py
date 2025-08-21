# tersavi.py

# Simulate entering Tersavi
print("You are about to enter Tersavi\n")

# Display version and statistics messages
print("Please Download latest TERSAVI version (2025 August V 15.6)")
print("Please Upload Statistics 111\n")

# Prompt for username and password
print("Tersavi Wants to acsses Terminal V")
print("Please Enter Username and Password (Make your OWN!)")

# Get username input from the user
username = input("Username: ")

# Get password input from the user (for security, input() doesn't hide characters)
password = input("Password: ")

# Display welcome message
print(f"\nWelcome to TERSAVI, {username}!")

print("\n--- Tersavi Command Center ---")

import asyncio
import json
import ssl # Import the ssl module
import certifi # Import the certifi module

# For making HTTP requests in Python
# If you don't have it, install it using: pip install aiohttp
import aiohttp

async def search_with_gemini_api(prompt):
    """
    Makes a fetch call to the Gemini API to generate content based on the prompt.
    """
    print(f"Searching for: '{prompt}' (Please wait, this might take a moment)...")

    # >>> IMPORTANT: PASTE YOUR GEMINI API KEY HERE <<<
    # Example: apiKey = "YOUR_ACTUAL_GEMINI_API_KEY_GOES_HERE"
    apiKey = "AIzaSyA46deUiX0csGGgToIEZstdz9RNN8kNmME" # <--- Replace "" with your actual API key here!
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={apiKey}"

    chatHistory = []
    chatHistory.append({ "role": "user", "parts": [{ "text": prompt }] })
    payload = { "contents": chatHistory }

    # Create an SSL context using certificates from certifi
    # This tells aiohttp to use these trusted certificates for secure connections.
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Implement exponential backoff for retries
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            # Pass the custom SSL context to aiohttp.ClientSession
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with session.post(apiUrl, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)) as response:
                    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                    result = await response.json()

            if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "No results found from Gemini API."

        except aiohttp.ClientResponseError as e:
            if e.status == 429: # Too Many Requests
                retries += 1
                wait_time = 2 ** retries # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"HTTP Error: {e.status} - {e.message}")
                return "An error occurred while connecting to the Gemini API."
        except aiohttp.ClientClientError as e: # Catch the specific client error for aiohttp
            print(f"Network or Client Error: {e}")
            return "A network error occurred while trying to reach the Gemini API. Please check your internet connection."
        except json.JSONDecodeError:
            print("Error decoding JSON response from Gemini API.")
            return "An invalid response was received from the Gemini API."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred during the search."
    return "Failed to get a response after multiple retries."


# Main loop for interaction
async def main():
    while True:
        user_query = input("\nEnter your query for Tersavi search (or 'exit' to quit): ")
        if user_query.lower() == 'exit':
            print("Exiting Tersavi. Goodbye!")
            break
        
        # Call the asynchronous search function
        response = await search_with_gemini_api(user_query)
        print("\n--- Search Result ---")
        print(response)
        print("---------------------\n")

# Run the asynchronous main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting Tersavi. Goodbye!")

