const rootUrl = 'http://127.0.0.1:8000';

module.exports = {
  LoginAPI: rootUrl + "/users"+"/login/",
  MessageAPI: rootUrl + "/users" + "/message/",
  AddressAPI: rootUrl + "/users" + "/address/",
  AddressDefaultAPI: rootUrl + "/users" + "/address/" +"default/",
  CategoryAPI: rootUrl + "/food" + "/category/",
  IndexAPI: rootUrl + "/food" +"/index/",
  FoodDetailAPI: rootUrl + "/food" + "/info/",
  FoodAPI: rootUrl + "/food" + "/food/",
  FoodCommentAPI: rootUrl + "/food" + "/comment/",
  SearchAPI: rootUrl + "/food" + "/search/",
  TradeAPI: rootUrl + "/trade" + "/info/",
  OrderAPI: rootUrl + "/trade" + "/order/",
  OrderListAPI: rootUrl + "/trade" + "/order/"+"list/",

}