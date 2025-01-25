import os
import subprocess


def create_transparent_video(frame_dir, output_video, frame_rate=20):
    """
    Erstellt ein Video mit transparentem Hintergrund aus PNG-Frames.

    :param frame_dir: Verzeichnis, in dem die Frames gespeichert sind
    :param output_video: Dateiname des Ausgabevideos (inkl. .webm)
    :param frame_rate: Frame-Rate des Videos (Standard: 30 fps)
    """
    # Überprüfen, ob das Verzeichnis existiert
    if not os.path.exists(frame_dir):
        raise FileNotFoundError(f"Das Verzeichnis {frame_dir} wurde nicht gefunden.")

    # FFmpeg-Befehl zum Erstellen eines transparenten WebM-Videos
    ffmpeg_cmd = [
        "ffmpeg",
        "-framerate", str(frame_rate),
        "-i", os.path.join(frame_dir, "Image%04d.png"),  # Frames müssen nummeriert sein
        "-c:v", "libvpx-vp9",  # VP9-Codec für Transparenz
        "-pix_fmt", "yuva420p",  # Transparenzformat
        "-y",  # Überschreibe existierende Datei
        os.path.join(frame_dir, output_video)  # Speichere das Video im selben Verzeichnis
    ]

    # FFmpeg ausführen
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Das Video wurde erfolgreich erstellt: {os.path.join(frame_dir, output_video)}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Erstellen des Videos: {e}")


# Beispielaufruf
if __name__ == "__main__":
    # Verzeichnis mit Frames und Zielvideo definieren
    frame_directory = r"C:\Users\padin\Documents\Blender render\frames"  # Pfad zu deinen Frames

    output_video_file = "Planty animation.webm"

    # Video erstellen
    create_transparent_video(frame_directory, output_video_file)

    # Video erstellen
    create_transparent_video(frame_directory, output_video_file)
