//获取应用实例
var api = require("../../config/api.js")
var app = getApp();
Page({
  data: {},
  selectTap: function(e) {
    //从商品详情下单选择地址之后返回
    var that = this;
    wx.request({
      url: api.AddressAPI,
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'PUT',
      data: {
        id: e.currentTarget.dataset.id,
        act: 'default'
      },
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        console.log(res.data)
        that.setData({
          list: res.data
        });
      },
    })
    wx.navigateBack({});
  },
  addessSet: function(e) {
    wx.navigateTo({
      url: "/pages/my/addressSet?id=" + e.currentTarget.dataset.id
    })
  },
  onShow: function() {
    var that = this;
    wx.request({
      url: api.AddressAPI,
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        console.log(res.data)
        that.setData({
          addressList: res.data,
        });
      }
    })
  }
});