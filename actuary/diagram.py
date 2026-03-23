import sys
import json
import random

def generate_diagram(data):
    # In a real environment with the Excalidraw MCP server connected, 
    # the LLM or this script would use `createNode`, `createTextElement`, etc.
    # to programmatically draw the specific Risk layout onto the canvas.
    # For this tutorial, we will mock the return URL.
    
    diagram_id = random.randint(1000000000000, 9999999999999)
    # Generate mock 22-character encryption key
    encryption_key = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=22))
    
    url = f"https://excalidraw.com/#json={diagram_id},{encryption_key}"
    print(url)
    return url

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
            generate_diagram(data)
        except:
            print("https://excalidraw.com/#json=mock123,key456")
    else:
        print("https://excalidraw.com/#json=mock123,key456")
