
def get_message_template(template_file: str) -> str:

    with open(template_file, 'r') as f:
        template = f.read()

    return template


def parse_template(template: str, manifest_entry: dict) -> str:
    message = template

    open_brace_index = None

    i = 0
    while i < len(message):
        if message[i] == '{':
            open_brace_index = i
            close_brace_index = i
        elif message[i] == '}':
            close_brace_index = i
            key = message[open_brace_index+1:close_brace_index]
            top = message[0:open_brace_index]
            bottom = message[close_brace_index+1:]
            message = top + manifest_entry[key] + bottom
            i = 0

        i += 1

    return message
