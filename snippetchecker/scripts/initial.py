# -*- coding: utf-8 -*-
"""snippetchecker

SnippetChecker API実行版

"""

from enum import Enum
from typing import List, Dict, Union, Optional, NamedTuple
import json
import os
import sys
import requests
import urllib.request, urllib.error, urllib.parse
import http.client
import http.cookiejar
import ssl
import uuid
from socket import error as SocketError


API_ENTRYPOINT = "https://3fwfffiffbiqxctst7bz32vakq0tmhuv.lambda-url.ap-northeast-1.on.aws/"
API_CLIENTVERSION = '0.1.0'
MIN_API_CPMPAT = 1


class SnippetType(Enum):
    """SnippetType

    スニペットのタイプ

    """
    CODE_SNIPPET = 1
    LINE_ASSIGN = 2
    LINE_VIABLE = 3
    CONSTANT_VALUE = 4
    CONSTANT_FORMULA = 5
    CONSTANT_STRUCTURE = 6
    UNDEFINED = 7


class LoopType(Enum):
    """LoopType

    ループのタイプ

    """
    NO_LOOP = 1
    CONSTANT_LOOP = 2
    GENERAL_LOOP = 3
    CONSTANT_COMPREHENSION = 4
    GENERAL_COMPREHENSION = 5


class LoopStructure(NamedTuple):
    """LoopType

    ループの入れ子構造

    """
    loop: LoopType
    body: List[Union[LoopType,NamedTuple]]


