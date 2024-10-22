import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class DataInputApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the layout and widgets
        self.initUI()

        # Create an empty DataFrame to store the data
        self.data_frame = pd.DataFrame(columns=['Input Data'])

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Create a QLabel for instructions
        self.label = QLabel("Enter some data:")
        layout.addWidget(self.label)

        # Create a QLineEdit for input
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        # Create a button to submit the input
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_button)

        # Set the layout for the main widget
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Data Input App")
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def handle_submit(self):
        # Get input from QLineEdit
        input_text = self.input_field.text()

        # Process the input (you can call any function here)
        processed_data = self.process_input(input_text)

        # Store the processed data in the DataFrame
        self.data_frame = self.data_frame.append({'Input Data': processed_data}, ignore_index=True)

        # Optionally clear the input field
        self.input_field.clear()

        # Print the DataFrame to console (for verification)
        print(self.data_frame)

    def process_input(self, input_text):
        # Example of processing (you can modify this as needed)
        return input_text.strip().upper()  # Example: strip whitespace and convert to uppercase

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataInputApp()
    sys.exit(app.exec_())
