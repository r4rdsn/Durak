WARNING_HEADER = '[\033[1m\033[93mWARNING\033[0m]'


def warning_message(message_text):
    print('{header} {text}'.format(header=WARNING_HEADER, text=message_text))
