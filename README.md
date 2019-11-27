### climbworm
批量获取特定页面资源
### wbimgs
批量获取m.weibo.cn用户微博页面的图片，由scrapy框架自动设置目录和文件名

### 常用命令（Scrapy tool）
####Usage  
>scrapy <command> [options] [args]  
####Available commands 
  >bench        &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Run quick benchmark test  
  fetch         &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Fetch a URL using the Scrapy downloader  
  genspider     &#8194;&#8194;&#8194;&#8194;Generate new spider using pre-defined templates  
  runspider     &#8194;&#8194;&#8194;&#8194;Run a self-contained spider (without creating a project)  
  settings      &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Get settings values  
  shell         &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Interactive scraping console  
  startproject  &#8194;&#8194;&#8194;Create new project  
  version       &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Print Scrapy version  
  view          &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;Open URL in browser, as seen by Scrapy  

  >[ more ]     &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;More commands available when run from project directory  
Use "scrapy <command> -h" to see more info about a command
####创建项目
 >scrapy startproject myproject
####创建一个新的spider
>scrapy genspider mydomain mydomain.com
####运行spider
>scrapy crawl \<spidername\>
####查看命令帮助
>scrapy \<command\> -h  
>scrapy -h 查看所有命令帮助
####全局命令
>startproject  
settings  
runspider  
shell  
fetch  
view  
version  
####项目命令（project-only）
>crawl  
check  
list  
edit  
parse  
genspider  
deploy  
bench  