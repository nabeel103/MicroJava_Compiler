import threading
import time
import queue
from Tokenizer import get_next_token
from RbTree import main_function
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        result = []
        operators = {'+', '-', '*', '/', '%', '(', ')', '[', ']', '{', '}', '=', ';', ',', '>', '<'}
        two_char_operators = {'==', '!=', '>=', '<='}

        while self.current_position < len(self.input_text):
            char = self.input_text[self.current_position]

            if char.isalpha():
                result.append(self.tokenize_identifier())
            elif char.isdigit():
                result.append(self.tokenize_number())
            elif char == "'":
                result.append(self.tokenize_char_const())
            elif char == '/':
                if self.current_position + 1 < len(self.input_text) and self.input_text[self.current_position + 1] == '/':
                    result.append(self.tokenize_comment())
                else:
                    result.append(char)
                    self.current_position += 1
            elif char in operators:
                if self.current_position + 1 < len(self.input_text) and char + self.input_text[self.current_position + 1] in two_char_operators:
                    result.append(char + self.input_text[self.current_position + 1])
                    self.current_position += 2
                else:
                    result.append(char)
                    self.current_position += 1
            elif char.isspace():
                self.current_position += 1
                continue
            else:
                result.append(char)
                self.current_position += 1

        return result
    def tokenize_identifier(self):
        identifier = ""
        while self.current_position < len(self.input_text) and (self.input_text[self.current_position].isalnum() or self.input_text[self.current_position] == '_'):
            identifier += self.input_text[self.current_position]
            self.current_position += 1

        if identifier.lower() in {'program', 'class', 'if', 'else', 'while', 'read', 'print', 'return', 'void', 'final', 'new'}:
            return identifier
        else:
            return identifier

    def tokenize_number(self):
        number = ""
        while self.current_position < len(self.input_text) and self.input_text[self.current_position].isdigit():
            number += self.input_text[self.current_position]
            self.current_position += 1

        return number

    def tokenize_char_const(self):
        char_const = "'"
        self.current_position += 1  # Skip the opening single quote
        while self.current_position < len(self.input_text) and self.input_text[self.current_position] not in {"'", '\r', '\n'}:
            char_const += self.input_text[self.current_position]
            self.current_position += 1
        char_const += "'"  # Include the closing single quote

        return char_const

    def tokenize_comment(self):
        comment = "//"
        self.current_position += 2  # Skip the two slashes
        while self.current_position < len(self.input_text) and self.input_text[self.current_position] not in {'\r', '\n'}:
            comment += self.input_text[self.current_position]
            self.current_position += 1

        return comment

# Define queue
shared_buffer = queue.Queue()
processing_complete = threading.Event()

# Read file by setting the buffer size to 100
def readingFileContent(path, bufferSize):
    with open(file=path, mode="rb") as f:
        while True:
            content = f.read(bufferSize)
            if not content:
                break
            # Decode the bytes-like string into a regular string using the decode method with 'utf-8' encoding
            decoded_string = content.decode('utf-8')
            # Store the regular string in shared_buffer (queue in our case)
            shared_buffer.put(decoded_string)
            time.sleep(1)
    # Empty the shared buffer (queue)
    shared_buffer.put(None)

# Get string stored in the queue to split words by removing space or other characters such as \n
def processData():
    list = []
    global tokens
    while True:
        # Start processing
        # shared_buffer (queue) serves as an intermediate storage for the content read from the file.
        # It allows the reading and processing of data here
        getString = shared_buffer.get()
        # If the shared buffer contains None, it'll break the loop and stop the overall program execution
        if getString is None:
            break
        # Tokenize the string using the Lexer
        lexer = Lexer(getString)
        tokens = lexer.tokenize()
        list = list + tokens
        time.sleep(1)
    processing_complete.set()
    
    tokens= get_next_token(list)
    for token in tokens:
        # if token.value = list:
            print(token)
    return tokens

    

# main block

# Enter the file path
filePath = input("Enter the file path: ")
# Enter the required buffer size
buffer_size = int(input("Enter the required buffer size: "))
reader_thread = threading.Thread(target=readingFileContent, args=(filePath, buffer_size))
processor_thread = threading.Thread(target=processData)
reader_thread.start()
processor_thread.start()

# wait for the thread to finish
reader_thread.join()
processor_thread.join()

# Call RB Tree Function To Construct a red black tree.
main_function(tokens)
