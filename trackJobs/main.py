from rich.prompt import IntPrompt

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2 
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4
def main():
    msg_prompt = "1 - Cadastrar Candidatura\n"
    msg_prompt += "2 - Editar status da candidatura\n"
    msg_prompt += "3 - Editar candidatura\n"
    msg_prompt += "4 - Remover candidatura"
    code = IntPrompt.ask(msg_prompt, choices=['1', '2', '3', '4'])

    if code == CADASTRAR_CANDIDATURA:
        pass
    elif code == EDITAR_STATUS:
        pass
    elif code == EDITAR_CANDIDATURA:
        pass
    else:
        pass

main()