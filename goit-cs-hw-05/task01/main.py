import asyncio
from pathlib import Path
import aiofiles
import logging

# логування
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source: Path, destination: Path):
    try:
        for entry in source.iterdir():
            if entry.is_dir():  
                await read_folder(entry, destination)
            elif entry.is_file():   
                await copy_file(entry, destination)
    except Exception as e:
        logging.error(f"Помилка при читанні папки {source}: {e}")

async def copy_file(file_path: Path, destination: Path):
    try:
        file_extension = file_path.suffix[1:] or "unknown"
        target_folder = destination / file_extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file_path.name
        
        async with aiofiles.open(file_path, "rb") as target_folder:
            s_f = await target_folder.read()

        async with aiofiles.open(target_file, "wb") as destiantion_folder:
            await destiantion_folder.write(s_f)

        logging.info(f'Скопійовано {file_path} в {target_file}')
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")

if __name__ == "__main__":

    source_path = Path(input("Input path to target dir --> "))

    destination_path = Path(input("input path where to save the sorted data --> "))

    if not source_path.exists() or not source_path.is_dir():
        logging.error(f"Вихідна папка {source_path} не існує або не є директорією.")
        exit(1)

    if not destination_path.exists():
        destination_path.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_path, destination_path))
