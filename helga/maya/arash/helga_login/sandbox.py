import heapq
op  = []
heapq.heapify(op)



heapq.heappush(op, 3)
heapq.heappush(op, 5)
heapq.heappush(op, 1)
heapq.heappush(op, 9)
heapq.heappush(op, 12)
heapq.heappush(op, 23)

print heapq.heappop(op)