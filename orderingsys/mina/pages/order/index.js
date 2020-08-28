//获取应用实例
var app = getApp();
var api = require("../../config/api.js")
Page({
  data: {
    goods_list: [],
    default_address: null,
    yun_price: "0.00",
    pay_price: "0.00", 
    total_price: "0.00",
    params: null,
    express_address_id: 0,
    post_script: ''
  },
  bindLiuyanInput: function(e) {
    console.log(e.detail.value)
    this.setData({
      post_script: e.detail.value
    });
  },
  onShow: function() {
    var that = this;
    this.getOrderInfo();
  },
  onLoad: function(e) {
    var that = this;
    //console.log(e)
    console.log(JSON.parse(e.data))
    that.setData({
      params: JSON.parse(e.data)
    });
  },
  onShow: function() {
    var that = this;
    this.getOrderInfo();
  },
  createOrder: function(e) {
    wx.showLoading();
    var that = this;
    wx.request({
      url: api.OrderAPI,
      data: {
        type: this.data.params.type,
        goods: this.data.params.goods,
        post_script: this.data.post_script,
        order_mount: this.data.params.totalPrice,
        address: this.data.express_address_id
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        console.log(res)
      },
    })
    wx.navigateTo({
      url: "/pages/my/order_list"
    });
  },
  addressSet: function() {
    wx.navigateTo({
      url: "/pages/my/addressSet?id=0"
    });
  },
  selectAddress: function() {
    wx.navigateTo({
      url: "/pages/my/addressList"
    });
  },
  getOrderInfo: function() {
    var that = this;
    //console.log(this.data.params.goods)
    wx.request({
      url: api.OrderAPI,
      data: {
        type: this.data.params.type,
        goods: JSON.stringify(this.data.params.goods)
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        console.log(res.data)
        var data = {
          yun_price:0,
          total_price:0,
        };
        for (var i = res.data.length-1; i >=0 ; i--) {
          data.yun_price = data.yun_price + res.data[i].yun_price,
          data.total_price = data.total_price + res.data[i].price * res.data[i].nums[i].nums
        }
        console.log(data.yun_price)
        console.log(data.total_price)
        that.setData({
          goods_list: res.data,
          default_address: res.data,
          yun_price: data.yun_price,
          pay_price: data.total_price,
          total_price: data.total_price + data.yun_price,
        });

        if (that.data.default_address) {
          that.setData({
            express_address_id: res.data[0].userAddress[0].id
          });
        }
      },
    })
  }
});