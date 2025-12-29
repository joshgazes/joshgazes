import os
import shutil
from pathlib import Path
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

# Define folder mappings
DIRECTORY_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Video": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".rar", ".gz"],
}

@app.command()
def organize(target_path: str = typer.Argument(..., help="The folder path to organize")):
    """
    Organizes files in the specified directory based on their file extensions.
    """
    path = Path(target_path)

    if not path.is_dir():
        console.print(f"[bold red]Error:[/bold red] {target_path} is not a valid directory.")
        raise typer.Exit()

    with console.status("[bold green]Organizing files...") as status:
        for item in path.iterdir():
            # Skip directories
            if item.is_dir():
                continue

            # Find the category for the file extension
            moved = False
            for category, extensions in DIRECTORY_MAP.items():
                if item.suffix.lower() in extensions:
                    dest_folder = path / category
                    dest_folder.mkdir(exist_ok=True)
                    
                    shutil.move(str(item), str(dest_folder / item.name))
                    console.print(f"Moved [cyan]{item.name}[/cyan] to [yellow]{category}/[/yellow]")
                    moved = True
                    break
            
            # Optional: Move unknown files to an 'Others' folder
            if not moved:
                others_folder = path / "Others"
                others_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(others_folder / item.name))

    console.print("\n[bold green]✔ Organization complete![/bold green]")

if __name__ == "__main__":
    app()