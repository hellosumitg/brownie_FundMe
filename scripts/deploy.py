from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# `from web3 import Web3`...now there is no use of importing "Web3" as it's already imported from "helpful_scripts.py" file


def deploy_fund_me():
    account = get_account()
    # as here this deploy() cause a state change so we always need to do it from account section
    # we need to pass the "price_feed_address" to our "FundMe" contract for this we have to paste the address as shown below
    # but this also not going to solve our problem the problem here is we again have hard-coded this rinkeby address so,
    # if we are on a persistent network like rinkeby use the associated address
    # otherwise, deploy mocks
    # this below "if" statement when we are not on the "development" chain...
    # if network.show_active() != "development":
    # now for using both "development and "ganache-local" we use list "LOCAL_BLOCKCHAIN_ENVIRONMENTS" from "helpful_scripts.py" file
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # price_feed_address = "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        # here by addiing the "price_feed_address" varibale for above "address" also doesn't make any change as we again passing a hard-coded rinkeby address
        # so for solveing this issue we have to parameterize where we get these addresses from. So for this we have to add different addresses to our "brownie-config.yaml" file...
        # ...so as to grab the address from our networks section this way we can define different addresses for this "price_feed_address" across different networks...

        # and What "if" we are on development chain  for that we can say "else" if we're not on a develpoment chain we're going to have to deploy a mock(i.e our own verion of the price_feed_contract this is known as Mocking) so right now
        # So for this we have to create a new folder called "test" in our contracts section
    else:
        # putting these below codes as a function naming "deploy_mocks()" in the "helpful_scripts.py" so as to make this file codes smaller
        """print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": account})
            # instead of 2000000000000000000000 we can write `Web3.toWei(2000, "ether")`
        print("Mocks Deployed!")
        """
        # using function for above codes instead...
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        # "MockV3Aggregator[-1].address" says to use the most recently deployed MockV3Aggregator
        # run the code using "brownie run scripts/deploy.py" wihtout the network flag
        # So we will deploy the "Mocks(i.e MockV3Aggregator)" first, then we do our "FundMe" and finally ran into an issue because we are trying to verify a contract on a chain that doesn't exist etherscan doesn't know about our local ganache chain...
        # ...so to fix this instead of doing "publish_source = True" below, we can have this "publish_source" be again based on what chain that we're on so we'll go back to "brownie-config.yaml" file in "networks:"..."rinkeby:" and add "verify: True"...
        # but for ..."development:"add "verify: False""
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # publish_source=True,
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()


"""
After putting the account detail of deployed contract for viewing our "Transaction's Contract" detail in easy to interact format on the "https://rinkeby.etherscan.io/"
we have to "Verify and Publish" it manually on the site...And now for continuing we have to add all the required details by chainging optimization to "Yes"...
...then enter our solidity code below where importing "FundMe" like this as we did above code wouldn'it actually work because etherscan doesn't know what "@chainlink/contracts..." means
So we have to copy paste the code from these imports to the top of our contract here...
...Removing these imports and copy pasting the code associated with those files
(i.e `import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; and `import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";) is known as "Flattening"...
And this is an important concept for verifying our smart contracts on platforms like etherscan,
however brownie has a great way to get around this situtaion.
Now after signin to etherscan we can go to API-Keys and create our API-Key Token so that we can verify our brownie smart contracts using it and for that we have to save this "API-Key Token" to ".env" file
after running and checking the `Contract deployed to "0x...."` by copy pasting the account detail on "https://rinkeby.etherscan.io/", we would now get a little green tick mark on "Contracts" Tab
And there now we can see all of the codes of "FundMe.sol", "AggregatorV3Interface.sol" and "SafeMathChainlink.sol" files which are gets downloded from our code base and form github repository of "@chailink/contracts..."
Also we can "read the contracts" and see the various "public variables" and also we can "write contracts" also by connecting to web3 using our "metamask account" which are shown as buttons similar to what we saw in,
while working with "RemixIDE-FundMe.sol" 
"""

"""
Now after updtaing FundMe.sol we need to change our deploy_fund_me() watch above comment...
"""

"""
Now when we open our Ganache UI and run "brownie run scripts/deploy.py" brownie will automatically gets attached to our ganache-local-network and do the two "Transactions" for which we are asked from brownie...
we can check the two in "Transaction" section of Ganache-UI but we can not able to see the deployment details in the "build-->deployments" folder as it was done on the development or temporary network.
So for this we have to create/add a local ganche network in Ethereum(i.e Persistent Network) therefore brownie can retain the deplyments using this command 
"brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=1337" and this will create a network naming `ganache-local` in the Ethereum section of brownie networks.
Now when we run "brownie run scripts/deploy.py --network ganache-local" we will get an error which will tell us that "ganache-local" isn't development network so it's going to go ahead and try to pull from our 
"browine-config.yaml" file but we don't want this we want to actually deploy mock for our "ganche-local" if a mock hasn't been deployed so what we can do is...we can extend our definition of what a development environment is...
If in our "helpful_scripts.py" we cam add a flag(i.e LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"])
But after running this command "brownie run scripts/deploy.py --network ganache-local" we will again run into issue saying-->"sender doesn't have enough funds to send tx. The upfront cost is: 9475280000000000 and the sender's account only has: 0"
as when we look into our "get_account()" in "helpful_scripts.py" which shows this one is also looking directly for the "development" chain, so we have to change "==development" to list "LOCAL_BLOCKCHAIN_ENVIROMENTS" in the "get_account()" and again run the same command...
we again get a `KeyError: "ganache-local"` as haven't updated about the "ganache-local" network in the "brownie-config.yaml" file so on correcting the same we can run the above command correctly in the terminal.
So when we look in our "build-->deployments-->1337(new ChainId for saving the deployments on ganache-local and we can check the same in "Transaction" section of our Ganache-UI)" folder...
IMPORTANT_NOTE:-if we close our Ganache-UI or ganache chain all our contracts related to "ganache-local with ChainID-1337" will be lost so we won't be able to interact with them again, in that case we have to delete the previous folder "1337" in "build-->deployments"...and re-run the same code
"""

"""
Now as we've deployed the "deploy.py" file let's actually write a script to interact with this by creating a new file naming "fund_and_withdraw.py" in "scripts" folder
"""
