__all__ = ['support','api']

from typing import List, Dict, Union, Optional
import json
import os
from .scripts.initial import SnippetType, LoopType, LoopStructure

class SnippetChecker:
    """snippetchecker

    SnippetCheckerローカル実行版

    Note:
        Local execution version is not implemented. use the api package.

    """
    def __init__(self):
        conf = os.path.join(os.path.expanduser("~"),".snippetchecker")
        if os.path.isfile(conf):
            with open(conf) as f:
                self.configure = json.loads(f.read())
    
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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

    def enumerate_functions_define(self,code:str) -> List[str]:
        """enumerate_functions_define

        スニペット内で定義されている関数を列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 定義されている関数の一覧

        Examples:

            >>> enumerate_functions_define("def hoge():\n  pass") == ['hoge']
                True

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

    def enumerate_classes_define(self,code:str) -> List[str]:
        """enumerate_classes_define

        スニペット内で定義されているクラスを列挙する

        Args:
            code (str): スニペットの文字列

        Returns:
            List[str]: 定義されているクラスの一覧

        Examples:

            >>> enumerate_classes_define("class hoge():\n  hogehoge=1") == ['hoge']
                True

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'

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
            safe_objects (List[str]): 仕様を許可するオブジェクト名
            safe_modules (List[str]): インポートを許可するモジュール名

        Returns:
            bool: 正常な代入文かどうか

        Examples:

            >>> check_formal_snippet("import random;hoge = 1;while True:hoge += random.randint(1,100)", ["random.randint"], [], ["random"])
                True

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'


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

        Note:
            Local execution version is not implemented. use the api package.

        """
        assert 'Local execution version is not implemented. use the api package.'


