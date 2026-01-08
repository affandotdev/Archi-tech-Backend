import requests
import json
import sys

def test_explain_endpoint():
    url = "http://127.0.0.1:8002/ai/explain"
    
    # Payload matching calculate_cost and the endpoint expectation
    payload = {
        "plot_length_ft": 40,
        "plot_width_ft": 60,
        "floors": 2,
        "location": "city",
        "building_type": "residential",
        "quality": "standard",
        "budget_lakhs": 50
    }

    try:
        print(f"Sending request to {url}...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("\n✅ Success! Service is working.")
            data = response.json()
            print("\nResponse:")
            print(f"Estimate: {data.get('estimate')}")
            print(f"AI Assisted: {data.get('ai_assisted')}")
            print(f"Explanation Preview: {data.get('explanation')[:100]}...")
            print(f"RAG Evidence Count: {len(data.get('rag_evidence', []))}")
        else:
            print(f"\n❌ Failed with status code: {response.status_code}")
            print(f"Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the service.")
        print("Is the server running? Try running: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_explain_endpoint()
