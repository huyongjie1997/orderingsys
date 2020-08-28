//获取应用实例
var commonCityData = require('../../utils/city.js');
var api = require("../../config/api.js")

var app = getApp();
Page({
  data: {
    info: [],
    provinces: [],
    citys: [],
    districts: [],
    selProvince: '请选择',
    selCity: '请选择',
    selDistrict: '请选择',
    selProvinceIndex: 0,
    selCityIndex: 0,
    selDistrictIndex: 0,
  },
  onLoad: function(e) {
    //var that = this;
    this.setData({
      id: e.id
    });
    this.initCityData(1);
  },
  onShow: function() {
    this.getInfo();
  },
  //初始化城市数据
  initCityData: function(level, obj) {
    if (level == 1) {
      var pinkArray = [];
      for (var i = 0; i < commonCityData.cityData.length; i++) {
        pinkArray.push(commonCityData.cityData[i].name);
      }
      this.setData({
        provinces: pinkArray
      });
    } else if (level == 2) {
      var pinkArray = [];
      var dataArray = obj.cityList
      for (var i = 0; i < dataArray.length; i++) {
        pinkArray.push(dataArray[i].name);
      }
      this.setData({
        citys: pinkArray
      });
    } else if (level == 3) {
      var pinkArray = [];
      var dataArray = obj.districtList
      for (var i = 0; i < dataArray.length; i++) {
        pinkArray.push(dataArray[i].name);
      }
      this.setData({
        districts: pinkArray
      });
    }
  },
  bindPickerProvinceChange: function(event) {
    var selIterm = commonCityData.cityData[event.detail.value];
    this.setData({
      selProvince: selIterm.name,
      selProvinceIndex: event.detail.value,
      selCity: '请选择',
      selCityIndex: 0,
      selDistrict: '请选择',
      selDistrictIndex: 0
    });
    this.initCityData(2, selIterm);
  },
  bindPickerCityChange: function(event) {
    var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[event.detail.value];
    this.setData({
      selCity: selIterm.name,
      selCityIndex: event.detail.value,
      selDistrict: '请选择',
      selDistrictIndex: 0
    });
    this.initCityData(3, selIterm);
  },
  bindPickerChange: function(event) {
    var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[event.detail.value];
    if (selIterm && selIterm.name && event.detail.value) {
      this.setData({
        selDistrict: selIterm.name,
        selDistrictIndex: event.detail.value
      })
    }
  },
  bindCancel: function() {
    wx.navigateBack({});
  },
  bindSave: function(e) {
    var that = this;
    var nickname = e.detail.value.nickname;
    var address = e.detail.value.address;
    var mobile = e.detail.value.mobile;

    if (nickname == "") {
      app.tip({
        content: '请填写联系人姓名~~'
      });
      return
    }
    if (mobile == "") {
      app.tip({
        content: '请填写手机号码~~'
      });
      return
    }
    if (this.data.selProvince == "请选择") {
      app.tip({
        content: '请选择地区~~'
      });
      return
    }
    if (this.data.selCity == "请选择") {
      app.tip({
        content: '请选择地区~~'
      });
      return
    }
    var city_id = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].id;
    var district_id;
    if (this.data.selDistrict == "请选择" || !this.data.selDistrict) {
      district_id = 1;
    } else {
      district_id = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[this.data.selDistrictIndex].id;
    }
    if (address == "") {
      app.tip({
        content: '请填写详细地址~~'
      });
      return
    }
    wx.request({
      url: api.AddressAPI,
      data: {
        id: that.data.id,
        province_id: commonCityData.cityData[this.data.selProvinceIndex].id,
        province_str: that.data.selProvince,
        city_id: city_id,
        city_str: that.data.selCity,
        area_id: district_id,
        area_str: that.data.selDistrict,
        signer_name: nickname,
        address: address,
        singer_mobile: mobile,
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: "POST",
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        var resp = res.data;
        console.log(resp)
        if (resp.status == false) {
          app.alert({
            "content": resp.msg
          });
          return;
        }
        // 跳转
        wx.navigateBack({});
      },
    })
  },
  deleteAddress: function(e) {

  },
  getInfo: function() {
    var that = this;
    if (this.data.id < 1) {
      return;
    }
    var id = this.data.id
    console.log(id)
    wx.request({
      url: api.AddressAPI,
      data: {
        id: id
      },
      header: {
        Authorization: app.globalData.userInfo ? app.globalData.userInfo.token : null
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function(res) {
        //if (resp.code != 200) {
        //  app.alert({
        //  "content": resp.msg
        // });
        // return;
        // }
        console.log(res.data)
        that.setData({
          info: res.data,
          selProvince: res.data[0].province_str ? res.data[0].province_str : "请选择",
          selCity: res.data[0].city_str ? res.data[0].city_str : "请选择",
          selDistrict: res.data[0].area_str ? res.data[0].area_str : "请选择"
        });
        console.log(that.data.info)
      }
    })
  }
});