from notecoin.database.base import Base, BaseTable, create_all, session
from notecoin.okex.client.const import account_api
from sqlalchemy import Column, Float, String


class OkexClientAccountBalance(Base, BaseTable):
    __tablename__ = 'okex_client_account_balance'
    ccy = Column(String(120), comment='币种', primary_key=True)
    eq = Column(Float(), comment='币种总权益', primary_key=True)
    cashBal = Column(Float(), comment='币种余额')
    uTime = Column(Float(), comment='币种余额信息的更新时间毫秒')

    disEq = Column(Float(), comment='美金层面币种折算权益')
    availBal = Column(Float(), comment='可用余额')
    frozenBal = Column(Float(), comment='币种占用金额')
    ordFrozen = Column(Float(), comment='挂单冻结数量')
    twap = Column(Float(), comment='当前负债币种触发系统自动换币的风险')
    eqUsd = Column(Float(), comment='币种权益美金价值')
    stgyEq = Column(Float(), comment='策略权益')

    def __init__(self, *args, **kwargs):
        self.ccy = kwargs.get("ccy")
        self.eq = kwargs.get("eq", 0)
        self.cashBal = kwargs.get("cashBal", 0)
        self.uTime = kwargs.get("uTime", 0)
        self.disEq = kwargs.get("disEq", 0)
        self.availBal = kwargs.get("availBal", 0)
        self.frozenBal = kwargs.get("frozenBal", 0)
        self.ordFrozen = kwargs.get("ordFrozen", 0)

        self.twap = kwargs.get("twap", 0)
        self.eqUsd = kwargs.get("eqUsd", 0)
        self.stgyEq = kwargs.get("stgyEq", 0)

    def __repr__(self):
        return f"ccy{self.ccy},availBal:{self.availBal}"

    @staticmethod
    def update():
        res = account_api.get_account().data

        try:
            data = res[0]['details']
            create_all()
            for detail in data:
                session.merge(OkexClientAccountBalance(**detail))
            session.commit()
            return {"success": len(data)}
        except Exception as e:
            session.rollback()
            return {"error": str(e), "res": res}
