def reverse_nodes(self, i: int) -> None:
	if i == 0:
		curr = self._first

		self._first = curr.next
		curr.next = self._first.next
		self._first.next = curr

	else:
		curr = self._first

		for unused_ in range(i - 1):
			curr = curr.next

		temp = curr.next
		curr.next = curr.next.next.next
		temp.next = curr