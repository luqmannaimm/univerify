"""
bst.py

Standalone Binary Search Tree (BST) implementation used by the Univerify app
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
      - A node in the BST that wraps a document
    """
    def __init__(self, document):
        self.doc = document
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

class Tree:
    """
    Tree Class
    ===========
      - Standard Binary Search Tree (BST) implementation
    """
    def __init__(self):
        self.root: Optional[Node] = None

    def insert(self, doc) -> bool:
        """Insert a new document into the tree"""
        key = int(doc.doc_id)
        if self.search(key) is not None:
            print(f"Document {key} already exists. Update or Search instead.")
            return False

        def _insert_node(node: Optional[Node], doc) -> Node:
            if node is None:
                return Node(doc)
            k = int(doc.doc_id)
            if k < int(node.doc.doc_id):
                node.left = _insert_node(node.left, doc)
            else:
                node.right = _insert_node(node.right, doc)
            return node

        was_empty = self.root is None
        self.root = _insert_node(self.root, doc)
        if was_empty:
            print(f"Inserted root: {key}")
        else:
            print(f"Inserted: {key}")
        return True

    def search(self, doc_id: int):
        """Search for a document in the tree"""
        node = self.root
        while node:
            if int(doc_id) == int(node.doc.doc_id):
                print(f"\nFound: {node.doc}")
                return node.doc
            elif int(doc_id) < int(node.doc.doc_id):
                node = node.left
            else:
                node = node.right
        print("Document not found.")
        return None

    def update(self, doc_id: int, new_status: str):
        """Update document status"""
        doc = self.search(doc_id)
        if doc:
            doc.status = new_status
            print(f"Updated Status to '{new_status}' for Document {doc_id}")
            return doc
        return None

    def delete(self, doc_id: int) -> bool:
        """Delete a document from the tree"""
        def _min_value_node(node: Node) -> Node:
            current = node
            while current.left is not None:
                current = current.left
            return current

        def _delete_node(node: Optional[Node], key: int) -> Optional[Node]:
            if node is None:
                return None
            if key < int(node.doc.doc_id):
                node.left = _delete_node(node.left, key)
            elif key > int(node.doc.doc_id):
                node.right = _delete_node(node.right, key)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                temp = _min_value_node(node.right)
                node.doc = temp.doc
                node.right = _delete_node(node.right, int(temp.doc.doc_id))
            return node

        if self.search(doc_id) is None:
            print("Document not found, cannot delete.")
            return False
        self.root = _delete_node(self.root, int(doc_id))
        print(f"Deleted Document {doc_id}")
        return True

    def display_root(self) -> None:
        """Display the current root document"""
        if self.root:
            print(f"Current Root: {self.root.doc}")
        else:
            print("Tree is empty.")
