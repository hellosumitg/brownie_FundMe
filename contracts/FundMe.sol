// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        /* removing this part
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        as we already declared above globally and do the exact same thing but in our constructor() right when we deploy this contract */
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        /* removing this part
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        as we already declared above globally and do the exact same thing but in our constructor() right when we deploy this contract */
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // 1000000000
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}

/*
Now, above we had seen working with "Rinkeby Test net", whose steps are written in the "deploy.py" 
however, we always want to deploy it to our own local blockchains or brownies local built-in development chain so we can test a lot more quicker using ganache-cli, so that we can write some tests 
we have some issue here:-
1. Our FundMe.sol contract currently has an address hard-coded above(i.e 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e) to work with the rinkeby chain so in fact the way it's written right now,
   it's going to be hard to work with anyother chain other than "rinkeby chain".
2. These "priceFeed contracts" don't exist on a local ganache chain or a ganache chain that brownie spins up.
   
So, there are two ways for getting around this by doing:-
1. Forking(i.e by working on a forked simulated chain) 
OR
2. Mocking(i.e by deploying to a Mock contract(i.e a fake price feed contract) on our local ganache development chain.
   deplpoying mocks is a common design pattern used across all software engineering industries and what it applies doing is deploying a fake version of something and interacting with it as if it's real.

So, again if we run "brownie run scripts/deploy.py" and don't set the network we're going to actually have a default spinning up a ganache chain and it's even going to try to verify 
but it's going to run into an issue because we can't verify on a ganache chian so we need to check these above listed couple of issues to solve this to work on a ganache chain
So, the first thing we want to do is we need to parameterize our "FundMe.sol" smart contract so as to remove the hard-coded addrress part(i.e 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e) in here.
So we can do this to solve, that right when we deploy this contract we'll tell it what price feed address it should use right when we call deploy function here instead of having it hard coded...
by adding this in constructor() as a input parameter "constructor(address _priceFeed) so whatever inoput parameter we use here is going to be our global "_pricefeed" address
So, instead of us creating these "AggregatorV3Interface contracts" 
(i.e AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e) 
right in the functions here we're just going to create a global one so we'll say
"AggregatorV3Interface public priceFeed;" and for rest watch above in code...
After making some changes above we can check by running "brownie complie"

*/
