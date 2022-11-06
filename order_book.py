import xml.etree.ElementTree as ET

from heapq import *
from time import *
import threading

# Passing the path of the
# xml document to enable the
# parsing process

tree = ET.parse('orders.xml')

# getting the parent tag of
# the xml document

root = tree.getroot()

# total number of orders
order_len = len(root)

buy = []
sell = []

buy2 = []
sell2 = []

def AddOrder(boo, op, price, vol, id):
    global buy
    global sell
    global buy2, sell2
    n = int(boo[5:]) - 1
    while(len(buy) < n+1):
        p = []
        q = []
        p1 = []
        q1 = []
        heapify(p)
        heapify(q)
        heapify(p1)
        heapify(q1)
        buy.append(p)
        sell.append(q)
        buy2.append(p1)
        sell2.append(q1)

    if(op == "SELL"):
        book = buy[n]
        m = len(book)
        if(m == 0):
            heappush(sell[n], [price, vol, id])
            heappush(sell2[n], [id, vol, price])

        elif(price > (-1)*book[0][0]):
            heappush(sell[n], [price, vol, id])
            heappush(sell2[n], [id, vol, price])

        else:
            v = book[0][1]
            if(v == vol):
                [a, b, c] = heappop(buy[n])
                buy2[n].remove([c, b, a])
            elif(v > vol):
                [a, b, c] = buy[n][0]
                buy[n][0][1] -= vol
                buy2[n].remove([c, b, a])
                heappush(buy2[n], [c, b-vol, a])
            else:
                [a, b, c] = heappop(buy[n])
                buy2[n].remove([c, b, a])
                AddOrder(boo, op, price, vol - v, id)

    else:
        book = sell[n]
        m = len(book)
        if(m == 0):
            heappush(buy[n], [(-1)*price, vol, id])
            heappush(buy2[n], [id, vol, (-1)*price])

        elif(price < book[0][0]):
            heappush(buy[n], [(-1)*price, vol, id])
            heappush(buy2[n], [id, vol, (-1) * price])

        else:
            v = book[0][1]
            if(v == vol):
                [a, b, c] = heappop(sell[n])
                sell2[n].remove([c, b, a])
            elif(v > vol):
                [a, b, c] = sell[n][0]
                sell[n][0][1] -= vol
                sell2[n].remove([c, b, a])
                heappush(sell2[n], [c, b-vol, a])
            else:
                [a, b, c] = heappop(sell[n])
                sell2[n].remove([c, b, a])
                AddOrder(boo, op, price, vol - v, id)

def DeleteOrder(b, id):
    global buy
    global sell, buy2, sell2
    n = int(b[5:]) - 1
    bb = buy[n]
    sb = sell[n]
    k = -1
    for i in range(len(bb)):
        if(bb[i][2] == id):
            k = i
            break
    if(k != -1):
        a0 = bb[k][0]
        a1 = bb[k][1]
        buy[n].remove([a0, a1, id])
        return

    for i in range(len(sb)):
        if(sb[i][2] == id):
            k = i
            break
    if(k != -1):
        a0 = sb[k][0]
        a1 = sb[k][1]
        sell[n].remove([a0, a1, id])
        return

st = time()

count = 0

print("Lets begin")
def fetch(threadNo):
    global count
    for i in range(order_len):
        a = root[i].attrib
        alen = len(a)
        y = int(a['book'][5:])
        if(y != threadNo):
            continue;
        if(alen == 2):
            # for deleting an order
            DeleteOrder(a['book'], a['orderId'])
            count += 1
            #print("Deleted : {}".format(i))
        else:
            #for adding an order
            AddOrder(a['book'], a['operation'], float(a['price']), int(a['volume']), int(a['orderId']))
            count += 1
            #print("Added : {}".format(i))


threads = []
startTime = time()
noOfThreads = 3

for i in range(noOfThreads):  # for connection 1
    x = threading.Thread(target=fetch, args=(i+1,))
    threads.append(x)
    x.start()

while(count <= order_len):
    if(count < order_len):
        continue;
    for i in range(3):
        print("Book : {}".format(i))
        print("BUY")
        for j in range(len(buy[i])):
            print("{} @ {}".format(buy[i][j][1],(-1)*buy[i][j][0]))
        print(" ")
        print("SELL")
        for j in range(len(sell[i])):
            print("{} @ {}".format(sell[i][j][1], sell[i][j][0]))

        print(" ")
    print("Done")
    break

et = time()
print(et - st)

# The code for printing the table is yet to be done
# Else the order book is well maintained and up to date