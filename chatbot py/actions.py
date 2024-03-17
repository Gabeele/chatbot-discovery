from utils import parse_date, parse_scale, normalize_yes_no, correct_spelling

def request_maintenance(client_socket):
    questions = {
        "emergency": "Is this an emergency issue? (Fire, flooding, etc.) Yes/No:",
        "issue_description": "What is the issue? Please explain in as much detail as possible:",
        "issue_duration": "How long has the issue been occurring? (e.g., '2 days')",
        "first_report": "Is this the first time you're reporting this issue? Yes/No:",
        "attempted_fix": "Have you attempted to fix the issue yourself? Yes/No:",
        "severity": "On a scale of 1-10, how would you rate the severity of the issue?",
        "urgency": "On a scale of 1-10, how urgent is this issue?",
        "photo_attachment": "Would you like to attach a photo of the issue? Yes/No: (Respond 'No' to skip)",
        "best_dates": "Please provide dates that are best for you to have someone come and fix the issue:",
        "best_times": "Please provide times that are best for you to have someone come and fix the issue: (e.g., '9am-12pm')",
        "prior_notice": "Do you require prior notice before someone comes to fix the issue? Yes/No:",
        "additional_details": "Is there anything else you would like to add? (Respond 'No' to skip):"
    }

    maintenance_request = {}

    for key, question in questions.items():
        client_socket.sendall(question.encode('utf-8'))
        answer = client_socket.recv(1024).decode('utf-8').strip()
        answer = correct_spelling(answer)
        
        if key in ["emergency", "first_report", "attempted_fix", "photo_attachment", "prior_notice"]:
            answer = normalize_yes_no(answer)
            while answer is None:
                client_socket.sendall("Please answer yes or no.".encode('utf-8'))
                answer = client_socket.recv(1024).decode('utf-8').strip().lower()
                answer = normalize_yes_no(correct_spelling(answer))
        
        elif key in ["severity", "urgency"]:
            answer = parse_scale(answer)
            while answer is None:
                client_socket.sendall("Invalid input, please enter a number between 1 and 10. ".encode('utf-8'))
                answer = parse_scale(client_socket.recv(1024).decode('utf-8').strip())

        elif key in ["issue_duration", "best_dates", "best_times"]:
            answer = parse_date(answer)
            while answer is None:
                client_socket.sendall("Invalid date format. Please use a valid date format. ".encode('utf-8'))
                answer = parse_date(client_socket.recv(1024).decode('utf-8').strip())
        
        if answer == 'bye':  # Allow the user to exit
            client_socket.sendall("Process canceled by user. Goodbye!".encode('utf-8'))
            return
        
        maintenance_request[key] = answer

    print("Maintenance request received with the following details:")
    for key, value in maintenance_request.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")

    client_socket.sendall("Thank you, your maintenance request has been submitted and will be processed shortly.".encode('utf-8'))
