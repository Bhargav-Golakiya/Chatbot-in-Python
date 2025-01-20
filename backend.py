import openai
import os
import time

# Get the API key securely (set the OPENAI_API_KEY environment variable in your system)
openai.api_key = "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"

# Initialize the conversation history
messages = []

# Ask the user to define the chatbot's purpose
system_msg = input("What type of chatbot would you like to create? (e.g., teacher, assistant, etc.)\n")
messages.append({"role": "system", "content": system_msg})

print("\nYour new assistant is ready! Type 'quit()' to exit.\n")

# Max conversation history to avoid exceeding token limits
MAX_HISTORY_LENGTH = 10

while True:
    # Get user input
    user_input = input("You: ")
    
    # Check if the user wants to quit
    if user_input.strip().lower() == "quit()":
        print("Goodbye!")
        break

    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    # Trim conversation history if it exceeds the maximum length
    if len(messages) > MAX_HISTORY_LENGTH:
        messages = messages[-MAX_HISTORY_LENGTH:]

    # Retry logic to handle rate limit errors
    while True:
        try:
            # Introduce a short delay to avoid hitting rate limits
            time.sleep(1)  # Wait 1 second before sending the request

            # Make an API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            # Extract the assistant's reply
            reply = response["choices"][0]["message"]["content"]

            # Add the assistant's reply to the conversation history
            messages.append({"role": "assistant", "content": reply})

            # Print the assistant's reply
            print("\nAssistant: " + reply + "\n")
            break  # Exit the retry loop after a successful response

        except openai.error.RateLimitError:
            print("Rate limit exceeded. Retrying in 10 seconds...")
            time.sleep(10)  # Wait 10 seconds before retrying
        except openai.error.AuthenticationError:
            print("Error: Invalid API key. Please check your OpenAI API key.")
            exit()
        except openai.error.APIConnectionError:
            print("Error: Unable to connect to OpenAI's API. Check your internet connection.")
            time.sleep(5)  # Retry after 5 seconds
        except openai.error.InvalidRequestError as e:
            print(f"Error: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
