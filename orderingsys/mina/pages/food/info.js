//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');
var api = require("../../config/api.js");
var auth = require("../../config/auth.js");

Page({
  data: {
    autoplay: true,
    interval: 3000,
    duration: 1000,
    swiperCurrent: 0,
    hideShopPopup: true,
    buyNumber: 1,
    buyNumMin: 1,
    buyNumMax: 1,
    canSubmit: false, //  选中时候是否允许加入购物车
    shopCarInfo: {},
    shopType: "addShopCar", //购物类型，加入购物车或立即购买，默认为加入购物车,
    id: 0,
    shopCarNum: 0,
    buyNowNumber: 0,
    commentCount: 0,
    info: [],
  },
  onLoad: function(e) {
    var that = this;
    console.log(e)
    wx.request({
      url: api.FoodDetailAPI + e.id + '/',
      data: e,
      method: 'GET',
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        
        console.log(res.data)
        that.setData({ 
          info: res.data,
          commentList: res.data.foodcomment,
          buyNumMax: res.data.status,
          shopCarNum: res.data.shoop_cart_num[0].nums
        })
        WxParse.wxParse('article', 'html', this.data.info.summary, that, 5);
        console.log(this.data.info)
      },

    })

  },
  goShopCar: function() {
    var result = auth.is_login()
    console.log(result)
    if(!result){
      return
    }
    wx.reLaunch({
      url: "/pages/cart/index"
    });
  },
  toAddShopCar: function() {
    var result = auth.is_login()
    console.log(result)
    if (!result) {
      return
    }
    this.setData({
      shopType: "addShopCar"
    });
    this.bindGuiGeTap();
  },
  tobuy: function() {
    var result = auth.is_login()
    console.log(result)
    if (!result) {
      return
    }
    this.setData({
      shopType: "tobuy"
    });
    this.bindGuiGeTap();
  },
  addShopCar: function(e) {
    var that = this
    wx.request({
      url: api.TradeAPI,
      data: {
        nums: this.data.buyNumber,
        food: e.currentTarget.dataset.id
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'POST',
      dataType: 'json',
      success: (res) => {
        console.log(res.data)
        that.setData({
          shopCarNum: res.data.nums
        })
      },
    })
    this.setData({
      shopCarNum: this.data.buyNumber,
      buyNumber: 1,
    })
    wx.navigateTo({
      url: "/pages/food/info?id=" + e.currentTarget.dataset.id,
    });
    //console.log(this.data.buyNumber)
  },
  buyNow: function(e) {
    this.setData({
      buyNowNumber: this.data.buyNumber,
      buyNumber: 1,
    })
    var list = this.data.info;
    console.log(this.data.info)
    var totalPrice = 0.00;
    totalPrice = totalPrice + parseFloat(list.price) * e.currentTarget.dataset.nums + parseFloat(list.yun_price);
    console.log(this.data.info)
    var data = {
      type: "cart",
      goods: [],
      totalPrice: totalPrice
    };
      data['goods'].push({
        "id": e.currentTarget.dataset.id,
        "nums": e.currentTarget.dataset.nums,
      });
    //console.log(this.data.buyNumber)
    wx.navigateTo({
      url: "/pages/order/index?data=" + JSON.stringify(data)
    });
  },
  /**
   * 规格选择弹出框
   */
  bindGuiGeTap: function() {
    this.setData({
      hideShopPopup: false
    })
  },
  /**
   * 规格选择弹出框隐藏
   */
  closePopupTap: function() {
    this.setData({
      hideShopPopup: true,
      buyNumber: 1,
    })
  },
  numJianTap: function() {
    if (this.data.buyNumber <= this.data.buyNumMin) {
      return;
    }
    var currentNum = this.data.buyNumber;
    currentNum--;
    this.setData({
      buyNumber: currentNum
    });
  },
  numJiaTap: function() {
    if (this.data.buyNumber >= this.data.buyNumMax) {
      return;
    }
    var currentNum = this.data.buyNumber;
    currentNum++;
    this.setData({
      buyNumber: currentNum
    });
  },
  //事件处理函数
  swiperchange: function(e) {
    this.setData({
      swiperCurrent: e.detail.current
    })
  }
}); 