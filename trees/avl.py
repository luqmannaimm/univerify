"""
avl.py

Standalone AVL tree implementation used by the Univerify app
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
      - A node in the AVL tree that wraps a document
    """

    def __init__(self, document):
        self.doc = document
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.height: int = 1


class Tree:
    """
    Tree Class
    ===========
      - AVL Tree with balancing on insert/delete
      - Left-Left (single right rotation)
      - Right-Right (single left rotation)
      - Left-Right (left rotation followed by right rotation)
      - Right-Left (right rotation followed by left rotation)
    """

    def __init__(self):
        self.root: Optional[Node] = None

    def _right_rotate(self, y: Node) -> Node:
        """Perform right rotation around node y"""

        # Perform right rotation
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max((y.left.height if y.left else 0), (y.right.height if y.right else 0))
        x.height = 1 + max((x.left.height if x.left else 0), (x.right.height if x.right else 0))
        
        return x

    def _left_rotate(self, x: Node) -> Node:
        """Perform left rotation around node x"""

        # Perform left rotation
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max((x.left.height if x.left else 0), (x.right.height if x.right else 0))
        y.height = 1 + max((y.left.height if y.left else 0), (y.right.height if y.right else 0))
        
        return y

    def insert(self, doc) -> bool:
        """Insert a new document into the tree"""

        # Get key
        key = int(doc.doc_id)

        # Check if document key exists
        if self.search(key) is not None:
            print(f"Document {key} already exists. Update or Search instead.")
            return False

        # Helper function for tree height
        def _height(node: Optional[Node]) -> int:
            return node.height if node else 0

        # Helper function for tree balance
        def _get_balance(node: Optional[Node]) -> int:
            return _height(node.left) - _height(node.right) if node else 0

        # Helper function for node insertion
        def _insert_node(node: Optional[Node], doc) -> Node:

            # Insert node
            if node is None:
                return Node(doc)
            
            # Insert node recursively
            k = int(doc.doc_id)
            if k < int(node.doc.doc_id):
                node.left = _insert_node(node.left, doc)
            else:
                node.right = _insert_node(node.right, doc)

            # Update height and balance
            node.height = 1 + max(_height(node.left), _height(node.right))
            balance = _get_balance(node)

            # Left Left
            if balance > 1 and k < int(node.left.doc.doc_id):
                return self._right_rotate(node)

            # Right Right
            if balance < -1 and k > int(node.right.doc.doc_id):
                return self._left_rotate(node)

            # Left Right
            if balance > 1 and k > int(node.left.doc.doc_id):
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)

            # Right Left
            if balance < -1 and k < int(node.right.doc.doc_id):
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

            return node

        # Insert node and balance tree
        was_empty = self.root is None
        self.root = _insert_node(self.root, doc)
        if was_empty:
            print(f"Inserted root: {key}")
        else:
            print(f"Inserted and Splayed to root: {key}")
        return True

    def search(self, doc_id: int):
        """Search for a document in the tree"""

        # Get node
        node = self.root

        # Search for document
        while node:
            if int(doc_id) == int(node.doc.doc_id):
                # found
                print(f"\nFound and Splayed: {node.doc}")
                return node.doc
            elif int(doc_id) < int(node.doc.doc_id):
                node = node.left
            else:
                node = node.right
        print("Document not found.")

        return None

    def update(self, doc_id: int, new_status: str):
        """Update document status"""

        # Find document
        doc = self.search(doc_id)

        # Update status if found
        if doc:
            doc.status = new_status
            print(f"Updated Status to '{new_status}' for Document {doc_id}")
            return doc

        return None

    def delete(self, doc_id: int) -> bool:
        """Delete a document from the tree"""

        # Helper function for tree height
        def _height(node: Optional[Node]) -> int:
            return node.height if node else 0

        # Helper function for tree balance
        def _get_balance(node: Optional[Node]) -> int:
            return _height(node.left) - _height(node.right) if node else 0

        # Helper function to find node with minimum value
        def _min_value_node(node: Node) -> Node:
            current = node
            while current.left is not None:
                current = current.left
            return current

        # Helper function for node deletion
        def _delete_node(node: Optional[Node], key: int) -> Optional[Node]:

            # Do nothing if no node
            if node is None:
                return None
            
            # Delete node
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

            # Update height and balance
            node.height = 1 + max(_height(node.left), _height(node.right))
            balance = _get_balance(node)

            # Left Left
            if balance > 1 and _get_balance(node.left) >= 0:
                return self._right_rotate(node)

            # Left Right
            if balance > 1 and _get_balance(node.left) < 0:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)

            # Right Right
            if balance < -1 and _get_balance(node.right) <= 0:
                return self._left_rotate(node)

            # Right Left
            if balance < -1 and _get_balance(node.right) > 0:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

            return node

        # Check if document key exists
        if self.search(doc_id) is None:
            print("Document not found, cannot delete.")
            return False

        # Perform node deletion
        self.root = _delete_node(self.root, int(doc_id))
        print(f"Deleted Document {doc_id}")
        return True

    def display_root(self) -> None:
        """Display the current root document"""

        if self.root:
            print(f"Current Root: {self.root.doc}")
        else:
            print("Tree is empty.")
