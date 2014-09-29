# -*- coding: utf-8 -*-
# 是否使用ini作为配置文件，0不使用
ini_config = 1411960135
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
check_update = 0

def config():
    Forward, set_dns, set_resolve, set_hosts, check_auth, redirect_https = import_from('util')
    RAW_FORWARD = FORWARD = Forward()
    set_dns('168.95.1.1')
    set_resolve('talk.google.com talkx.l.google.com .youtube.com .facebook.com .googlevideo.com')
    google_sites = ('.appspot.com', '.google.com', '.google.com.hk', '.googlecode.com', '.googleusercontent.com', '.googlegroups.com', '.google-analytics.com', '.gstatic.com', '.googleapis.com', '.blogger.com', '.ggpht.com', 'golang.org')
    google_hosts = 'www.google.com www.google.com.hk mail.google.com www.google.at www.google.es www.google.ca www.google.com.mx www.google.com.pa www.google.gl www.google.com.gt www.google.com.bz www.google.com.sv www.google.hn'
    set_hosts(google_sites, google_hosts)
    set_hosts('www.youtube.com upload.youtube.com', google_hosts)

    from plugins import misc; misc = install('misc', misc)
    PAGE = misc.Page('page.html')

    from plugins import paas; paas = install('paas', paas)
    GAE = paas.GAE(appids=['goblin1alchemist', 'zx00000000000', 'zx1982az', 'zx444441444', 'zx44444444', 'zx4654x', 'zx555555555', 'zx666666666', 'zx77777777', 'zx888888887'], listen='8087', path='/fetch.py', scheme='https', hosts=google_hosts, max_threads=3, fetch_mode=1)

    PacFile, RuleList, HostList = import_from('pac')
    def apnic_parser(data):
        from re import findall
        return '\n'.join(findall(r'(?i)\|cn\|ipv4\|((?:\d+\.){3}\d+\|\d+)\|', data))
    forcehttps_sites = RuleList('http://*.appspot.com/ \n http://*.google.com/ \n http://*.google.com.hk/ \n http://*.googlecode.com/ \n http://*.googleusercontent.com/ \n http://*.blogger.com/ \n http://www.youtube.com/ \n @@http://books.google.com/ \n @@http://translate.google.com/ \n @@http://scholar.google.com/ \n @@http://feedproxy.google.com/ \n @@http://fusion.google.com/ \n @@http://picasa.google.com/ \n @@http://*pack.google.com/ \n @@http://*android.clients.google.com/ \n @@http://wenda.google.com.hk/ \n @@http://www.google.com*/imgres? \n @@http://www.google.com*/translate_t? \n @@http://www.google.com/analytics/ \n @@http://wiki.*.googlecode.com/ \n @@http:/// \n @@http://website.*.googlecode.com/ \n @@http://www.google.com*/custom? \n @@http://www.google.com/dl/ \n @@http://www.google.com/drive/ \n @@http://www.google.com*/alerts?')
    autorange_rules = RuleList('||c.youtube.com \n ||atm.youku.com \n ||googlevideo.com \n http*://av.vimeo.com/ \n http*://smile-*.nicovideo.jp/ \n http*://video.*.fbcdn.net/ \n http*://s*.last.fm/ \n http*://x*.last.fm/ \n ||x.xvideos.com \n ||edgecastcdn.net \n ||d.rncdn3.com \n http*://cdn*.public.tube8.com/ \n http*://videos.flv*.redtubefiles.com/ \n http*://cdn*.public.extremetube.phncdn.com/ \n http*://cdn*.video.pornhub.phncdn.com/ \n ||mms.vlog.xuite.net \n http*://vs*.thisav.com/ \n http*://archive.rthk.hk/ \n http*://video*.modimovie.com/ \n http*://v*.cache*.c.docs.google.com/ \n /^https?:\\/\\/[^\\/]+\\/[^?]+\\.(?:cab|f4v|flv|hlv|m4v|mp4|mp3|ogg|avi|exe|zip|iso|ipa|rar|bz2|xz|deb|dmg|3gp)(?:$|\\?)/ \n http*://*.googleusercontent.com/videoplayback?')
    _GAE = GAE; GAE = lambda req: _GAE(req, autorange_rules.match(req.url, req.proxy_host[0]))
    import re; useragent_match = re.compile('(?i)mobile').search
    useragent_rules = RuleList('||twitter.com')
    withgae_sites = RuleList('||c.docs.google.com \n ||translate.google.com \n http*://books.google.com/books?id= \n http*://*.googleusercontent.com/videoplayback?')
    notruehttps_sites = HostList('.docs.google.com translate.google.com books.google.com')
    truehttps_sites = HostList('.appspot.com .google.com .google.com.hk .googlecode.com .googleusercontent.com .googlegroups.com .google-analytics.com .gstatic.com .googleapis.com .blogger.com .ggpht.com')
    crlf_rules = RuleList('/^https?:\\/\\/[^\\/]+\\.c\\.youtube\\.com\\/liveplay\\?/ \n /^https?:\\/\\/upload\\.youtube\\.com\\// \n /^https?:\\/\\/www\\.youtube\\.com\\/upload\\// \n /^https?:\\/\\/[^\\/]+\\.googlevideo\\.com\\/crossdomain\\.xml/')
    hosts_rules = RuleList(' \n ||appspot.com \n ||google.com \n ||google.com.hk \n ||googlecode.com \n ||googleusercontent.com \n ||googlegroups.com \n ||google-analytics.com \n ||gstatic.com \n ||googleapis.com \n ||blogger.com \n ||ggpht.com \n ||golang.org')
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
        (RuleList(['https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt', 'userlist.ini']), GAE),
    )
    httpslist = (
        (rulelist[0][0], None),
    )

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
            if crlf_rules.match(url, host):
                req.crlf = 1
                return FORWARD
            if not needhttps and hosts_rules.match(url, host):
                return FORWARD
            for rule,target in rulelist:
                if rule.match(url, host):
                    return target
            return FORWARD
        if notruehttps_sites.match(host): return
        if truehttps_sites.match(host): return FORWARD
        url = build_fake_url(proxy_type, (host, port))
        for rule,target in httpslist:
            if rule.match(url, host):
                return target
        return FORWARD
    return find_proxy_handler
