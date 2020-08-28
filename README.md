# orderingsys

mina为小程序代码

ordering为后项目代码

orderingsys_yml为docker-compose文件（用于整个项目的启动）

配置类文件（Dockerfile文件、gunnicorn.py部署、requirements.txt、start.sh启动文件）

项目名称：微信小程序订餐系统

开发工具：
  Navicat 、MySQL、Pycharm、微信开发者工具、Python3.7、Django rest framework
  
项目描述：
  项目由小程序和后台项目文件组成。小程序有1个api.js管理总的URL，为6个pages管理不同的页面和发送请求，获取数据。后台项目则是设计项目所需的数据模型以及对数据的序列化封装，和接收数据的校验保存等业务逻辑的操作。
  
项目总结：
  小程序的开发需要有较高的数据格式封装要求，以便于数据在页面之间的传递和请求发送。
