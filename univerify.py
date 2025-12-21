"""
Univerify Application
=====================
Description: A simple document verification system using a splay tree
Author: Luqman Naim bin Mohd Esa
Email: luqmannaim@graduate.utm.my
"""

import os
import json
import argparse
from typing import List, Optional, Tuple
from trees import splay, avl, bst


class Document:
    """
    Document Metadata Class
    =======================
      - doc_id: unique document identifier used as the tree key.
      - applicant_id: short identifier for the applicant.
      - doc_type: file type string ("pdf", "doc").
      - status: verification state (new", "pending", "verified").
    """

    def __init__(self, doc_id: int, applicant_id: str, doc_type: str, status: str = "new"):
        """
        Initialize a document instance.
        """
        self.doc_id = doc_id
        self.applicant_id = applicant_id
        self.doc_type = doc_type
        self.status = status

    def to_dict(self) -> dict:
        """
        Convert document to dictionary for JSON serialization.
        """
        return {
            "doc_id": self.doc_id,
            "applicant_id": self.applicant_id,
            "doc_type": self.doc_type,
            "status": self.status,
        }

    def __repr__(self) -> str:
        """
        String representation of the document.
        """
        doc_repr = f"\n-------------------\n"
        doc_repr += f"Document ID: {self.doc_id}\n"
        doc_repr += f"Applicant ID: {self.applicant_id}\n"
        doc_repr += f"Document Type: {self.doc_type}\n"
        doc_repr += f"Document Status: {self.status}\n"
        doc_repr += f"-------------------\n"
        return doc_repr

