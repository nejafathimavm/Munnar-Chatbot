"""
==============================================================
        Munnar Stay & Food Guide Chatbot
                Groq API Edition
==============================================================

SETUP:
  1. pip install groq
  2. Replace YOUR_GROQ_API_KEY_HERE with your Groq key
     Get free key from: https://console.groq.com
  3. Run: python munnar_chatbot.py
"""

from groq import Groq
import os
import time

# -------------------------------------------------------------
# API KEY (Use Environment Variable Recommended)
# -------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "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"

MODEL = "llama-3.3-70b-versatile"

# -------------------------------------------------------------
# MUNNAR HOTEL + FOOD DATABASE (ASCII CLEANED)
# -------------------------------------------------------------
MUNNAR_DATA = """
You are a friendly and knowledgeable Munnar Travel, Stay and Food Guide chatbot.
You help tourists find the best hotels, resorts, and homestays in Munnar, Kerala.
You provide full details about check-in/check-out timings, complete food menus,
nearby tourist places, prices, and travel tips.
Always be warm, helpful, and conversational like a local guide.

--------------------------------------------------
HOTEL 1 - BLANKET HOTEL AND SPA (5-Star)
--------------------------------------------------
Location     : 3 miles from Munnar town center
Type         : Luxury Resort
Price        : Rs. 8000 - Rs. 20000 per night
Check-in     : 2:00 PM
Check-out    : 12:00 PM (Noon)

Highlights:
- Multi-cuisine restaurant
- Candlelight dinner available
- Complimentary morning tea
- Kerala Sadhya on Fridays

Nearby:
- Eravikulam National Park (4 km)
- Mattupetty Dam (6 km)
- Tea Museum (3 km)

--------------------------------------------------
HOTEL 2 - THE PANORAMIC GETAWAY (5-Star)
--------------------------------------------------
Location     : Hilltop, 4 miles from Munnar
Price        : Rs. 10000 - Rs. 25000
Check-out    : 11:00 AM

Highlights:
- Valley view rooms
- Rooftop dining
- BBQ Fridays
- Complimentary evening tea

Nearby:
- Anamudi Peak
- Top Station
- Kundala Lake

--------------------------------------------------
HOTEL 3 - FRAGRANT NATURE MUNNAR
--------------------------------------------------
Price        : Rs. 7500 - Rs. 18000
Check-in     : 1:00 PM

Highlights:
- Spice garden experience
- Ayurvedic meals
- Live dosa Sundays

--------------------------------------------------
HOTEL 4 - T AND U LEISURE HOTEL
--------------------------------------------------
Price        : Rs. 3500 - Rs. 7000

Highlights:
- Budget friendly
- Rooftop restaurant
- Candlelight dinner

--------------------------------------------------
HOTEL 5 - HOTEL C7
--------------------------------------------------
Price        : Rs. 2500 - Rs. 5000

Highlights:
- Tea garden views
- Free tea tasting
- Guided tea walk

--------------------------------------------------
HOTEL 6 - MUNNAR INN
--------------------------------------------------
Price        : Rs. 2000 - Rs. 4000

Highlights:
- Located in town
- Budget meals
- 24 hour service

--------------------------------------------------
HOTEL 7 - NATURE ZONE JUNGLE RESORT
--------------------------------------------------
Price        : Rs. 3000 - Rs. 8000

Highlights:
- Treehouses and tents
- Campfire dinner
- Bamboo biriyani
- Organic food

--------------------------------------------------
HOTEL 8 - SPRINGDALE HERITAGE
--------------------------------------------------
Price        : Rs. 5000 - Rs. 12000

Highlights:
- Colonial style stay
- High tea experience
- Garden dining

--------------------------------------------------
TOP TOURIST PLACES
--------------------------------------------------
1. Eravikulam National Park
2. Mattupetty Dam
3. Echo Point
4. Top Station
5. Tea Museum
6. Anamudi Peak
7. Kundala Lake
8. Attukal Waterfalls

--------------------------------------------------
MUST TRY FOODS
--------------------------------------------------
- Appam and stew
- Puttu and kadala curry
- Kerala fish curry
- Bamboo biriyani
- Payasam
- Banana fritters

--------------------------------------------------
TRAVEL TIPS
--------------------------------------------------
Best time     : October to March
Monsoon       : June to September
Airport       : Cochin International Airport
Temperature   : 5C to 25C
"""

# -------------------------------------------------------------
# SESSION MEMORY
# -------------------------------------------------------------
conversation_history = []
MAX_HISTORY = 10

# -------------------------------------------------------------
# INIT CLIENT (ONLY ONCE)
# -------------------------------------------------------------
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------------------------------
# CHAT FUNCTION
# -------------------------------------------------------------
def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Limit memory
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

    messages = [{"role": "system", "content": MUNNAR_DATA}] + conversation_history

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=1200,
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

# -------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------
def main():
    print("==========================================================")
    print("     Munnar Stay and Food Guide Chatbot")
    print("==========================================================")
    print("Ask about hotels, food, timings, tourist places.")
    print("Type 'exit' to quit.")
    print("==========================================================\n")

    print("Try asking:")
    print(" - Show me all hotels in Munnar")
    print(" - Best honeymoon hotel")
    print(" - Budget hotels under 4000")
    print(" - Which hotel has bamboo biriyani?")
    print(" - Tourist places in Munnar\n")

    if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        print("[WARNING] Add your Groq API key first!")
        print("Get it from: https://console.groq.com\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Happy travels to Munnar!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye", "q"}:
            print("\nBot: Thank you! Enjoy your trip to Munnar!")
            break

        try:
            print("\nBot is thinking...\n")
            time.sleep(1)

            reply = chat(user_input)
            print(f"Bot: {reply}\n")

        except Exception as e:
            error = str(e)
            if "401" in error or "invalid_api_key" in error:
                print("\n[ERROR] Invalid Groq API key.")
                break
            elif "rate_limit" in error.lower():
                print("\n[ERROR] Rate limit hit. Try again later.\n")
            else:
                print(f"\n[ERROR] {error}\n")


if __name__ == "__main__":
    main()