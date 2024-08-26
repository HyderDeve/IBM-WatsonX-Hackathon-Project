import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/search"

def main():
    st.title("Customer Service App")

    user_id = st.text_input("Enter your user ID:")
    query = st.text_area("Enter your query:")

    if st.button("Search"):
        if not user_id or not query:
            st.error("Please provide both User ID and Query.")
            return
        
        response = requests.post(API_URL, json={"user_id": user_id, "query": query})
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                for result in results:
                    st.write(f"**Document ID:** {result['document_id']}")
                    st.write(f"**Content:** {result['content']}")
                    st.write(f"**Score:** {result['score']:.4f}")
                    st.write("---")
            else:
                st.write("No results found.")
        else:
            st.error(f"Failed to fetch results: {response.status_code}")

if __name__ == "__main__":
    main()
