import os
import json

class FeedbackStack:
    def __init__(self):
        self.stack = []
    def push(self, feedback):
        self.stack.append(feedback)
    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()
    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]
    def is_empty(self):
        return len(self.stack) == 0

class FeedbackList:
    def __init__(self, file_path):
        self.file_path = file_path
        self.feedback_stack = FeedbackStack()
        self.load_feedback_data()

    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def load_feedback_data(self):
        self.ensure_file_exists()
        with open(self.file_path, 'r') as file:
            try:
                data = json.load(file)
                for feedback in reversed(data):
                    self.feedback_stack.push(feedback)
            except json.JSONDecodeError:
                pass  # Empty or invalid JSON file

    def save_feedback_data(self):
        feedback_data = self.get_all_feedback()
        with open(self.file_path, 'w') as file:
            json.dump(feedback_data, file, indent=4)
     
    def add_feedback(self, feedback):
        # Check if feedback already exists
        if feedback not in self.feedback_stack.stack:
            self.feedback_stack.push(feedback)
            self.save_feedback_data()

    def get_all_feedback(self):
        return list(reversed(self.feedback_stack.stack))
