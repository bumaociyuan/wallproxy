# -*- coding: utf-8 -*-
# 是否使用ini作为配置文件，0不使用
ini_config = 1
# 监听ip
listen_ip = '127.0.0.1'
# 监听端口
listen_port = 8086
# 是否使用通配符证书
cert_wildcard = 1
# 更新PAC时也许还没联网，等待tasks_delay秒后才开始更新
tasks_delay = 0
# WEB界面是否对本机也要求认证
web_authlocal = 0
# 登录WEB界面的用户名
web_username = 'admin'
# 登录WEB界面的密码
web_password = 'admin'
# 全局代理
global_proxy = None
# URLFetch参数
fetch_keepalive = 1
debuglevel = 0
check_update = 0

def config():
    Forward, set_dns, set_resolve, set_hosts, check_auth, redirect_https = import_from('util')
    YOUKU = Forward('hosts://api.youku.com:80')
    RAW_FORWARD = FORWARD = Forward()
    set_dns('168.95.1.1')
    set_resolve('talk.google.com talkx.l.google.com .youtube.com .facebook.com .googlevideo.com .dropbox.com .dropboxusercontent.com')
    google_sites = ('.appspot.com', '.google.com', '.google.com.hk', '.googlecode.com', '.googleusercontent.com', '.googlegroups.com', '.google-analytics.com', '.gstatic.com', '.googleapis.com', '.blogger.com', '.ggpht.com', 'golang.org', 'goo.gl', 'googledrive.com', '.googledrive.com')
    google_hosts = '2.2.2.2 www.google.com www.google.com.hk 203.66.124.173 202.39.143.94 203.66.124.237 103.25.178.59 203.66.124.168 218.176.242.109 218.176.242.236 218.176.242.49 218.176.242.45 203.211.0.59 203.66.124.241 203.66.124.247 61.219.131.227 61.219.131.216 218.176.242.113 203.66.124.182 218.176.242.158 210.61.221.103 61.219.131.231 218.176.242.88 61.219.131.232 210.61.221.108 61.219.131.118 218.176.242.232 103.25.178.42 210.61.221.123 210.61.221.153 202.39.143.109 202.39.143.108 203.66.124.172 218.176.242.221 202.39.143.103 210.61.221.183 218.176.242.119 202.39.143.104 61.219.131.221 178.45.251.94 210.61.221.109 218.176.242.108 218.176.242.55 202.39.143.30 203.211.0.25 210.61.221.99 210.61.221.119 203.211.0.40 210.61.221.158 218.176.242.30 203.211.0.29 203.66.124.212 103.25.178.38 61.219.131.222 218.176.242.162 61.219.131.103'
    set_hosts(google_sites, google_hosts)
    set_hosts('www.youtube.com upload.youtube.com', google_hosts)

    from plugins import misc; misc = install('misc', misc)
    PAGE = misc.Page('page.html')
    redirect_rules = misc.Redirects(# -*- coding:utf-8 -*-
[
    # 修复userscripts链接
    (r'^https?://userscripts\.org(?::8080)?/', 'http://userscripts-mirror.org/'),
    # 禁止广告引流
    (r'^https?://click\.union\.jd\.com\/.+?&to=([^&]+)(?:&.+)?', r'\1'),
    # 解决WayOS劫持流量插入广告
    #(r'(?i).+?\.unionabcd\.com[:/].+?&surl=([^&]+).*', r'http://\1/?'),
    # 解决部分运营商劫持流量插入广告
    #(r'^http://\d+(?:\.\d+){3}(?::\d+)?/redirect\d+\.php\?desturl=([^&]+)&augid1=.+?julyid=.*', r'\1'),
]
)

    from plugins import paas; paas = install('paas', paas)
    GAE = paas.GAE(appids=['goblin1alchemist', 'zx00000000000', 'zx1982az', 'zx444441444', 'zx44444444', 'zx4654x', 'zx555555555', 'zx666666666', 'zx77777777', 'zx888888887'], listen='8087', path='/fetch.py', scheme='https', hosts=google_hosts, bufsize=65536, max_threads=3, fetch_mode=1)

    PacFile, RuleList, HostList = import_from('pac')
    def apnic_parser(data):
        from re import findall
        return '\n'.join(findall(r'(?i)\|cn\|ipv4\|((?:\d+\.){3}\d+\|\d+)\|', data))
    forcehttps_sites = RuleList('http://*.appspot.com/ \n http://*.google.com/ \n http://*.google.com.hk/ \n http://*.googlecode.com/ \n http://*.googleusercontent.com/ \n http://*.blogger.com/ \n http://www.youtube.com/ \n http://goo.gl/ \n http://googledrive.com/ \n http://*.googledrive.com/ \n @@http://books.google.com/ \n @@http://translate.google.com/ \n @@http://scholar.google.com/ \n @@http://feedproxy.google.com/ \n @@http://fusion.google.com/ \n @@http://picasa.google.com/ \n @@http://*pack.google.com/ \n @@http://*android.clients.google.com/ \n @@http://wenda.google.com.hk/ \n @@http://www.google.com*/imgres? \n @@http://www.google.com*/translate_t? \n @@http://www.google.com/analytics/ \n @@http://wiki.*.googlecode.com/ \n @@http:/// \n @@http://website.*.googlecode.com/ \n @@http://www.google.com*/custom? \n @@http://www.google.com/dl/ \n @@http://www.google.com/drive/ \n @@http://www.google.com*/alerts?')
    autorange_rules = RuleList('||c.youtube.com \n ||atm.youku.com \n ||googlevideo.com \n http*://av.vimeo.com/ \n http*://smile-*.nicovideo.jp/ \n http*://video.*.fbcdn.net/ \n http*://s*.last.fm/ \n http*://x*.last.fm/ \n ||x.xvideos.com \n ||edgecastcdn.net \n ||d.rncdn3.com \n http*://cdn*.public.tube8.com/ \n http*://videos.flv*.redtubefiles.com/ \n http*://cdn*.public.extremetube.phncdn.com/ \n http*://cdn*.video.pornhub.phncdn.com/ \n ||mms.vlog.xuite.net \n http*://vs*.thisav.com/ \n http*://archive.rthk.hk/ \n http*://video*.modimovie.com/ \n http*://v*.cache*.c.docs.google.com/ \n /^https?:\\/\\/[^\\/]+\\/[^?]+\\.(?:cab|f4v|flv|hlv|m4v|mp4|mp3|ogg|avi|msi|exe|zip|iso|ipa|rar|bz2|gz|xz|deb|dmg|3gp)(?:$|\\?)/ \n http*://*.googleusercontent.com/videoplayback? \n @@/^https?:\\/\\/manifest\\.googlevideo\\.com\\/api\\//')
    _GAE = GAE; GAE = lambda req: _GAE(req, autorange_rules.match(req.url, req.proxy_host[0]))
    import re; useragent_match = re.compile('(?i)mobile').search
    useragent_rules = RuleList('||twitter.com')
    withgae_sites = RuleList('||c.docs.google.com \n ||translate.google.com \n http*://books.google.com/books?id= \n http*://*.googleusercontent.com/videoplayback?')
    notruehttps_sites = HostList('.docs.google.com translate.google.com books.google.com')
    truehttps_sites = HostList('.appspot.com .google.com .google.com.hk .googlecode.com .googleusercontent.com .googlegroups.com .google-analytics.com .gstatic.com .googleapis.com .blogger.com .ggpht.com goo.gl googledrive.com .googledrive.com')
    crlf_rules = RuleList('/^https?:\\/\\/[^\\/]+\\.c\\.youtube\\.com\\/liveplay\\?/ \n /^https?:\\/\\/upload\\.youtube\\.com\\// \n /^https?:\\/\\/www\\.youtube\\.com\\/upload\\//')
    hosts_rules = RuleList(' \n ||appspot.com \n ||google.com \n ||google.com.hk \n ||googlecode.com \n ||googleusercontent.com \n ||googlegroups.com \n ||google-analytics.com \n ||gstatic.com \n ||googleapis.com \n ||blogger.com \n ||ggpht.com \n ||golang.org \n ||goo.gl \n ||googledrive.com \n ||googledrive.com')
    unparse_netloc = import_from('utils')
    def build_fake_url(scheme, host):
        if scheme == 'https' and host[1] != 80 or host[1] % 1000 == 443:
            scheme, dport = 'https', 443
        else: scheme, dport = 'http', 80
        return '%s://%s/' % (scheme, unparse_netloc(host, dport))
    _HttpsFallback = (GAE,)
    nofallback_rules = RuleList('/^https?:\\/\\/(?:[\\w-]+|127(?:\\.\\d+){3}|10(?:\\.\\d+){3}|192\\.168(?:\\.\\d+){2}|172\\.(?:1[6-9]|2\\d|3[01])(?:\\.\\d+){2}|\\[.+?\\])(?::\\d+)?\\//')
    def FORWARD(req):
        if req.proxy_type.endswith('http'):
            if nofallback_rules.match(req.url, req.proxy_host[0]):
                return RAW_FORWARD(req)
            return RAW_FORWARD(req, GAE)
        url = build_fake_url(req.proxy_type, req.proxy_host)
        if nofallback_rules.match(url, req.proxy_host[0]):
            return RAW_FORWARD(req)
        return RAW_FORWARD(req, _HttpsFallback)

    rulelist = (
        (['string:///^https?:\\/\\/.*?(?:youku|qiyi|iqiyi|letv|sohu|ku6|ku6cdn|pps)\\.(?:com|tv)\\/crossdomain\\.xml$/'], 'PROXY API.YOUKU.COM:80'),
        (['https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt', 'userlist.ini'], 'PROXY *:8087;DIRECT'),
    )
    iplist = (
        (['203.66.124.177', '203.66.124.172', '60.199.175.153', '202.39.143.114', '74.125.200.104', '74.125.68.17', '203.66.124.236', '202.39.143.113', '74.125.130.38', '106.162.192.152', '106.162.198.123', '173.194.117.172', '111.168.255.182', '218.189.25.173', '61.219.131.94', '64.233.187.18', '203.165.13.238', '106.162.198.109', '203.165.14.237', '203.165.14.245', '218.176.242.152', '218.189.25.166', '193.120.166.113', '64.15.115.118', '64.15.115.179', '208.117.224.244', '94.40.70.46', '64.15.113.205', '80.228.65.167', '121.78.74.80', '64.233.187.136', '118.174.27.109', '194.78.99.55', '178.60.128.53', '173.194.117.72', '208.117.228.216', '64.15.112.183', '208.117.233.87', '85.182.250.24', '64.15.115.187', '64.233.160.31', '106.162.192.178', '64.15.115.245', '64.15.115.35', '208.117.231.119', '64.233.181.114', '208.117.224.108', '64.15.126.134', '74.125.232.204', '94.40.70.49', ''], 'PROXY *:8087;DIRECT'),
    )
    PacFile(rulelist, iplist, ['proxy.pac'], ['DIRECT', 'DIRECT', 'DIRECT'])

    rulelist = (
        (RuleList(['string:///^https?:\\/\\/.*?(?:youku|qiyi|iqiyi|letv|sohu|ku6|ku6cdn|pps)\\.(?:com|tv)\\/crossdomain\\.xml$/']), YOUKU),
        (RuleList(['https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt', 'userlist.ini']), GAE),
    )
    httpslist = (
        (rulelist[0][0], YOUKU),
        (rulelist[1][0], None),
    )
    IpList, makeIpFinder = import_from('pac')
    iplist = (
        (IpList(['203.66.124.177', '203.66.124.172', '60.199.175.153', '202.39.143.114', '74.125.200.104', '74.125.68.17', '203.66.124.236', '202.39.143.113', '74.125.130.38', '106.162.192.152', '106.162.198.123', '173.194.117.172', '111.168.255.182', '218.189.25.173', '61.219.131.94', '64.233.187.18', '203.165.13.238', '106.162.198.109', '203.165.14.237', '203.165.14.245', '218.176.242.152', '218.189.25.166', '193.120.166.113', '64.15.115.118', '64.15.115.179', '208.117.224.244', '94.40.70.46', '64.15.113.205', '80.228.65.167', '121.78.74.80', '64.233.187.136', '118.174.27.109', '194.78.99.55', '178.60.128.53', '173.194.117.72', '208.117.228.216', '64.15.112.183', '208.117.233.87', '85.182.250.24', '64.15.115.187', '64.233.160.31', '106.162.192.178', '64.15.115.245', '64.15.115.35', '208.117.231.119', '64.233.181.114', '208.117.224.108', '64.15.126.134', '74.125.232.204', '94.40.70.49', '']), GAE),
    )
    findHttpProxyByIpList = makeIpFinder(iplist, [FORWARD, FORWARD, FORWARD])
    findHttpsProxyByIpList = makeIpFinder(iplist, [FORWARD, FORWARD, FORWARD])

    def find_gae_handler(req):
        proxy_type = req.proxy_type
        host, port = req.proxy_host
        if proxy_type.endswith('http'):
            url = req.url
            if useragent_match(req.headers.get('User-Agent','')) and useragent_rules.match(url, host):
                req.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
            if withgae_sites.match(url, host):
                return GAE
            needhttps = req.scheme == 'http' and forcehttps_sites.match(url, host) and req.content_length == 0
            if needhttps and getattr(req, '_r', '') != url:
                req._r = url
                return redirect_https
            handler = redirect_rules(req)
            if handler: return handler
            if crlf_rules.match(url, host):
                req.crlf = 1
                return FORWARD
            if not needhttps and hosts_rules.match(url, host):
                return FORWARD
            return GAE
        if notruehttps_sites.match(host): return
        if truehttps_sites.match(host): return FORWARD
    paas.data['GAE_server'].find_handler = find_gae_handler

    def find_proxy_handler(req):
        proxy_type = req.proxy_type
        host, port = req.proxy_host
        if proxy_type.endswith('http'):
            url = req.url
            if useragent_match(req.headers.get('User-Agent','')) and useragent_rules.match(url, host):
                req.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
            if withgae_sites.match(url, host):
                return GAE
            needhttps = req.scheme == 'http' and forcehttps_sites.match(url, host) and req.content_length == 0
            if needhttps and getattr(req, '_r', '') != url:
                req._r = url
                return redirect_https
            handler = redirect_rules(req)
            if handler: return handler
            if crlf_rules.match(url, host):
                req.crlf = 1
                return FORWARD
            if not needhttps and hosts_rules.match(url, host):
                return FORWARD
            for rule,target in rulelist:
                if rule.match(url, host):
                    return target
            return findHttpProxyByIpList(host)
        if notruehttps_sites.match(host): return
        if truehttps_sites.match(host): return FORWARD
        url = build_fake_url(proxy_type, (host, port))
        for rule,target in httpslist:
            if rule.match(url, host):
                return target
        return findHttpsProxyByIpList(host)
    return find_proxy_handler
