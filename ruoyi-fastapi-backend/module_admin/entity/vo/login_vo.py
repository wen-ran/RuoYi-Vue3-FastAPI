import re

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from exceptions.exception import ModelValidatorException
from module_admin.entity.vo.menu_vo import MenuModel


class UserLogin(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    user_name: str = Field(description='用户名')
    password: str = Field(description='用户密码')
    code: str | None = Field(default=None, description='验证码')
    uuid: str | None = Field(default=None, description='会话编号')
    login_page_key: str | None = Field(default='default', description='登录页标识')
    login_info: dict | None = Field(default=None, description='登录信息')
    captcha_enabled: bool | None = Field(default=None, description='是否启用验证码')


class UserRegister(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    username: str = Field(description='用户名')
    password: str = Field(description='用户密码')
    confirm_password: str = Field(description='二次确认密码')
    code: str | None = Field(default=None, description='验证码')
    uuid: str | None = Field(default=None, description='会话编号')

    @model_validator(mode='after')
    def check_password(self) -> 'UserRegister':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')


class Token(BaseModel):
    access_token: str = Field(description='token信息')
    token_type: str = Field(description='token类型')


class LoginToken(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    token: str = Field(description='token信息')


class CaptchaCode(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    captcha_enabled: bool = Field(description='是否启用验证码')
    register_enabled: bool = Field(description='是否启用注册')
    img: str = Field(description='验证码图片')
    uuid: str = Field(description='会话编号')


class SmsCode(BaseModel):
    is_success: bool | None = Field(default=None, description='操作是否成功')
    sms_code: str = Field(description='短信验证码')
    session_id: str = Field(description='会话编号')
    message: str | None = Field(default=None, description='响应信息')


class MenuTreeModel(MenuModel):
    children: list['MenuTreeModel'] | None | None = Field(default=None, description='子菜单')


class MetaModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    title: str | None = Field(default=None, description='侧边栏和面包屑中展示的名称')
    icon: str | None = Field(default=None, description='路由图标')
    no_cache: bool | None = Field(default=None, description='是否缓存')
    link: str | None = Field(default=None, description='内链地址')


class RouterModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: str | None = Field(default=None, description='路由名称')
    path: str | None = Field(default=None, description='路由地址')
    hidden: bool | None = Field(default=None, description='是否隐藏路由')
    redirect: str | None = Field(default=None, description='重定向地址')
    component: str | None = Field(default=None, description='组件地址')
    query: str | None = Field(default=None, description='路由参数')
    always_show: bool | None = Field(default=None, description='是否总是显示根路由')
    meta: MetaModel | None = Field(default=None, description='其他元信息')
    children: list['RouterModel'] | None | None = Field(default=None, description='子路由')
