# 东方Project沙包聚集地机器人
<p>这是东方Project沙包聚集地（以下简称“红群”）的机器人，基于`Python3`编写<br/>
  <i>README待完善</i></p>

<p>
整个框架包含以下三个部分：
</p>
<ul>
<li>QQ登录部分使用的是MyQQ框架的HTTPAPI，官网：
https://www.myqqx.cn/</li>
<li>Bilibili登录和开播部分是自己实现的，直接调用Bilibili的API接口：
https://github.com/SocialSisterYi/bilibili-API-collect</li>
<li>权限管理部分，在程序内部维护了一个Dict实现</li>
</ul>

<p>在使用前，请下载并安装MyQQ，登录机器人QQ号，并修改config.py配置文件</p>
<p>考虑到MyQQ框架并不算很稳定，期待后续能使用更加稳定的框架替换，例如Mirai等</p>
