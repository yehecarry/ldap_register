from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .forms import register
from ldap3 import Server, Connection, ALL

serverip = '192.168.100.151'  # ldap服务ip地址
ldap_basedn_user = 'cn=test,dc=fotoable,dc=com'  # ldap管理员用户
ldap_basedn_pass = '123456'  # ldap管理员用户密码
ldap_basedb_people = 'ou=People,dc=fotoable,dc=com'  # ldap用户dn
ldap_basedb_group = 'ou=Group,dc=fotoable,dc=com'  # ldap组dn
filter_mail = '@fotoable.com'
soft_dic = {"1": "confluence-users", "2": "jira-software-users", "3": "gitlab"}  # 软件列表


# 添加用户规则
def user_add(username, cname, email):
    server = Server(serverip, get_info=ALL)
    conn = Connection(server, ldap_basedn_user, ldap_basedn_pass, auto_bind=True)
    with open('static/uid', mode='r') as f1:
        number = f1.read()
    re = conn.add("uid=%s,%s" % (username, ldap_basedb_people),
             ['inetOrgPerson', 'shadowAccount', 'posixAccount'],
             {'uid': '%s' % username,
              'sn': '%s' % username,
              'cn': '%s' % cname,
              'userPassword': '{SSHA}byTjdIDsrK6x1m1yQlvAaGYRgiwavVso',
              'mail': '%s' % email,
              'homeDirectory': "/home/test",
              'uidNumber': '%s' % number,
              'gidNumber': 10000})
    return re


# 添加组规则
def change_group(soft_name, username):
    server = Server(serverip, get_info=ALL)
    conn = Connection(server, ldap_basedn_user, ldap_basedn_pass, auto_bind=True)
    conn.modify('cn=%s,%s' % (soft_name,ldap_basedb_group),
                {'member': [('MODIFY_ADD', ['uid=%s,%s' % (username, ldap_basedb_people)])]})
    conn.closed()


# 主函数
def index(request):
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            cname = form.cleaned_data['cname']
            email = form.cleaned_data['email']
            if not email.endswith(filter_mail):
                return render(request, 'index.html', {'form': form, 'error': '邮箱格式不对'})
            softs = form.cleaned_data['soft']
            for soft in softs:
                change_group(soft_dic.get(soft), username)
            if user_add(username, cname, email):
                with open('static/uid', mode='r') as f1:
                    number = f1.read()
                with open('static/uid', mode='w') as f2:
                    f2.write(str(int(number) + 1))
                return render(request, 'index.html', {'form': form, 'error': '用户创建成功\n'
                                                                             ',用户名为%s\n'
                                                                             ',密码为123456\n'
                                                                             ',请登录https://ssp.ftsview.com 进行修改密码操作' % username})
            else:
                return render(request, 'index.html', {'form': form, 'error': '用户已存在'})
        else:
            return render(request, 'index.html', {'form': form, 'error': '用户创建失败,输入有误'})
    else:
        form = register()
    return render(request, 'index.html', {'form': form})
