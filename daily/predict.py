from core.researchScript import main,readSP500

if __name__ == "__main__":
    # Set parameters here
    period=2
    buyNStd = 1
    buyNVol = 1.5
    sellNStd = 1
    sellNVol = 1
    klapse = 300
    ifplot = False
    rootdir = "../historicalData"
    sp500 = 0
    main(period, buyNStd, buyNVol, sellNStd, sellNVol, klapse, rootdir, ifplot, sp500)

