#!/usr/bin/env python3
"""
IRENO Smart Assistant - Log Monitor
Real-time log monitoring script to track application events and errors
"""

import time
import os
import sys
from datetime import datetime

def monitor_logs(log_file="ireno_assistant.log"):
    """Monitor log file for new entries in real-time"""
    
    print("=" * 80)
    print("🔍 IRENO Smart Assistant - Real-time Log Monitor")
    print("=" * 80)
    print(f"📁 Monitoring log file: {log_file}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📋 Press Ctrl+C to stop monitoring")
    print("=" * 80)
    
    # Check if log file exists
    if not os.path.exists(log_file):
        print(f"⚠️  Log file '{log_file}' does not exist yet.")
        print("💡 It will be created when the Flask app starts.")
        print("🔄 Waiting for log file to be created...")
        
        # Wait for log file to be created
        while not os.path.exists(log_file):
            time.sleep(1)
            print(".", end="", flush=True)
        print("\n✅ Log file created! Starting to monitor...")
    
    # Start monitoring
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            # Go to end of file
            file.seek(0, 2)
            
            while True:
                line = file.readline()
                if line:
                    # Format and display the log line
                    formatted_line = format_log_line(line.strip())
                    print(formatted_line)
                else:
                    time.sleep(0.1)  # Short sleep to prevent excessive CPU usage
                    
    except KeyboardInterrupt:
        print("\n" + "=" * 80)
        print("🛑 Log monitoring stopped by user")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Error monitoring logs: {str(e)}")

def format_log_line(line):
    """Format log lines with colors and emojis for better readability"""
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Color codes (if terminal supports them)
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Check for different log levels and add appropriate formatting
    if "ERROR" in line:
        return f"{RED}🚨 [{timestamp}] {line}{RESET}"
    elif "WARNING" in line or "WARN" in line:
        return f"{YELLOW}⚠️  [{timestamp}] {line}{RESET}"
    elif "INFO" in line:
        if "✅" in line or "success" in line.lower():
            return f"{GREEN}✅ [{timestamp}] {line}{RESET}"
        elif "🤖" in line or "Processing" in line:
            return f"{BLUE}🤖 [{timestamp}] {line}{RESET}"
        elif "📡" in line or "API Call" in line:
            return f"{CYAN}📡 [{timestamp}] {line}{RESET}"
        elif "🌐" in line or "request" in line.lower():
            return f"{MAGENTA}🌐 [{timestamp}] {line}{RESET}"
        else:
            return f"{WHITE}ℹ️  [{timestamp}] {line}{RESET}"
    elif "DEBUG" in line:
        return f"{CYAN}🔧 [{timestamp}] {line}{RESET}"
    else:
        return f"{WHITE}📝 [{timestamp}] {line}{RESET}"

def show_recent_logs(log_file="ireno_assistant.log", lines=50):
    """Show the last N lines from the log file"""
    
    print("=" * 80)
    print(f"📜 IRENO Smart Assistant - Last {lines} Log Entries")
    print("=" * 80)
    
    if not os.path.exists(log_file):
        print(f"⚠️  Log file '{log_file}' does not exist yet.")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            all_lines = file.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            for line in recent_lines:
                formatted_line = format_log_line(line.strip())
                print(formatted_line)
                
    except Exception as e:
        print(f"❌ Error reading log file: {str(e)}")

def main():
    """Main function to handle command line arguments"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "recent":
            lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            show_recent_logs(lines=lines)
        elif command == "help":
            print("IRENO Smart Assistant - Log Monitor")
            print("Usage:")
            print("  python monitor_logs.py          - Start real-time monitoring")
            print("  python monitor_logs.py recent   - Show last 50 log entries")
            print("  python monitor_logs.py recent N - Show last N log entries")
            print("  python monitor_logs.py help     - Show this help message")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python monitor_logs.py help' for usage information")
    else:
        # Default: start real-time monitoring
        monitor_logs()

if __name__ == "__main__":
    main()
