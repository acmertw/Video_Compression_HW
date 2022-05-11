import math

oriImgMatrix = [
    [126, 159, 178, 181],
    [ 98, 151, 181, 181],
    [ 80, 137, 176, 156],
    [ 75, 114,  88,  68]
]

zigZagScanIndex = [
    [ 0,  1,  5,  6],
    [ 2,  4,  7, 12],
    [ 3,  8, 11, 13],
    [ 9, 10, 14, 15]
]

def forwardDCT():
    # 產生一個4x4的list
    fdctMatrix = [[0 for x in range(4)] for y in range(4)]

    for u in range(4):
        for v in range(4):
            sum = 0.0

            for m in range(4):
                for n in range(4):
                    val1 = ((2 * m + 1) * u * math.pi) / 8
                    val2 = ((2 * n + 1) * v * math.pi) / 8
                    tmp = oriImgMatrix[m][n] * math.cos(val1) * math.cos(val2)
                    sum += tmp

            constU = 1/math.sqrt(2)
            constV = 1/math.sqrt(2)

            if u == 0:
                constU = 1 / 2
            if v == 0:
                constV = 1 / 2

            sum = constU * constV * sum

            truncatedSum = int(sum * 100) / 100.0  #小數第三位開始無條件捨去, 只保留兩位小數
            fdctMatrix[u][v] = float(truncatedSum)

    return fdctMatrix

def inverseDCT(inverseZigZagMatrix):
    idctMatrix = [[0 for x in range(4)] for y in range(4)]

    for m in range(4):
        for n in range(4):
            sum = 0.0

            for u in range(4):
                for v in range(4):
                    constU = 1 / math.sqrt(2)
                    constV = 1 / math.sqrt(2)
                    if u == 0:
                        constU = 1 / 2
                    if v == 0:
                        constV = 1 / 2

                    val1 = ((2 * m + 1) * u * math.pi) / 8
                    val2 = ((2 * n + 1) * v * math.pi) / 8
                    tmp = constU * constV * inverseZigZagMatrix[u][v] * math.cos(val1) * math.cos(val2)
                    sum += tmp

            truncatedSum = int(sum * 100) / 100.0  # 小數第三位開始無條件捨去, 只保留兩位小數
            idctMatrix[m][n] = float(truncatedSum)

    return idctMatrix

def zigZagScan(fdcMatrix, n):
    scanResult = [0] * 16
    truncateCoeff = [0] * 16
    for i in range(4):
        for j in range(4):
            index = zigZagScanIndex[i][j]
            scanResult[index] = fdcMatrix[i][j]

    #Truncate coefficient : 只保留絕對值前5大係數, 其於係數變成0
    truncateCoeff[0] = scanResult[0]
    truncateCoeff[1] = scanResult[1]
    truncateCoeff[2] = scanResult[2]
    truncateCoeff[5] = scanResult[5]
    truncateCoeff[8] = scanResult[8]
    

    return truncateCoeff

def inverseZigZagScan(truncateCoeff):
    inverseZigZagMatrix = [[0 for x in range(4)] for y in range(4)]
    inverseZigZagMatrix[0][0] = truncateCoeff[0]
    index = 1
    # 擺放上半部的係數
    for level in range(1, 4):
        if level % 2 == 0:
            i = level
            j = 0
        else:
            i = 0
            j = level

        count = level + 1
        while count > 0:
            inverseZigZagMatrix[i][j] = truncateCoeff[index]
            index = index + 1
            count = count - 1
            if level % 2 == 0:
                i = i - 1
                j = j + 1
            else:
                i = i + 1
                j = j - 1

    # 擺放下半部的係數
    startx = 1
    for level in range(4, 7):
        if level % 2 == 0:
            i = 3
            j = startx
        else:
            i = startx
            j = 3

        startx = startx + 1
        count = 3 - level
        while count > 0:
            inverseZigZagMatrix[i][j] = truncateCoeff[index]
            index = index + 1
            count = count - 1
            if level % 2 == 0:
                i = i - 1
                j = j + 1
            else:
                i = i + 1
                j = j - 1

    return inverseZigZagMatrix

if __name__ == '__main__':
    # 定義題目上的n
    n = 1

    #Step 1 : 計算DCT
    fdctMatrix = forwardDCT()
    print("Print out fdctMatrix ==> ")
    for row in fdctMatrix:
        print("{: >6} {: >6} {: >6} {: >6} ".format(*row))

    #Step 2 : 將DCT結果做zig-zag scan得到1-D array, 且只保留想要的係數個數n
    scanResult = zigZagScan(fdctMatrix, n)
    print("\nPrint out scanResult ==> ")
    print(scanResult)

    # Step 3 : 將Step2結果轉回到2-D matrix
    inverseZigZagMatrix = inverseZigZagScan(scanResult)
    print("\nPrint out inverseZigZagMatrix ==> ")
    for row in inverseZigZagMatrix:
        print("{: >6} {: >6} {: >6} {: >6} ".format(*row))

    #Step 4 : 將2-D matrix透過IDCT轉回image
    decodedImgMatrix = inverseDCT(inverseZigZagMatrix)
    print("\nPrint out decodedImgMatrix ==> ")
    for row in decodedImgMatrix:
        print("{: >6} {: >6} {: >6} {: >6}".format(*row))
