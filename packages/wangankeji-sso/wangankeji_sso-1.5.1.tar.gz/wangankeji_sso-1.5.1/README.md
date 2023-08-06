# 网安 SSO 客户端

示例见 [sample.py](./sample.py)

## 需要实现以下功能

- 提供通信接口
    - 会校验请求头（加密传输）
    - 接收用户的绑定/解绑
    - 接收用户的登录校验
- 提供登录接口
    - 不校验请求头
    - 存储登录的 session、cookie
- 定期检查当前用户的登录状态
    - token 是否仍然存活
- 退出时向SSO发通知

### 实现描述

此节点会描述：当系统需要接入时，功能实现的细节。

应用内需要提供以下内个地址:

- 通信接口地址 用于处理应用与SSO间数据交换的地址
- 登录接口地址 用于处理应用登录状态（一般用于将登录信息写入 session/cookie），完成后应当转到 **主页地址**
- 主页地址 **登录接口地址** 处理完成后，需要跳转到的地址
- 登录地址 登录请求失败或接口处理失败后的跳转地址

#### 提供通信接口

```python
from wangankeji_sso.client import AbstractSsoRequestHandler, SsoToken, SsoErrorCodes
from typing import Optional, List


class MySsoRequestHandler(AbstractSsoRequestHandler):
  def get_user(self, user_id: str) -> Optional[dict]:
    """
    可选实现
    """
    pass

  def get_all_users(self) -> List[dict]:
    """
    若应用内存在用户体系
    并且:
        1. 需要进行用户绑定（校验用户名密码）
        2. 需要通过此系统校验登录（校验用户是否可用）
    那么必须实现此接口
    """
    # 数据结构:
    # [{
    #     'uid': 用户ID,
    #     'uname': 用户名,
    #     'user_rid': 用户角色ID列表，多个ID使用逗号分隔,
    #     'ext': []
    # }]
    pass

  def get_role(self, role_id: str) -> Optional[dict]:
    """
    可选实现
    """
    pass

  def get_all_roles(self) -> List[dict]:
    """
    若应用内存在用户体系
    并且:
        1. 需要进行用户绑定（校验用户名密码）
        2. 需要通过此系统校验登录（校验用户是否可用）
    那么必须实现此接口
    """
    # 数据结构:
    # [{
    #     'rid': 角色ID,
    #     'rname': 角色名,
    #     'ext': []
    # }]
    pass

  def do_login(self, token: SsoToken) -> SsoErrorCodes:
    """
    进行用户校验（主要是用户状态的校验，比如：用户已经被删除，用户被禁用等）
    """
    return SsoErrorCodes.NONE

  def do_logout(self, token: SsoToken):
    """
    可选实现
    """
    pass

  def do_bind(self, sso_uid: str, app_uid: str, app_uname: str, password: str) -> SsoErrorCodes:
    """
    进行用户校验
    1. 用户密码是否正确
    2. 用户状态的校验，比如：用户已经被删除，用户被禁用等
    """
    return SsoErrorCodes.NONE

  def do_unbind(self, sso_uid: str, app_uid: str, app_uname: str) -> SsoErrorCodes:
    """
    可选实现
    """
    return SsoErrorCodes.NONE
```

#### 实例化客户端

```python
from wangankeji_sso.client import Sso, SsoOption

option = SsoOption()
# 应用的 APPID
# option.app_id = SSO_APP_ID
# SSO 的通信地址
# option.sso_url = SSO_URL
# SSO RSA 公钥（注意：此公钥仅可用于单一应用，多个应用无法通用）
# option.sso_public_key = SSO_PUB_KEY
# 应用RSA私钥
# option.app_private_key = APP_PRIV_KEY

sso = Sso(option, MySsoRequestHandler())
```

#### 登录接口

示例如下:

```python
from wangankeji_sso.client import SsoToken
from wangankeji_sso.client.utils import Rsa


def post(request, token: str, main_url: str, login_url: str):
  """

  :param request: 请求对象
  :param token: 使用SSO公钥加密的TOKEN
  :param main_url: 主页地址
  :param login_url: 登录页地址
  :return:
  """
  try:
    # 解密出明文的 token
    clear_token = SsoToken.parse(Rsa.decrypt(token, options.APP_PRIV_KEY))
    if not clear_token:
      raise Exception('TOKEN 数据无效')
  except Exception as ex:
    return HttpResponse('无法解码 TOKEN')

  # 使用 token，设置当前的登录状态
  try:
    # 应用内的登录流程
    # 添加一个登录方式的标记
    session['login-by-wa-sso'] = 1
    session['wa-sso-token'] = str(clear_token)
    redirect_url = main_url
  except Exception as ex:
    redirect_url = login_url
  return Redirect(redirect_url)
```

#### 检查登录状态

建议在应用的中间件上，添加登录状态的的检查。（为了减轻资源消耗，建议缓存检查结果）

```python
if session.get('login-by-wa-sso') == 1:
    # 是从 sso 登录的
    token = session.get('wa-sso-token')
    # sso 来自客户端实例
    if not sso.client.check_login(token):
        session.remove('login-by-wa-sso')
        session.remove('wa-sso-token')
        return HttpResponse('登录已经超时')
```
