"""
splay.py

Standalone Splay tree implementation used by the Univerify app
 - insert(Document) -> bool
 - search(doc_id) -> Optional[Document]
 - update(doc_id, new_status) -> Optional[Document]
 - delete(doc_id) -> bool
 - display_root() -> None

"""

from __future__ import annotations

from typing import Optional

class Node:
    """
    Node Class
    ===========
      - A node in the splay tree that wraps a document
    """

    def __init__(self, document):
        self.doc = document
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


class Tree:
    """
    Tree Class
    ===========
      - Zig (single rotation when parent is root)
      - Zig-Zig (two rotations when node and parent are both left or both right children of their parents)
      - Zig-Zag (two rotations when node and parent are opposite-side children)
    """

    def __init__(self):
        self.root: Optional[Node] = None

    def _right_rotate(self, x: Node) -> Node:
        """Perform right rotation around node x"""

        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x: Node) -> Node:
        """Perform left rotation around node x"""

        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[Node], key: int) -> Optional[Node]:
        """Splay the node with the given key to the root of the tree"""

        # If root is None or key is at root, return root
        if root is None or root.doc.doc_id == key:
            return root

        # Key lies in left subtree
        if key < root.doc.doc_id:

            # Key not in left tree
            if root.left is None:
                return root
            
            # Zig-Zig (Left Left)
            if key < root.left.doc.doc_id:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)

            # Zig-Zag (Left Right)
            elif key > root.left.doc.doc_id:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)
            
            # Return root after rotation completion
            return self._right_rotate(root) if root.left else root
        
        # Key lies in right subtree
        else:

            # Key not in right tree
            if root.right is None:
                return root
            
            # Zig-Zig (Right Right)
            if key < root.right.doc.doc_id:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)

            # Zig-Zag (Right Left)
            elif key > root.right.doc.doc_id:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)

            # Return root after rotation completion
            return self._left_rotate(root) if root.right else root

    def insert(self, doc) -> bool:
        """Insert a document into the tree and splay it to the root"""

        # If tree is empty, insert node as root
        if self.root is None:
            self.root = Node(doc)
            print(f"Inserted root: {doc.doc_id}")
            return True
        
        # Splay the document to be inserted to the root
        self.root = self._splay(self.root, doc.doc_id)

        # If document already exists, do not insert
        if self.root.doc.doc_id == doc.doc_id:
            print(f"Document {doc.doc_id} already exists. Update or Search instead.")
            return False
        
        # Create new node
        node = Node(doc)

        # Insert to left or right subtree
        if doc.doc_id < self.root.doc.doc_id:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None

        # Set new node as root
        self.root = node
        print(f"Inserted and Splayed to root: {doc.doc_id}")
        return True

    def search(self, doc_id: int):
        """Search for a document and splay it to the root"""

        # If tree is empty return nothing
        if not self.root:
            return None
        
        # Splay the searched document to the root
        self.root = self._splay(self.root, doc_id)

        # Check if found
        if self.root.doc.doc_id == doc_id:
            print(f"\nFound and Splayed: {self.root.doc}")
            return self.root.doc
        print("\nDocument not found!")
        return None

    def update(self, doc_id: int, new_status: str):
        """Update document status after splaying it to the root"""

        # Find document
        doc = self.search(doc_id)
        if doc:
            doc.status = new_status
            print(f"Updated Status to '{new_status}' for Document {doc_id}")
            return doc

        return None

    def delete(self, doc_id: int) -> bool:
        """Delete a document from the tree"""

        # If tree is empty do nothing
        if self.root is None:
            return False
        
        # Splay the document to be deleted to the root
        self.root = self._splay(self.root, doc_id)
        if self.root.doc.doc_id != doc_id:
            print("Document not found, cannot delete.")
            return False
        
        # Now delete the root
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
        """Display the current root document"""

        if self.root:
            print(f"Current Root: {self.root.doc}")
        else:
            print("Tree is empty.")

