pragma solidity 0.4.17;


import 'trading/Order.sol';
import 'reporting/IMarket.sol';


contract ITrade {
    function publicBuy(IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) external returns (bytes32);
    function publicSell(IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) external returns (bytes32);
    function publicTrade(Order.TradeDirections _direction, IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) external returns (bytes32);
    function publicTakeBestOrder(Order.TradeDirections _direction, IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) external returns (uint256);
    function trade(address _sender, Order.TradeDirections _direction, IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) internal returns (bytes32);
    function fillBestOrder(address _sender, Order.TradeDirections _direction, IMarket _market, uint8 _outcome, uint256 _fxpAmount, uint256 _price, uint256 _tradeGroupID) internal returns (uint256);
}
