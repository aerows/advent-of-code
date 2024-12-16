from typing import TypeVar, Generic, Optional, Iterator, List, Union

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data: T = data
        self.next: Optional[Node[T]] = None
        self.prev: Optional[Node[T]] = None

    def replace_with(self, replacement: Union[T, "LinkedList[T]"]) -> None:
        """
        Replace this node with either a new value or an entire linked list.
        If a linked list is provided, it will be spliced into the current position.
        """
        if isinstance(replacement, LinkedList):
            if replacement.is_empty():
                # If replacement list is empty, just remove this node
                if self.prev:
                    self.prev.next = self.next
                if self.next:
                    self.next.prev = self.prev
                return

            # Connect the previous node to the start of replacement list
            if self.prev:
                self.prev.next = replacement.head
            if replacement.head:
                replacement.head.prev = self.prev

            # Connect the next node to the end of replacement list
            if self.next:
                self.next.prev = replacement.tail
            if replacement.tail:
                replacement.tail.next = self.next

            # Update list size in the parent list if we can access it
            if hasattr(self, "_parent_list"):
                parent_list = getattr(self, "_parent_list")
                parent_list._size += replacement.size() - 1
        else:
            # Simple value replacement
            self.data = replacement


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size: int = 0

    def append(self, data: T) -> Node[T]:
        """Add a new node with given data to the end of the list. Returns the created node."""
        new_node = Node(data)
        setattr(new_node, "_parent_list", self)  # Add reference to parent list

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            if self.tail:
                self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        return new_node

    def iterNodes(self) -> Iterator[Node[T]]:
        """Make the linked list iterable."""
        current = self.head
        while current:
            yield current
            current = current.next

    def prepend(self, data: T) -> Node[T]:
        """Add a new node with given data to the start of the list. Returns the created node."""
        new_node = Node(data)
        setattr(new_node, "_parent_list", self)  # Add reference to parent list

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
        return new_node

    def delete(self, data: T) -> bool:
        """Delete the first occurrence of data in the list. Returns True if found and deleted."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self._size -= 1
                return True
            current = current.next
        return False

    def insert_at(self, index: int, data: T) -> bool:
        """Insert data at given index. Returns False if index out of range."""
        if index < 0 or index > self._size:
            return False

        if index == 0:
            self.prepend(data)
            return True

        if index == self._size:
            self.append(data)
            return True

        current = self.head
        for _ in range(index):
            if current:
                current = current.next

        if current:
            new_node = Node(data)
            new_node.prev = current.prev
            new_node.next = current
            if current.prev:
                current.prev.next = new_node
            current.prev = new_node
            self._size += 1
            return True
        return False

    def find(self, data: T) -> Optional[int]:
        """Find the index of first occurrence of data. Returns None if not found."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return None

    def get(self, index: int) -> Optional[T]:
        """Get data at given index. Returns None if index out of range."""
        if index < 0 or index >= self._size:
            return None

        # Optimize by starting from tail for indices closer to the end
        if index > self._size // 2:
            current = self.tail
            for _ in range(self._size - 1 - index):
                if current:
                    current = current.prev
        else:
            current = self.head
            for _ in range(index):
                if current:
                    current = current.next

        return current.data if current else None

    def reverse_iter(self) -> Iterator[T]:
        """Iterate through the list in reverse."""
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def to_list(self) -> List[T]:
        """Convert the linked list to a Python list."""
        result: List[T] = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def size(self) -> int:
        """Return the number of nodes in the list."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if the list is empty."""
        return self._size == 0

    def __iter__(self) -> Iterator[T]:
        """Make the linked list iterable."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        """String representation of the linked list."""
        return " <-> ".join(str(item) for item in self) + " <-> None"