class SnippetChecker:
    """snippetchecker

    SnippetChecker API実行版

    """
    def __init__(self, allow_save_code=False, write_configure_file=True, uniq_id=None):
        """
        Args:
            allow_save_code (bool): サーバーにコードの保存を許可
            write_configure_file (bool): ローカル設定ファイル作成
            uniq_id (bool): ローカル識別子
        """
        self.configure = dict()
        self.errormsg = []
        self.pyver = f'{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}'
        self.allow_save_code = allow_save_code
        self.cookiejar = http.cookiejar.CookieJar()
        self.cookie = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        localconf = dict()
        conf = os.path.join(os.path.expanduser("~"),".snippetchecker")
        if os.path.isfile(conf):
            with open(conf) as f:
                localconf = json.loads(f.read())
        if type(localconf) is dict:
            uniq_id = localconf.get('UNIQUE_ID', uniq_id)
        apiresult = self._api_fetche(API_ENTRYPOINT, {'name':'configure','data':{'version':API_CLIENTVERSION},'python':self.pyver}, reconnect=5, uniq_id=uniq_id)
        assert apiresult, "Configure Error.\nInternet connection probrem or broken ~/.snippetchecker?\nremove it and re-install snippetchecker!"
        try:
            apiconf = json.loads(apiresult)
        except:
            assert False, 'API result error'
        if apiconf is not None and type(apiconf) is dict and 'API_COMPATIBILITY' in apiconf:
            assert int(apiconf['API_COMPATIBILITY']) <= MIN_API_CPMPAT, 'API_COMPATIBILITY error.\nPlease updata package to newest version.\n\nTo update, use this command;\n$ pip install --update snippetchecker-api'
        if apiconf is not None and type(apiconf) is dict and type(localconf) is dict:
            self.configure['API_ENTRYPOINT'] = apiconf.get('API_ENTRYPOINT', localconf.get('API_ENTRYPOINT', API_ENTRYPOINT))
            if 'result' in apiconf and type(apiconf['result']) is dict:
                for key in set(apiconf['result'].keys())|set(localconf.keys()):
                    self.configure[key] = apiconf['result'].get(key, localconf.get(key, ''))
        if uniq_id is not None and type(uniq_id) is str:
            self.configure['UNIQUE_ID'] = uniq_id
        if write_configure_file and localconf != self.configure:
            with open(conf, "w") as wf:
                wf.write(json.dumps(self.configure))

    def print_errors(self):
        print('\n'.join(self.errormsg))

    def clear_errors(self):
        self.errormsg = []
    
    def _common_api(self, name, data):
        if 'version' not in data:
            data['version'] = API_CLIENTVERSION
        apiresult = self._api_fetche(self.configure['API_ENTRYPOINT'], {'name':name,'data':data,'python':self.pyver,'allow_save_code':self.allow_save_code}, errormsg=self.errormsg)
        if apiresult is None:
            self.errormsg.append('API responce error')
            return None
        try:
            apiresult = json.loads(apiresult)
        except:
            self.errormsg.append('json parse error')
            return None
        if type(apiresult) is not dict or len(apiresult) == 0:
            self.errormsg.append('json type error')
            return None
        if 'error_msg' in apiresult:
            if type(apiresult['error_msg']) is str:
                self.errormsg.append(apiresult['error_msg'])
            elif type(apiresult['error_msg']) is list:
                for l in apiresult['error_msg']:
                    if type(l) is str:
                        self.errormsg.append(l)
        if 'result' in apiresult:
            return apiresult['result']
        return None

    def _api_fetche(self, url, data, sleep_time=0.0, timeout=3.0, reconnect=1, uniq_id=None, errormsg=None):
        lasterror = None
        result = None
        if errormsg is None:
            errormsg = self.errormsg
        if uniq_id is None and 'UNIQUE_ID' in self.configure:
            uniq_id = self.configure['UNIQUE_ID']
        if uniq_id is not None and type(uniq_id) is str and len(uniq_id) > 0:
            for t in range(reconnect):
                try:
                    headers = {'Content-Type':'application/json','User-agent':f'SnippetChecker/{API_CLIENTVERSION} ({uniq_id})'}
                    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
                except:
                    errormsg.append('post data format error')
                    return None
                try:
                    result = self.cookie.open(req, timeout = timeout).read()
                    break
                except EOFError as e:
                    lasterror = 'Cannot access api with EOFError'
                except urllib.error.URLError as e:
                    return None
                except urllib.error.HTTPError as e:
                    lasterror = 'Cannot access api with urllib2.httperror'
                except ssl.SSLError as e:
                    lasterror = 'Cannot access api with ssl error'
                except http.client.BadStatusLine as e:
                    lasterror = 'Cannot access api with BadStatusLine'
                except http.client.IncompleteRead as e:
                    lasterror = 'Cannot access api with IncompleteRead'
                except SocketError as e:
                    lasterror = 'Cannot access api with SocketError'
                except UnicodeEncodeError as e:
                    lasterror = 'Cannot access api with UnicodeEncodeError'
                time.sleep(sleep_time)
            if result is None and lasterror is not None and errormsg is not None and type(errormsg) is list:
                errormsg.append(lasterror)
            return result
        else:
            errormsg.append('Uniq ID error')
            return None

    def determine_snippet_type(self,code:str) -> SnippetType:
        """determine_snippet_type

        スニペットのタイプを認識する

        Args:
            code (str): スニペットの文字列

        Returns:
            SnippetType: スニペットのタイプ

        Examples:

            >>> determine_snippet_type("hoge = hogehoge + 1") == LINE_ASSIGN
                True

        """
        result = self._common_api(name='determine_snippet_type',data={'code':code})
        try:
            return SnippetType(result)
        except ValueError as e:
            return SnippetType.UNDEFINED

    def enumerate_difinitions_used(self,code:str) -> List[str]:
        """enumerate_difinitions_used

        スニペット内での定義を列挙する

        Args:
            List[str]: 定義されている名前の一覧

        Returns:
            SnippetType: スニペットのタイプ

        Examples:

            >>> enumerate_difinitions_used("hoge = hogehoge + 1") == ['hoge']
                True

        """
        return self._common_api(name='enumerate_difinitions_used',data={'code':code})

    def enumerate_variables_assign(self,code:str) -> List[str]:
        """enumerate_variables_assign

        スニペット内で代入更新されている定義を列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 代入されている名前の一覧

        Examples:

            >>> enumerate_variables_assign("hoge = hogehoge + 1") == ['hoge']
                True

        """
        return self._common_api(name='enumerate_variables_assign',data={'code':code})

    def enumerate_functions_called(self,code:str) -> List[str]:
        """enumerate_functions_called

        スニペット内で呼び出されている関数を列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 呼び出されている関数の一覧

        Examples:

            >>> enumerate_functions_called("hoge = random.randint(1,100) + 1") == ['random.randint']
                True

        """
        return self._common_api(name='enumerate_functions_called',data={'code':code})

    def enumerate_functions_define(self,code:str) -> List[str]:
        """enumerate_functions_define

        スニペット内で定義されている関数を列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 定義されている関数の一覧

        Examples:

            >>> enumerate_functions_define("def hoge():\\n  pass") == ['hoge']
                True

        """
        return self._common_api(name='enumerate_functions_define',data={'code':code})

    def enumerate_classes_define(self,code:str) -> List[str]:
        """enumerate_classes_define

        スニペット内で定義されているクラスを列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 定義されているクラスの一覧

        Examples:

            >>> enumerate_classes_define("class hoge():\\n  hogehoge=1") == ['hoge']
                True

        """
        return self._common_api(name='enumerate_classes_define',data={'code':code})

    def enumerate_packages_import(self,code:str) -> List[str]:
        """enumerate_packages_import

        スニペット内でインポートされているパッケージを列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: インポートされているパッケージの一覧

        Examples:

            >>> enumerate_packages_import("import random") == ['random']
                True

        """
        return self._common_api(name='enumerate_packages_import',data={'code':code})

    def check_formal_assign(self,
                            code:str,
                            target_name:str,
                            safe_function:List[str]) -> bool:
        """check_formal_assign

        正常な代入文かどうかをチェックする

        Args:
            code (str): スニペットの文字列
            target_name (str): 代入先の変数名
            safe_function (List[str]): 呼び出しを許可する関数名

        Returns:
            bool: 正常な代入文かどうか

        Examples:

            >>> check_formal_assign("hoge = 1 + random.randint(1,100)", "hoge", ["random.randint"])
                True

        """
        return self._common_api(name='check_formal_assign',data={'code':code,'target_name':target_name,'safe_function':safe_function})

    def check_formal_snippet(self,
                             code:str,
                             safe_function:List[str],
                             safe_objects:List[str],
                             safe_modules:List[str]) -> bool:
        """check_formal_snippet

        正常なスニペットどうかをチェックする

        Args:
            code (str): スニペットの文字列
            safe_function (List[str]): 呼び出しを許可する関数名
            safe_objects (List[str]): 使用を許可するオブジェクト名
            safe_modules (List[str]): インポートを許可するモジュール名

        Returns:
            bool: 正常な代入文かどうか

        Examples:

            >>> check_formal_snippet('import random\\nhoge = 1\\nwhile True:\\n  hoge += random.randint(1,100)', ['random.randint'], [], ['random'])
                True

        """
        return self._common_api(name='check_formal_snippet',data={'code':code,'safe_function':safe_function,'safe_objects':safe_objects,'safe_modules':safe_modules})

    def find_loop_in_snippet(self, code:str) -> List[Union[LoopType,LoopStructure]]:
        """find_loop_in_snippet

        スニペットに含まれるループの種類を判定する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[Union[LoopType,LoopStructure]]: ループの入れ子構造

        Examples:

            >>> find_loop_in_snippet("a=0\\nfor _ in range(10):\\n  a+=1\\nprint(a)") == [CONSTANT_LOOP]
                True
            >>> find_loop_in_snippet("while True:\\n  [b for b in range(20)]")
                [LoopStructure(loop=<LoopType.GENERAL_LOOP: 3>, body=[<LoopType.CONSTANT_COMPREHENSION: 4>])]

        """
        result = self._common_api(name='find_loop_in_snippet',data={'code':code})
        def _casttype(r):
            if type(r) is int:
                return LoopType(r) if r in [2,3,4,5] else LoopType.NO_LOOP
            elif type(r) is str:
                return LoopType(int(r)) if r in ['2','3','4','5'] else LoopType.NO_LOOP
            elif type(r) is dict:
                return [LoopStructure(loop=LoopType(int(k)),body=_casttype(v)) for k,v in r.items()]
            elif type(r) is list:
                return sum([(p if type(p) is list else [p]) for p in [_casttype(v) for v in r]], [])
        try:
            return _casttype(result)
        except ValueError as e:
            return LoopType.NO_LOOP


def initialrun():
    tester = SnippetChecker(write_configure_file=True, uniq_id=str(uuid.uuid4()))
    if len(tester.errormsg) == 0:
        print("SnippetChecker-API installed successfully.")
        print("Please read service policy from this URL;")
        print("https://www.reiwa-ai.co.jp/policy.html")
    else:
        print("SnippetChecker-API install FAIL!!!")
        print("Please check Internet connection or broken ~/.snippetchecker file.")
        tester.print_errors()
