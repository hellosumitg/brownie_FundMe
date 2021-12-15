from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
# As this gonna resemble the "eth_to_usd" "price_feed" it actually has only 8 decimals because "get_price()" in "FundMe.sol" has only 8 Decimal places see it below
"""function getPrice() public view returns (uint256) {
        /* removing this part
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        as we already declared above globally and do the exact same thing but in our constructor() right when we deploy this contract */
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }
"""
STARTING_PRICE = 200000000000


def get_account():
    # if network.show_active() == "development":
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    # for checking on the mainnet-fork network we have to use below modified code
    # Also we have to create "mainnet-fork" network in brownie also using this command "brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1:8545 fork='https://mainnet.infura.io/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie port=8545"
    # but using this infura account would lead us to some error. So intead of this "Infura" we use "Alchemy" by signing it up and create app on Ethereum Mainnet and use this below code to create the "mainnet-fok-dev" network
    # "brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1:8545 fork='https://eth-mainnet.alchemyapi.io/v2/5qBGZnv2i5MsVdjnPGG9-zXh5sXNxfbO' accounts=10 mnemonic=brownie port=8545"
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
        # it says if network is in LOCAL_BLOCKCHAIN_ENVIRONMENTS(i.e list) phase return account at [0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
        # instead of 2000000000000000000000 we can write `Web3.toWei(2000, "ether")`
    print("Mocks Deployed!")
