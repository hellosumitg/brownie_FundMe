from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]  # most rectly deployed or last "FundMe"
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    # We added "getEntranceFee()" in "FundMe.sol" file
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()


# looks like on running "brownie run scripts/fund_and_withdraw.py --network ganache-local" everything is good and above script we can run on a main network if we'd like
# Now again it's still much better for us to run on tests and for these tests we would have to quit our Ganache-UI for further move
