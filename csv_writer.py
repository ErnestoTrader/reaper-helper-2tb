import csv
import os

def write_metadata_to_csv(metadata_list, output_file):
    """
    Writes a list of metadata dictionaries to a CSV file.

    Args:
        metadata_list (list): A list of dictionaries containing metadata.
        output_file (str): The path to the output CSV file.

    Raises:
        ValueError: If the metadata_list is empty.
        IOError: If there is an issue with writing to the file.
    """
    if not metadata_list:
        raise ValueError("Metadata list is empty. Nothing to write to CSV.")

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = metadata_list[0].keys()  # Get the keys from the first dict
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header
            for metadata in metadata_list:
                writer.writerow(metadata)  # Write each metadata dict
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")
        raise

# TODO: Add more features like appending to existing files or better error logging
# TODO: Consider supporting more output formats if needed in the future
# TODO: Implement unit tests to ensure functionality

# Example usage (uncomment to use):
# metadata = [
#     {"track_name": "Guitar", "duration": 120, "sample_rate": 44100},
#     {"track_name": "Drums", "duration": 150, "sample_rate": 44100},
# ]
# write_metadata_to_csv(metadata, 'output/metadata.csv')
