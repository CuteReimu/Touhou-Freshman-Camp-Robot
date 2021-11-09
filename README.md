# 东方Project沙包聚集地机器人
<p>这是东方Project沙包聚集地（以下简称“红群”）的机器人，基于<b><i>Python3</i></b>编写<br/>
</p>
<ul>
<li>请勿滥用，本项目仅用于学习和测试！不可用于商业用途！</li>
<li>由于使用本项目提供的接口、文档等造成的不良影响和后果与本人和红群无关</li>
<li>由于本项目的特殊性，可能随时停止开发或删档</li>
<li>本项目为开源项目，不接受任何的催单和索取行为</li>
</ul>
<p>
整个框架包含以下三个部分：
</p>
<ul>
<li>QQ登录部分使用的是MyQQ框架的HTTPAPI，官网：
https://www.myqqx.cn/</li>
<li>Bilibili登录和开播部分是自己实现的，直接调用Bilibili的API接口：
https://github.com/SocialSisterYi/bilibili-API-collect</li>
<li>权限管理部分，在程序内部维护了一个<i>dict</i>实现</li>
</ul>

<p>在使用前，请下载并安装MyQQ，登录机器人QQ号，并将config.py.template重命名为config.py并进行配置</p>
<p>考虑到MyQQ框架并不算很稳定，期待后续能使用更加稳定的框架替换，例如Mirai等</p>
