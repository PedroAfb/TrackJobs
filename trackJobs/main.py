from rich.console import Console
from rich.prompt import IntPrompt
from rich.panel import Panel

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2 
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4

console = Console()

def main():
    console.print(Panel("[bold magenta]TrackJobs - Gerenciador de Candidaturas[/bold magenta]", expand=False))

    msg_prompt = (
        "[bold cyan]Escolha uma opção abaixo:[/bold cyan]\n\n"
        "[green]1[/green] - Cadastrar Candidatura\n"
        "[green]2[/green] - Editar Status da Candidatura\n"
        "[green]3[/green] - Editar Candidatura\n"
        "[green]4[/green] - Remover Candidatura\n"
    )
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