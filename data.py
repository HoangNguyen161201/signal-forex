from oder import symbols

class SymboInfoTrade:
    # Constructor để khởi tạo các thuộc tính
    def __init__(self, candle1, candle2, lot, is_buy):
        self.candle1 = candle1
        self.candle2 = candle2
        self.lot = lot
        self.is_buy = is_buy
        self.is_hedging = False
        self.magic_1 = 0
        self.magic_2 = 0
        self.is_wait_to_cut = False
        self.is_update_sl = False

    def setPrepareTrade(self, candle1, candle2, is_buy, lot):
        self.lot = lot
        self.is_buy = is_buy
        self.candle1 = candle1
        self.candle2 = candle2

    def setMagic(self, value, isFirst):
        if(isFirst):
            self.magic_1 = value
        else:
            self.magic_2 = value

    def setIsHedging(self, is_hedging):
        self.is_hedging = is_hedging

    def setIsWaitToCut(self, is_wait_to_cut):
        self.is_wait_to_cut = is_wait_to_cut

    def setIsUpdateSl(self, is_update_sl):
        self.is_update_sl = is_update_sl

    def setLot(self, lot):
        self.lot = lot