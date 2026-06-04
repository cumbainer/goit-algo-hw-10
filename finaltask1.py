class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    @classmethod
    def from_list(cls, values):
        linked_list = cls()
        for value in values:
            linked_list.append(value)
        return linked_list

    def to_list(self):
        values = []
        current = self.head

        while current:
            values.append(current.value)
            current = current.next

        return values

    def print_list(self):
        print(" -> ".join(map(str, self.to_list())))


def reverse_linked_list(head):
    previous = None
    current = head

    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node

    return previous


def split_list(head):
    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    middle = slow.next
    slow.next = None
    return head, middle


def merge_sorted_lists(left, right):
    dummy = Node(0)
    tail = dummy

    while left and right:
        if left.value <= right.value:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next

        tail = tail.next

    tail.next = left or right
    return dummy.next


def sort_linked_list(head):
    if head is None or head.next is None:
        return head

    left, right = split_list(head)
    left = sort_linked_list(left)
    right = sort_linked_list(right)

    return merge_sorted_lists(left, right)


linked_list = LinkedList.from_list([1, 2, 3, 4, 5])
linked_list.head = reverse_linked_list(linked_list.head)
print("Reversed list:")
linked_list.print_list()

unsorted_list = LinkedList.from_list([7, 2, 9, 1, 5, 3])
unsorted_list.head = sort_linked_list(unsorted_list.head)
print("Sorted list:")
unsorted_list.print_list()

first = LinkedList.from_list([1, 3, 5, 7])
second = LinkedList.from_list([2, 4, 6, 8])
merged = LinkedList()
merged.head = merge_sorted_lists(first.head, second.head)
print("Merged sorted lists:")
merged.print_list()
