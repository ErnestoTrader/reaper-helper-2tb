import os
import csv
import mutagen
from mutagen.mp3 import MP3
from mutagen.wavpack import WavPack
from mutagen.flac import FLAC

class MetadataExtractor:
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.audio_files = []

    def find_audio_files(self):
        """Recursively find audio files in the project directory."""
        for root, _, files in os.walk(self.project_directory):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.flac', '.wvp')):
                    self.audio_files.append(os.path.join(root, file))
        if not self.audio_files:
            raise FileNotFoundError("No audio files found in the specified directory.")

    def extract_metadata(self):
        """Extract metadata from the audio files."""
        metadata_list = []
        for audio_file in self.audio_files:
            try:
                audio = self._load_audio_file(audio_file)
                metadata = self._get_audio_metadata(audio, audio_file)
                metadata_list.append(metadata)
            except Exception as e:
                print(f"Error extracting metadata from {audio_file}: {e}")
        return metadata_list

    def _load_audio_file(self, file_path):
        """Load an audio file based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.mp3':
            return MP3(file_path)
        elif ext == '.wav':
            return mutagen.File(file_path)
        elif ext == '.flac':
            return FLAC(file_path)
        elif ext == '.wvp':
            return WavPack(file_path)
        else:
            raise ValueError(f"Unsupported audio format: {ext}")

    def _get_audio_metadata(self, audio, file_path):
        """Retrieve relevant metadata from the audio file."""
        ext = os.path.splitext(file_path)[1].lower()
        
        # Initialize default values
        title = artist = album = 'Unknown'
        duration = 'Unknown'
        
        # Get duration
        if hasattr(audio, 'info') and audio.info:
            duration = audio.info.length
        
        # Get tags based on format
        if audio and hasattr(audio, 'tags') and audio.tags:
            if ext == '.mp3':
                # ID3 tags for MP3
                title = str(audio.tags.get('TIT2', '')) if audio.tags.get('TIT2') else 'Unknown'
                artist = str(audio.tags.get('TPE1', '')) if audio.tags.get('TPE1') else 'Unknown'
                album = str(audio.tags.get('TALB', '')) if audio.tags.get('TALB') else 'Unknown'
            elif ext == '.flac':
                # Vorbis comments for FLAC
                title_list = audio.tags.get('TITLE', [])
                title = title_list[0] if title_list else 'Unknown'
                artist_list = audio.tags.get('ARTIST', [])
                artist = artist_list[0] if artist_list else 'Unknown'
                album_list = audio.tags.get('ALBUM', [])
                album = album_list[0] if album_list else 'Unknown'
            elif ext == '.wvp':
                # WavPack uses APE tags
                title_tag = audio.tags.get('Title')
                title = str(title_tag[0] if isinstance(title_tag, list) and title_tag else title_tag) if title_tag else 'Unknown'
                artist_tag = audio.tags.get('Artist')
                artist = str(artist_tag[0] if isinstance(artist_tag, list) and artist_tag else artist_tag) if artist_tag else 'Unknown'
                album_tag = audio.tags.get('Album')
                album = str(album_tag[0] if isinstance(album_tag, list) and album_tag else album_tag) if album_tag else 'Unknown'
            else:
                # Generic handling for WAV and other formats
                # Try common tag names
                for title_key in ['TIT2', 'TITLE', 'Title']:
                    if title_key in audio.tags:
                        tag_val = audio.tags[title_key]
                        title = str(tag_val[0] if isinstance(tag_val, list) and tag_val else tag_val)
                        break
                for artist_key in ['TPE1', 'ARTIST', 'Artist']:
                    if artist_key in audio.tags:
                        tag_val = audio.tags[artist_key]
                        artist = str(tag_val[0] if isinstance(tag_val, list) and tag_val else tag_val)
                        break
                for album_key in ['TALB', 'ALBUM', 'Album']:
                    if album_key in audio.tags:
                        tag_val = audio.tags[album_key]
                        album = str(tag_val[0] if isinstance(tag_val, list) and tag_val else tag_val)
                        break
        
        return {
            'title': title,
            'artist': artist,
            'album': album,
            'duration': duration
        }

def save_to_csv(metadata_list, output_file):
    """Save the extracted metadata to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'artist', 'album', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)

def main():
    project_directory = input("Enter the path to the Reaper project directory: ").strip()
    output_file = input("Enter the path for the output CSV file: ").strip()

    try:
        extractor = MetadataExtractor(project_directory)
        extractor.find_audio_files()
        metadata_list = extractor.extract_metadata()
        save_to_csv(metadata_list, output_file)
        print(f"Metadata extracted and saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
