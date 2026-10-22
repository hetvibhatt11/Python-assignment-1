import os
import re
import sys
import pickle
import zipfile

def tokenize(line):
    """
    Converts a log line into normalized tokens.

    Normalization:
    - Converts text to lowercase.
    - Keeps letters and numbers.
    - Removes punctuation.
    """

    return re.findall(r"[a-zA-Z0-9]+", line.lower())

def build_index(folder_path):
    """
    Scans all text files in the folder and creates
    an inverted index.

    Index format:

    {
        "server": [
            ("app.log", 1),
            ("system.log", 5)
        ]
    }
    """

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    index = {}

    total_files = 0
    total_lines = 0

    # Scan files in sorted order for consistent output
    file_names = sorted(os.listdir(folder_path))

    for file_name in file_names:

        file_path = os.path.join(
            folder_path,
            file_name
        )

        # Only process regular .txt log files
        if not os.path.isfile(file_path):
            continue

        # Process text/log files
        if not file_name.lower().endswith(
            (".txt", ".log")
        ):
            continue

        total_files += 1

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):

                    total_lines += 1

                    tokens = tokenize(line)

                    # Use a set so the same token appearing
                    # multiple times on one line is stored
                    # only once for that file:line location.
                    unique_tokens = set(tokens)

                    for token in unique_tokens:

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (file_name, line_number)
                        )

        except OSError as error:

            print(
                f"WARNING: Could not read {file_name}: {error}"
            )

    # Sort postings for predictable search output
    for token in index:
        index[token].sort(
            key=lambda item: (
                item[0],
                item[1]
            )
        )

    return (
        index,
        total_files,
        total_lines
    )

def save_pickle(
    index,
    pickle_path,
    total_files,
    total_lines
):
    """
    Saves the index and metadata using pickle.
    """

    data = {
        "index": index,
        "total_files": total_files,
        "total_lines": total_lines,
        "unique_tokens": len(index)
    }

    with open(
        pickle_path,
        "wb"
    ) as file:

        pickle.dump(
            data,
            file,
            protocol=pickle.HIGHEST_PROTOCOL
        )
def create_zip(
    folder_path,
    pickle_path,
    zip_path
):
    """
    Compresses the original log files and the pickle
    index into a ZIP archive.
    """

    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        # Add original log files
        for file_name in sorted(
            os.listdir(folder_path)
        ):

            file_path = os.path.join(
                folder_path,
                file_name
            )

            if not os.path.isfile(file_path):
                continue

            if not file_name.lower().endswith(
                (".txt", ".log")
            ):
                continue

            archive.write(
                file_path,
                arcname=os.path.join(
                    "logs",
                    file_name
                )
            )

        # Add pickle index
        archive.write(
            pickle_path,
            arcname=os.path.basename(
                pickle_path
            )
        )

def build_mode(
    folder_path,
    zip_path
):
    """
    Builds the index, saves it as a pickle file,
    and creates a ZIP archive.
    """

    (
        index,
        total_files,
        total_lines
    ) = build_index(folder_path)

    # Store pickle next to the ZIP archive.
    # Example:
    # archive.zip -> log_index.pkl
    base_directory = os.path.dirname(
        os.path.abspath(zip_path)
    )

    if not base_directory:
        base_directory = "."

    pickle_path = os.path.join(
        base_directory,
        "log_index.pkl"
    )

    save_pickle(
        index,
        pickle_path,
        total_files,
        total_lines
    )

    create_zip(
        folder_path,
        pickle_path,
        zip_path
    )

    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")

    print(f"PICKLE {pickle_path}")
    print(f"ZIP {zip_path}")

def load_index(pickle_path):
    """
    Loads the inverted index from the pickle file.
    """

    if not os.path.isfile(pickle_path):
        raise FileNotFoundError(
            f"Pickle file not found: {pickle_path}"
        )

    with open(
        pickle_path,
        "rb"
    ) as file:

        data = pickle.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "Invalid pickle index format."
        )

    if "index" not in data:
        raise ValueError(
            "Pickle file does not contain an index."
        )

    return data["index"]

def search_mode(
    pickle_path,
    queries
):
    """
    Searches the pickle index for the given tokens.
    """

    index = load_index(pickle_path)

    for query in queries:

        # Normalize the query exactly like log tokens
        normalized_query = query.lower()

        # Search only normalized tokens
        if normalized_query in index:

            matches = index[normalized_query]

            for file_name, line_number in matches:

                print(
                    f"{normalized_query}: "
                    f"{file_name}:{line_number}"
                )

        else:

            print(
                f"{normalized_query}: NOT FOUND"
            )

def main():

    try:

        if len(sys.argv) < 2:
            print(
                "Usage:"
            )
            print(
                "BUILD <folder> <zip_name>"
            )
            print(
                "SEARCH <pickle_path> <q> <token1> ..."
            )
            return

        mode = sys.argv[1].upper()

        if mode == "BUILD":

            if len(sys.argv) != 4:
                raise ValueError(
                    "BUILD format: "
                    "BUILD <folder> <zip_name>"
                )

            folder_path = sys.argv[2]
            zip_path = sys.argv[3]

            build_mode(
                folder_path,
                zip_path
            )

        elif mode == "SEARCH":

            if len(sys.argv) < 4:
                raise ValueError(
                    "SEARCH format: "
                    "SEARCH <pickle_path> <q> <token1> ..."
                )

            pickle_path = sys.argv[2]

            q = int(sys.argv[3])

            if q < 1:
                raise ValueError(
                    "Number of queries must be positive."
                )

            if len(sys.argv) != 4 + q:
                raise ValueError(
                    f"Expected {q} query tokens."
                )

            queries = sys.argv[4:]

            search_mode(
                pickle_path,
                queries
            )

        else:

            raise ValueError(
                "Mode must be BUILD or SEARCH."
            )

    except (
        FileNotFoundError,
        ValueError,
        pickle.UnpicklingError,
        OSError
    ) as error:

        print(f"ERROR: {error}")

if __name__ == "__main__":
    main()
