#!/usr/bin/env python3
"""
Quick test script to verify Azure OpenAI connection
"""

from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

# Load environment variables
load_dotenv()

def test_azure_openai_connection():
    """Test Azure OpenAI connection with current credentials"""
    print("🔧 Testing Azure OpenAI Connection...")
    print("=" * 50)
    
    try:
        # Get API key
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        if not api_key:
            print("❌ AZURE_OPENAI_API_KEY not found in .env file")
            return False
        
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-10:]}")
        
        # Initialize Azure OpenAI
        print("🔄 Initializing Azure OpenAI client...")
        azure_llm = AzureChatOpenAI(
            azure_deployment="gpt-4o",
            openai_api_version="2025-01-01-preview",
            azure_endpoint="https://ireno-interns-openai.openai.azure.com/",
            api_key=api_key,
            temperature=0
        )
        
        print("✅ Azure OpenAI client created successfully")
        
        # Test a simple API call
        print("🔄 Testing API call with simple message...")
        test_messages = [("human", "Hello, what is your name?")]
        
        response = azure_llm.invoke(test_messages)
        print(f"✅ API call successful!")
        print(f"📝 Response: {response.content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        
        # Specific error diagnosis
        error_str = str(e).lower()
        if "unauthorized" in error_str or "401" in error_str:
            print("🔍 Diagnosis: Invalid API key or expired credentials")
        elif "forbidden" in error_str or "403" in error_str:
            print("🔍 Diagnosis: API key lacks permission for this operation")
        elif "timeout" in error_str or "connection" in error_str:
            print("🔍 Diagnosis: Network connectivity issue to Azure OpenAI")
        elif "not found" in error_str or "404" in error_str:
            print("🔍 Diagnosis: Deployment 'gpt-4o' not found or incorrect endpoint")
        else:
            print(f"🔍 Diagnosis: Unknown error - {str(e)}")
        
        return False

if __name__ == "__main__":
    print("🚀 IRENO Azure OpenAI Connection Test")
    print("=" * 50)
    
    success = test_azure_openai_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Connection test PASSED - Azure OpenAI is working correctly")
        print("💡 The issue might be in the agent execution or tool calling")
    else:
        print("❌ Connection test FAILED - Please check your Azure OpenAI setup")
        print("💡 Contact your mentor for updated API credentials")
    print("=" * 50)
