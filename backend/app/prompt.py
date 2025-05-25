def print_prompt():
    with open('./app/prompt.md', 'r', encoding='utf-8') as f:
        return f.read().strip()

print(print_prompt())