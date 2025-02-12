import os

def parse_qa_file(file_path):
    """Reads the QA file and formats it into HTML."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return ""

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    html_content = ""
    question_count = 0
    code_block = ""  # To accumulate lines of code

    def is_code(line):
        """Detects code by checking if the line starts with exactly three tabs."""
        return line.startswith("\t\t\t")  # 3 tabs check

    for line in lines:
        stripped_line = line.rstrip()  # Remove trailing spaces and newlines
        if stripped_line and not stripped_line.startswith((" ", "\t")):  # Question
            if code_block:
                # Write the accumulated code block before the next question
                html_content += f"<pre><code>{code_block.strip()}</code></pre>\n"
                code_block = ""  # Reset the code block accumulator
            
            question_count += 1
            html_content += f"<h3><b>{question_count}. {stripped_line}</b></h3>\n"
        elif stripped_line:  # Answer
            if is_code(stripped_line):
                # Accumulate code lines
                code_block += f"{stripped_line.strip()}\n"
            else:
                if code_block:
                    # Write the accumulated code block before the next non-code answer
                    html_content += f"<pre><code>{code_block.strip()}</code></pre>\n"
                    code_block = ""  # Reset the code block accumulator
                html_content += f"<p>{stripped_line.strip()}</p>\n"

    # If there's any remaining code block after the last answer
    if code_block:
        html_content += f"<pre><code>{code_block.strip()}</code></pre>\n"

    return html_content

def generate_html(output_path, qa_content):
    """Creates an HTML file with the parsed content."""
    if not qa_content:
        print("No content to write.")
        return

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q&A Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Questions and Answers</h1>
    {qa_content}
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_template)
    print(f"HTML file '{output_path}' generated successfully.")

if __name__ == "__main__":
    qa_file = "questions.txt"  # Ensure this file exists
    output_html = "index.html"  # Change path if needed

    qa_content = parse_qa_file(qa_file)
    generate_html(output_html, qa_content)
