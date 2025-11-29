import mutagen
import mutagen.easymp4
import re
import os


def search_music(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if mutagen.File(file_path, easy=True) is not None:
                    change_artist(file_path)
            except Exception:
                continue


def change_artist(file_path: str):
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} isn't a file")
        return

    file = mutagen.File(file_path, easy=True)
    pattern = r"\sft.?\s|\sfeat.?\s|\sfeaturing\s|\s?;\s?|\s?&\s?|\sand\s"

    try:
        artists_tag = file.get("artist")
        if not artists_tag:
            return

        print(f"{os.path.basename(file_path)}: {artists_tag} ->", end=" ")

        artists = []
        for artist in artists_tag:
            artists.extend(re.split(pattern, artist))

        print(artists)

        if isinstance(file, mutagen.easymp4.EasyMP4):
            file["artist"] = ["/".join(artists)]
        else:
            file["artist"] = artists

        file.save()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    try:
        path = os.path.abspath(input("Folder with music: "))
        search_music(path)
    except KeyboardInterrupt:
        print("Exiting...")