class UniverifyApp:
    """
    Main Application Class
    ======================
      - List, Search, Insert, Update, Delete documents in the tree
    """

    def __init__(self, data_dir: str = None, tree_type: str = "splay"):
        """
        Initialize data directory and tree
        """

        # Set data directory (default: ./data)
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "data")

        # Initialize the chosen tree implementation
        tt = (tree_type or "splay").lower()
        if tt == "avl":
            self.tree = avl.Tree()   # Use AVL tree
        elif tt == "bst":
            self.tree = bst.Tree()   # Use BST tree
        else:
            self.tree = splay.Tree() # Use Splay tree

    def _file_path(self, doc_id: int) -> str:
        """
        Helper function to get JSON file path
        """
        return os.path.join(self.data_dir, f"{doc_id}.json")

    def _load_all(self) -> List[Tuple[int, str, str, str]]:
        """
        Helper function to return a sorted list of rows (doc_id, applicant_id, doc_type, status)
        """
        # Load all JSON files from data directory
        rows: List[Tuple[int, str, str, str]] = []
        if not os.path.isdir(self.data_dir):
            return rows
        
        # Iterate over files in data directory
        for name in sorted(os.listdir(self.data_dir)):
            if not name.lower().endswith('.json'):
                continue
            fp = os.path.join(self.data_dir, name)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    rows.append((int(obj.get('doc_id')), str(obj.get('applicant_id')), str(obj.get('doc_type')), str(obj.get('status'))))
            except Exception:
                # Skip malformed files instead of crashing the app
                continue
        return rows

    def list_documents(self) -> None:
        """
        Choice 1: List Documents
        Load documents from disk and print a small table of the document database.
        """

        # Load all documents from disk
        rows = self._load_all()

        # Print the available documents
        print("\nAvailable documents (from folder):")
        if not rows:
            print("No documents found!")
            return

        # Create headers
        headers = ["Doc ID", "Applicant ID", "Type", "Status"]

        # Calculate column widths
        cols = list(zip(*([headers] + [tuple(str(x) for x in r) for r in rows])))
        col_widths = [max(len(v) for v in c) for c in cols]

        # Create separators
        def sep():
            """Separator line for the table"""
            print("+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+")

        # Create rows
        def row(vals):
            """A single row of the table"""
            print("| " + " | ".join(v.ljust(w) for v, w in zip(vals, col_widths)) + " |")

        # Print the table
        sep()
        row(headers)
        sep()
        for r in rows:
            row([str(r[0]), str(r[1]), str(r[2]), str(r[3])])
        sep()

    def search_document(self, doc_id: int) -> Optional[Document]:
        """
        Choice 2: Search Document
        Search for a document in the in-memory tree and return it
        """
        return self.tree.search(doc_id)

    def insert_document(self, doc: Document) -> bool:
        """
        Choice 3: Insert Document
        Insert a new document into the tree and save to data folder.
        Returns True on success, False if a document with the same id exists.
        """
        ok = self.tree.insert(doc)
        if ok:
            try:
                # Get file path
                fp = self._file_path(doc.doc_id)

                # Write the JSON file to data folder
                with open(fp, 'w', encoding='utf-8') as f:
                    json.dump(doc.to_dict(), f, indent=2)
                print(f"Saved document to {self._file_path(doc.doc_id)}")
            except Exception as e:
                print(f"Failed to save file: {e}")
        return ok

    def update_document(self, doc_id: int, status: str) -> Optional[Document]:
        """
        Choice 4: Update Document
        Update a document's status and save the changes.
        """
        doc = self.tree.update(doc_id, status)
        if doc:
            try:
                # Get file path
                fp = self._file_path(doc.doc_id)

                # Write the JSON file to data folder
                with open(fp, 'w', encoding='utf-8') as f:
                    json.dump(doc.to_dict(), f, indent=2)
                print(f"Updated file {self._file_path(doc_id)}")
            except Exception as e:
                print(f"Failed to update file: {e}")
        return doc

    def delete_document(self, doc_id: int) -> bool:
        """
        Choice 5: Delete Document
        Delete a document from tree and remove the file.
        """
        ok = self.tree.delete(doc_id)
        if ok:
            try:
                # Get file path
                fp = self._file_path(doc_id)

                # Delete the file from disk
                if os.path.exists(fp):
                    os.remove(fp)
                print(f"Removed file {fp}")
            except Exception as e:
                print(f"Failed to remove file: {e}")
        return ok

    def run(self) -> None:
        """
        Run the user interface loop.
        """

        # Preload the tree from data folder
        os.makedirs(self.data_dir, exist_ok=True)
        rows = self._load_all()
        for r in rows:
            self.tree.insert(Document(*r))

        # List initial documents
        self.list_documents()

        # User interface
        while True:
            print("\nOptions: 1. List  2. Search  3. Insert  4. Update  5. Delete  6. Exit")
            choice = input("Enter choice: ")

            # List documents
            if choice == '1':
                self.list_documents()

            # Search document
            elif choice == '2':
                try:
                    did = int(input("Search Doc ID: "))
                    self.search_document(did)
                    self.tree.display_root()
                except ValueError:
                    print("Invalid ID.")

            # Insert document
            elif choice == '3':
                try:
                    did = int(input("Doc ID: "))
                    aid = input("Applicant ID: ")
                    dtype = input("Type (pdf/doc): ")
                    doc = Document(did, aid, dtype)
                    self.insert_document(doc)
                except ValueError:
                    print("Invalid input.")

            # Update document
            elif choice == '4':
                try:
                    did = int(input("Update Doc ID: "))
                    status = input("New Status (new/pending/verified): ")
                    self.update_document(did, status)
                except ValueError:
                    print("Invalid ID.")

            # Delete document
            elif choice == '5':
                try:
                    did = int(input("Delete Doc ID: "))
                    self.delete_document(did)
                except ValueError:
                    print("Invalid ID.")

            # Exit application
            elif choice == '6':
                print("Exiting.")
                break

            # Unknown choice
            else:
                print("Unknown choice.")

def main():
    """
    Main entry point for the Univerify application    
    """

    # Parse command line arguments
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", help="data directory to use")
    p.add_argument("--tree", choices=["splay", "avl"], default="splay", help="Which tree to use (splay or avl)")
    args = p.parse_args()

    # Initialize and run the application
    app = UniverifyApp(data_dir=args.data_dir, tree_type=args.tree)
    app.run()

if __name__ == "__main__":
    main()