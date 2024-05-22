import CynanBot.misc.utils as utils


# This class was taken from online:
# https://gist.github.com/jerryan999/6677a2619e8175e54ed05d3c6e1621cf
#
# I then slightly tweaked it for simplification... (fingers crossed it works)
class LinkedNode():

    def __init__(self, key: str):
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        self.key: str = key
        self.next: LinkedNode | None = None
        self.prev: LinkedNode | None = None


class LruCache():

    def __init__(self, capacity: int):
        if not utils.isValidInt(capacity):
            raise TypeError(f'capacity argument is malformed: \"{capacity}\"')
        elif capacity < 2 or capacity > utils.getIntMaxSafeSize():
            raise ValueError(f'capacity argument is out of bounds: {capacity}')

        self.__capacity: int = capacity
        self.__lookup: dict[str, LinkedNode | None] = dict()
        self.__stub: LinkedNode = LinkedNode("stub")
        self.__head: LinkedNode | None = self.__stub.next
        self.__tail: LinkedNode | None = self.__stub.next

    def __append_new_node(self, newNode: LinkedNode):
        """  add the new node to the tail end
        """
        if not self.__tail:
            self.__head = newNode
            self.__tail = newNode
        else:
            self.__tail.next = newNode
            newNode.prev = self.__tail
            self.__tail = self.__tail.next

    def contains(self, key: str) -> bool:
        if not utils.isValidStr(key) or key not in self.__lookup:
            return False

        node = self.__lookup[key]

        if node is not self.__tail:
            assert node
            self.__unlink_cur_node(node)
            self.__append_new_node(node)

        return True

    def put(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        if key in self.__lookup:
            self.contains(key)
            return

        if len(self.__lookup) == self.__capacity:
            # remove head node and corresponding key
            assert self.__head
            self.__lookup.pop(self.__head.key)
            self.__remove_head_node()

        # add new node and hash key
        newNode: LinkedNode = LinkedNode(key)
        self.__lookup[key] = newNode
        self.__append_new_node(newNode)

    def __remove_head_node(self):
        if not self.__head:
            return

        prev = self.__head
        self.__head = self.__head.next

        if self.__head:
            self.__head.prev = None

        del prev

    def __unlink_cur_node(self, node: LinkedNode):
        """ unlink current linked node
        """
        if self.__head is node:
            self.__head = node.next

            if node.next:
                node.next.prev = None

            return

        # removing the node from somewhere in the middle; update pointers
        prev, nex = node.prev, node.next
        assert prev and nex
        prev.next = nex
        nex.prev = prev
