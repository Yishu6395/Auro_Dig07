import xml.etree.ElementTree as ET

from heapq import *

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

l = [1, 22, 3]
heapify(l)
heappush(l, 5)
print(l)
l.remove(3)
print(l)

def AddOrder(b, op, price, vol, id):
    global buy
    global sell
    while(len(buy) < int(b[5:])):
        p = []
        q = []
        heapify(p)
        heapify(q)
        buy.append(p)
        sell.append(q)

    n = int(b[5:]) -1
    if(op == "SELL"):
        book = buy[n]
        m = len(book)
        if(m == 0):
            heappush(sell[n], [price, vol, id])

        elif(price > (-1)*book[0][0]):
            heappush(sell[n], [price, vol, id])

        else:
            v = book[0][1]
            if(v == vol):
                heappop(buy[n])
            elif(v > vol):
                buy[n][0][1] -= vol
            else:
                heappop(buy[n])
                AddOrder(b, op, price, vol - v, id)

    else:
        book = sell[n]
        m = len(book)
        if(m == 0):
            heappush(buy[n], [(-1)*price, vol, id])

        elif(price < book[0][0]):
            heappush(buy[n], [(-1)*price, vol, id])

        else:
            v = book[0][1]
            if(v == vol):
                heappop(sell[n])
            elif(v > vol):
                sell[n][0][1] -= vol
            else:
                heappop(sell[n])
                AddOrder(b, op, price, vol - v, id)

def DeleteOrder(b, id):
    global buy
    global sell
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

for i in range(order_len):
    a = root[i].attrib
    alen = len(a)
    if(alen == 2):
        # for deleting an order
        DeleteOrder(a['book'], a['orderId'])
    else:
        #for adding an order
        AddOrder(a['book'], a['operation'], float(a['price']), int(a['volume']), int(a['orderId']))


# The code for printing the table is yet to be done
# Else the order book is well maintained and up to date 