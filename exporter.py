import os
import sqlite3

USER_HOME_DIR = os.environ["HOME"]
BOOK_DOCS_DIR = f"{USER_HOME_DIR}/Library/Containers/com.apple.iBooksX/Data/Documents/"


def get_books():
    books_db_dir = f"{BOOK_DOCS_DIR}/BKLibrary/"
    book_db_file = [f for f in os.listdir(books_db_dir)
                    if f.startswith("BKLibrary")
                    and f.endswith("sqlite")][0]
    with sqlite3.connect(books_db_dir + book_db_file) as conn:
        sql = '''
        select ZASSETID as book_id, ZTITLE as title, ZAUTHOR as author
        from zbklibraryasset
        where title is not null
        '''
        cursor = conn.cursor()
        books = cursor.execute(sql).fetchall()
        return books
    return None

def get_notes():
    notes_db_dir = f"{BOOK_DOCS_DIR}/AEAnnotation/"
    notes_db_file = [f for f in os.listdir(notes_db_dir)
                     if f.startswith("AEAnnotation")
                     and f.endswith("sqlite")][0]
    with sqlite3.connect(notes_db_dir + notes_db_file) as conn:
        sql = '''
        select ZANNOTATIONASSETID as book_id, ZANNOTATIONSELECTEDTEXT
        from zaeannotation
        where ZANNOTATIONSELECTEDTEXT is not null
        '''
        cursor = conn.cursor()
        notes = cursor.execute(sql).fetchall()
        return notes
    return None
        


if __name__ == "__main__":
    books = get_books()
    notes = get_notes()
    book_ids = [book[0] for book in books]
    for idx, book_id in enumerate(book_ids):
        book_notes = [note[1] for note in notes if note[0]==book_id]
        if not book_notes:
            continue
        print(f"Book name: {books[idx][1]}")
        for i, note in enumerate(book_notes):
            print(note)
