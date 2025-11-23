import mutagen
import re
import os


def search_music(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if mutagen.File(file_path) is not None:
                    change_artist(file_path)
            except Exception:
                continue


def change_artist(file_path: str):
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} isn't a file")
        return

    file = mutagen.File(file_path)
    pattern = r"\sft.?\s|\sfeat.?\s|\sfeaturing\s|\s?;\s?|\s?&\s?|\sand\s"

    print(f"{os.path.basename(file_path)}: {file["artist"]} ->", end=" ")

    artists = []
    for artist in file["artist"]:
        artists.extend(re.split(pattern, artist))

    print(artists)
    file["artist"] = artists
    file.save()


if __name__ == "__main__":
    path = os.path.abspath(input("Folder with music: "))
    search_music(path)
