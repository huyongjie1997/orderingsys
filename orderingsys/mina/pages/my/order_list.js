var app = getApp();
var api = require("../../config/api.js")
Page({
  data: {
    order_list: [],
    statusType: ["待付款", "待发货", "待确认", "待评价", "已完成", "已关闭"],
    status: ["-8", "-7", "-6", "-5", "1", "0"],
    currentType: 0,
    tabClass: ["", "", "", "", "", ""]
  },
  statusTap: function(e) {
    var curType = e.currentTarget.dataset.index;
    this.setData({
      currentType: curType
    });
    this.getPayOrder();
  },
  orderDetail: function(e) {
    wx.navigateTo({
      url: "/pages/my/order_info?order_sn=" + e.currentTarget.dataset.id
    })
  },
  onLoad: function(options) {
    // 生命周期函数--监听页面加载
  },
  onShow: function() {
    this.getPayOrder();
  },
  orderCancel: function(e) {
    this.orderOps(e.currentTarget.dataset.id, "cancel", "确定取消订单？");
  },
  getPayOrder: function() {
    var that = this;
    wx.request({
      url: api.OrderListAPI,
      data: {
        status: that.data.status[that.data.currentType]
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        var resp = res.data;
        //console.log(resp)
        if (resp.statu == false) {
          app.alert({
            "content": resp.msg
          });
          return;
        }

        that.setData({
          order_list: resp
        });
      }
    })
  },
  /*toPay: function (e) {
    var that = this;
    wx: request({
      //url: app.buildUrl("/order/pay"),
      url:'',
      header: app.getRequestHeader(),
      method: 'POST',
      data: {
        order_sn: e.currentTarget.dataset.id
      },
      success: function (res) {
        var resp = res.data;
        if (resp.code != 200) {
          app.alert({ "content": resp.msg });
          return;
        }
        var pay_info = resp.data.pay_info;
        wx.requestPayment({
          'timeStamp': pay_info.timeStamp,
          'nonceStr': pay_info.nonceStr,
          'package': pay_info.package,
          'signType': 'MD5',
          'paySign': pay_info.paySign,
          'success': function (res) {
          },
          'fail': function (res) {
          }
        });
      }
    });
  },*/
  orderConfirm: function(e) {
    this.orderOps(e.currentTarget.dataset.id, "confirm", "确定收到？");
  },
  orderComment: function(e) {
    wx.navigateTo({
      url: "/pages/my/comment?order_sn=" + e.currentTarget.dataset.id
    })
  },
  orderOps: function(order_sn, act, msg) {
    var that = this;
    var params = {
      "content": msg,
      "cb_confirm": function() {
        wx.request({
          url: api.OrderListAPI,
          method: 'POST',
          data: {
            order_sn: order_sn,
            act: act
          },
          header: {
            Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
          },
          dataType: 'json',
          responseType: 'text',
          success: function(res) {
            console.log(res.data)
            var resp = res.data;
            app.alert({
              "content": resp.msg
            });
            if (resp.status == 200) {
              that.getPayOrder();
            }
          }
        })
      }
    };
    app.tip(params);
  }
});