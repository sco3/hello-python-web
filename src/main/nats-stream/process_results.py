import re
import os
import sys


def main():
    # Collect command-line arguments (file paths)
    args = sys.argv[1:]

    if not args:
        print("Usage: python3 script.py <file1> <file2> ...", file=sys.stderr)
        return

    stat_re = re.compile(r"stats:\s*([\d,\.]+)\s+msgs")
    results = {}

    for file_path in args:
        if file_path.endswith(".rs"):
            continue

        # Get the size part from the file name (4th part split by ".")
        size_str = file_path.split(".")[3] if len(file_path.split(".")) > 3 else None
        if size_str:
            try:
                size = int(size_str)
            except ValueError:
                size = 0

            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}", file=sys.stderr)
                continue

            try:
                with open(file_path, "r") as file:
                    msg_per_sec = float("inf")
                    for line in file:
                        match = stat_re.search(line)
                        if match:
                            size_match = match.group(1)
                            stat = size_match.replace(",", "")
                            try:
                                stat = int(stat)
                            except ValueError:
                                stat = 0

                            if stat < msg_per_sec:
                                msg_per_sec = stat

                    if size > 0:
                        results[size] = msg_per_sec

            except Exception as err:
                print(f"Error opening file {file_path}: {err}", file=sys.stderr)

    # Output results
    print('"Message size","msg/s"')
    for key, value in sorted(results.items()):
        print(f"{key},{value}")


if __name__ == "__main__":
    main()
