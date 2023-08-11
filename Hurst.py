import yfinance as yf
import matplotlib.pyplot as plt
from hurst import compute_Hc
import statistics

asset = yf.download("^BVSP", start = "1995-01-01", interval = "1d", rounding = True)
assetClosing = asset["Adj Close"]
assetOpening = asset["Open"]
print("Asset return: ", str(round((assetClosing[len(assetClosing) - 1]/assetOpening[0] - 1) * 100, 2)) + "%")
print("Asset length: ", len(assetClosing))

for x in range(50, 100, 5):
    periodAnalysis = 50
    count = 0
    high = 0
    low = 0
    roi = 1
    buy = False
    sell = False

    start = periodAnalysis
    end = len(assetClosing)
    
    #Começa o loop a partir da janela móvel que se quer analisar
    for i in range(start, end, 1):
        auxAsset = assetClosing[i - periodAnalysis : i]

        lastMean = statistics.mean(auxAsset)
        currentMean = statistics.mean(assetClosing[i - periodAnalysis + 1 : i + 1])

        if (i != periodAnalysis) and (i != len(assetClosing) - 1):
            if buy:
                roi = roi * (assetOpening[i + 1]/assetOpening[i])
                buy = False
            if sell:
                roi = roi * ((1 - assetOpening[i + 1]/assetOpening[i]) + 1)
                sell = False

        H, c, data = compute_Hc(auxAsset, kind = 'random_walk', min_window = 5, max_window = periodAnalysis)
        
        if H > (x / 100):
            count += 1

            if(currentMean - lastMean) > 0:
                high += 1
                buy = True
            if(currentMean - lastMean) < 0:
                low += 1
                #sell = True

    if (high == 0) and (low == 0):
        break

    print("\nH = " + str(x / 100))
    print("H > " + str(x / 100) + ": " + str(count))
    print("Percentage: " + str(round(count / len(assetClosing) * 100, 2)) + "%")
    print("High: ", high)
    print("Low: ", low)
    print("Strategy return: " + str(round((roi - 1) * 100, 2)) + "%")


'''
Possibilidades a fazer:
- Considerar a cotação do ativo para verificar quantidades que podem ser compradas com o capital disponível
- Considerar custos operacionais
'''