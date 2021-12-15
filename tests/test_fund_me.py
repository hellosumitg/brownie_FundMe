from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    # We add 100 so if we need a little bit more money it will be fine for us
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # So as to check our account "address" and the "amount" that we funded is being adequately recorded
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# And for checking just run "brownie test" or "brownie test --network development" to check above test code
# We can also run this test on "rinkeby" or other live network, but it will take time to run all the functionality.
# So sometimes we only want to run tests on our local chains and we can do this by using the "skip" functionality of "pytest"
# So for checking this "skip" functionality lets write a new function below:-


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
        # And now whem we run this command "brownie test -k test_only_owner_can_withdraw --network rinkeby" uupto this above code we will one test is skipped and have output "-s"
        account = get_account()
        fund_me = deploy_fund_me()
        bad_actor = accounts.add()  # some other person
        # As we know in our "FundMe.sol" file our "withdraw()" has the only owner modifier see this code snippet from "FundMe.sol":-
        """modifier onlyOwner() {
        require(msg.sender == owner);
        _;
        }"""
        # As running test code will raise error now so fixing that error we use below code for creating exceptions
        with pytest.raises(exceptions.VirtualMachineError):
            fund_me.withdraw({"from": bad_actor})


# Now the last version of testing is "Mainnet Forking" and it's incredibly powerful when we are working with smart contracts on mainnet that we want to test locally.
# So, a forked blockchain iterally takes a copy of an existing blockchain and brings it iinto our local computer for us to work with and we have control of this blockchain,...
# ...Since it's going to run on our local computer similar to ganache and now all the interctaions that we do on this local blockchain are not going to affect the real blockchain
# because it's a simulated blockchain, we can go ahead and interact with "Price_Feed" contracts, "Aave" contracts and other contracts...which are already on the chain.
# Mainnet Fork is a built in part of "brownie netwoks" and also pulls from infura the same way it works with Rinkeby, Kovan and other networks just we have to add this to networks in the "brownie-confi.yaml" file.
# And now when we run this command "brownie test --network mainnet-fork-dev" we would get our test has been pass successfully.
