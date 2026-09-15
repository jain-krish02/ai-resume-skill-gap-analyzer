import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6JqZlNtEwcQlatKp3mbnlgA6Lso7KOPmMQPKQFJGg61og")
model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content("hello")
    print("SUCCESS")
    print(response.text)
except Exception as e:
    print("ERROR")
    print(e)
