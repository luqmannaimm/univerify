"""
Univerify Application
=====================
Description: A simple document verification system using a splay tree
Author: Luqman Naim bin Mohd Esa
Email: luqmannaim@graduate.utm.my
"""

import os
import json
from typing import List, Optional, Tuple

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


class SplayNode:
    """
    SplayNode Class
    ===============
      - A node in the splay tree that wraps a document
    """

    def __init__(self, document: Document):
        self.doc = document
        self.left: Optional["SplayNode"] = None
        self.right: Optional["SplayNode"] = None


class SplayTree:
    """
    SplayTree Class
    ===============
      - Zig (single rotation when parent is root)
      - Zig-Zig (two rotations when node and parent are both left or both right children of their parents)
      - Zig-Zag (two rotations when node and parent are opposite-side children)
    """

    def __init__(self):
        self.root: Optional[SplayNode] = None

    def _right_rotate(self, x: SplayNode) -> SplayNode:
        """
        Right rotation around node x.

        Before rotation:
            x
           / \
          y  T3
         / \
        T1  T2

        After rotation:
            y
           / \
         T1   x
             / \
            T2  T3
        """
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x: SplayNode) -> SplayNode:
        """
        Left rotation around node x.

        Before rotation:
            x
           / \
          T1  y
             / \
            T2  T3

        After rotation:
            y
           / \
          x   T3
         / \
        T1  T2
        """
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[SplayNode], key: int) -> Optional[SplayNode]:
        """
        Bring the node with the given key to the root of the subtree.
        The function returns the new subtree root after performing the
        necessary rotations. If the key is not present, the last accessed
        node (closest to the key) will be splayed to the root instead.
        """

        # Base case where root is None or key is at root
        if root is None or root.doc.doc_id == key:
            return root

        # Key lies in left subtree
        if key < root.doc.doc_id:

            # Key not found in left subtree
            if root.left is None:
                return root
            
            # Zig-Zig (Left Left): bring key up twice, then rotate right
            if key < root.left.doc.doc_id:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)

            # Zig-Zag (Left Right): rotate left on left child, then right on root
            elif key > root.left.doc.doc_id:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)

            # Final rotation brings the node upward
            return self._right_rotate(root) if root.left else root

        # Key lies in right subtree
        else:

            # Key not found in right subtree
            if root.right is None:
                return root
            
            # Zag-Zig (Right Left): rotate right on right child, then left on root
            if key < root.right.doc.doc_id:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)

            # Zag-Zag (Right Right): bring key up twice, then rotate left
            elif key > root.right.doc.doc_id:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)

            # Final rotation brings the node upward
            return self._left_rotate(root) if root.right else root

    def insert(self, doc: Document) -> bool:
        """
        Insert a Document into the tree.
        Returns True if inserted, False if a document with the same id exists.
        """

        # Empty tree: new node becomes root without rotations
        if self.root is None:
            self.root = SplayNode(doc)
            print(f"Inserted root: {doc.doc_id}")
            return True

        # Splay at the key
        self.root = self._splay(self.root, doc.doc_id)
        if self.root.doc.doc_id == doc.doc_id:
            print(f"Document {doc.doc_id} already exists. Update or Search instead.")
            return False

        # Insert new node and reattach subtrees
        node = SplayNode(doc)
        if doc.doc_id < self.root.doc.doc_id:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

        print(f"Inserted and Splayed to root: {doc.doc_id}")
        return True

    def search(self, doc_id: int) -> Optional[Document]:
        """
        Search for a document by id. If found, splay to root and return it.
        Returns the Document instance or None if not found.
        """

        # If tree is empty nothing to do
        if not self.root:
            return None
        
        # Bring the nearest node with respect to doc_id to the root
        self.root = self._splay(self.root, doc_id)
        if self.root.doc.doc_id == doc_id:
            print(f"\nFound and Splayed: {self.root.doc}")
            return self.root.doc
        
        # If the root's key differs, the document doesn't exist
        print("Document not found.")
        return None

    def update_status(self, doc_id: int, new_status: str) -> Optional[Document]:
        """
        Update the status field of the document and return it.
        """
        # Reuse search which splays the node if it exists
        doc = self.search(doc_id)

        # Update status if document found
        if doc:
            doc.status = new_status
            print(f"Updated Status to '{new_status}' for Document {doc_id}")
            return doc
        return None

    def delete(self, doc_id: int) -> bool:
        """
        Remove a document from the tree.
        Returns True when a node was removed; False otherwise.
        """

        # If tree empty nothing to delete
        if self.root is None:
            return False
        
        # Splay the tree at doc_id if document found
        self.root = self._splay(self.root, doc_id)
        if self.root.doc.doc_id != doc_id:
            print("Document not found, cannot delete.")
            return False

        # Delete the root node and re-attach subtrees
        if self.root.left is None:
            self.root = self.root.right
        else:
            temp = self.root.right
            self.root = self.root.left
            self.root = self._splay(self.root, doc_id)
            self.root.right = temp
        print(f"Deleted Document {doc_id}")
        return True

    def display_root(self) -> None:
        """
        Print a short representation of the current root (or empty).
        """
        if self.root:
            print(f"Current Root: {self.root.doc}")
        else:
            print("Tree is empty.")


class UniverifyApp:
    """
    Main Application Class
    ======================
      - List, Search, Insert, Update, Delete documents in the splay tree
    """

    def __init__(self, data_dir: str = None):
        """
        Initialize data directory and splay tree
        """

        # Set data directory (default: ./data)
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "data")

        # Initialize the splay tree
        self.tree = SplayTree()

    def _file_path(self, doc_id: int) -> str:
        """
        Helper function to get JSON file path
        """
        return os.path.join(self.data_dir, f"{doc_id}.json")

    def _load_all(self) -> List[Tuple[int, str, str, str]]:
        """
        Helper function to return a sorted list of rows (doc_id, applicant_id, doc_type, status)
        """
        rows: List[Tuple[int, str, str, str]] = []
        if not os.path.isdir(self.data_dir):
            return rows
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
        doc = self.tree.update_status(doc_id, status)
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
    app = UniverifyApp()
    app.run()

if __name__ == "__main__":
    main()