import locale
import os
import sqlite3
import subprocess

class stats:
    def get_stats(self, PATH_LIBRARY_DB, VERBOSE = False):
        if(os.path.exists(PATH_LIBRARY_DB) == False):
            if(os.path.exists(os.path.basename(PATH_LIBRARY_DB))):
                PATH_LIBRARY_DB = os.path.basename(PATH_LIBRARY_DB)
            else:
                print("The path to your libraries database cannot be found.")
                return 0

        conn = sqlite3.connect(PATH_LIBRARY_DB)
        db = conn.cursor()

        print("Library Overview")
        print("----------------")
        db.execute("SELECT Library, Items \
            FROM ( SELECT name AS Library, \
            COUNT(duration) AS Items \
            FROM media_items m  \
            LEFT JOIN library_sections l ON l.id = m.library_section_id  \
            WHERE library_section_id > 0 GROUP BY name );")
        for i in db.fetchall():
            if(str(i[0]) == "Movies"):
                print(str(i[0]) + ": " + str(locale.format_string("%d", i[1], grouping=True)) + " movies")
            elif(str(i[0]) == "TV Shows"):
                print(str(i[0]) + ": " + str(locale.format_string("%d", i[1], grouping=True)) + " episodes")
            elif(str(i[0]) == "Anime"):
                print(str(i[0]) + ": " + str(locale.format_string("%d", i[1], grouping=True)) + " episodes")
            elif(str(i[0]) == "Music"):
                print(str(i[0]) + ": " + str(locale.format_string("%d", i[1], grouping=True)) + " tracks")
            else:
                print(str(i[0]) + ": " + str(locale.format_string("%d", i[1], grouping=True)) + " items")
        
        subtitles = 0
        for root, dirs, files in os.walk("/mnt/media"):
            for file in files:
                if(file.endswith(".srt")): subtitles += 1

        subtitles = str(locale.format_string("%d", subtitles, grouping=True))
        print(f"Subtitles: {subtitles} subtitles\n")

        print("Runtime Statistics")
        print("------------------")
        db.execute("SELECT Library, Minutes, Hours, Days \
            FROM ( SELECT name AS Library, \
            SUM(duration)/1000/60 AS Minutes, \
            SUM(duration)/1000/60/60 AS Hours, \
            SUM(duration)/1000/60/60/24 AS Days \
            FROM media_items m \
            LEFT JOIN library_sections l ON l.id = m.library_section_id \
            WHERE library_section_id > 0 GROUP BY name );")
        for i in db.fetchall():
            print("[" + str(i[0]) + "]\n    Minutes: " + str(locale.format_string("%d", i[1], grouping=True)) + "\n    Hours: " + str(locale.format_string("%d", i[2], grouping=True)) + "\n    Days: " + str(locale.format_string("%d", i[3], grouping=True)) + "\n")
        
        print("Library Statistics")
        print("------------------")

        db.execute("SELECT COUNT(*) FROM media_items")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " files in your library.")

        db.execute("SELECT COUNT(*) FROM media_parts WHERE extra_data NOT LIKE '%intros=%' AND file != '';")
        missing_intro_detection = db.fetchone()[0]
        print(str(missing_intro_detection) + " files are missing intro detection markers.")

        db.execute("SELECT COUNT(*) FROM media_parts WHERE extra_data NOT LIKE '%credits=%' AND file != '';")
        missing_intro_detection = db.fetchone()[0]
        print(str(missing_intro_detection) + " files are missing credit detection markers.")

        db.execute("SELECT COUNT(*) FROM media_items WHERE bitrate IS NULL")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " files missing bitrate analyzation info.")

        db.execute("SELECT COUNT(*) FROM media_items WHERE media_analysis_version != 6;")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " files missing analysation info.")

        db.execute("SELECT COUNT(*) FROM media_parts WHERE extra_data NOT LIKE '%deepAnalysisVersion=6%' AND file != '';")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " files missing deep analysation info.")

        db.execute("SELECT COUNT(*) FROM media_parts WHERE deleted_at IS NOT NULL")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " media_parts marked as deleted.")

        db.execute("SELECT COUNT(*) FROM metadata_items WHERE deleted_at IS NOT NULL")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " metadata_items marked as deleted.")

        db.execute("SELECT COUNT(*) FROM directories WHERE deleted_at IS NOT NULL")
        print(str(locale.format_string("%d", db.fetchone()[0], grouping=True)) + " directories marked as deleted.")

        if(VERBOSE):
            print("Report for Missing Deep Analysation Info:")
            print("-----------------------------------------")
            db.execute("SELECT meta.id,title FROM metadata_items meta JOIN media_items media ON media.metadata_item_id = meta.id JOIN media_parts part ON part.media_item_id = media.id WHERE part.extra_data NOT LIKE '%deepAnalysisVersion=6%' AND meta.metadata_type IN (1, 4, 12) AND part.file != '';")
            for media in db.fetchall():
                print(str(media[0]) + ":" + media[1])
            
        conn.close()
        return 1

class repair:
    def file_permissions(self):
        libraries = [
            "/mnt/media/movies",
            "/mnt/media/tv-series",
            "/mnt/media/anime",
            "/mnt/media/music",
            "/mnt/media/books",
        ]
        for library in libraries:
            if(os.path.exists(library)):
                command = "find " + library + " -type d -exec chmod 775 {} \;"
                subprocess.call(command, shell=True)

                command = "find " + library + " -type f -exec chmod 664 {} \;"
                subprocess.call(command, shell=True)
            
            else:
                print("The library: " + library + " doesn't exist on the file system.")