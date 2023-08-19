from typing import List, Dict, Union

def make_cleaned_builtins(allow_global_functions:List[str],
                          allow_import_modules:List[str]) -> object:
    """make_cleaned_builtins

    許可された組み込み関数とインポートのみ含んだ__builtins__を返す

    Args:
        allow_global_functions (List[str]): 呼び出しを許可する関数名
        allow_import_modules (List[str]): インポートするモジュール名

    Returns:
        object: 新しい__builtins__

    Examples:

        execで実行するときにコードチェックと組み合わせるとある程度安全なサンドボックスになる

        >>> global_builtins = make_cleaned_builtins(allow_global_functions=['int'], allow_import_modules=['random'])
        >>> local_variables = dict()
        >>> exec('test_val = int(random.random()*100)',
        >>>   {'__builtins__':global_builtins},
        >>>   local_variables
        >>>   )
        >>> print(local_variables)
        {'test_val': 58}
        >>> exec('test_val = float(random.random()*100)',
        >>>   {'__builtins__':global_builtins},
        >>>   local_variables
        >>>   )
        NameError: name 'float' is not defined

    Note:
        __builtins__だけでは安全な実行は出来ないので、事前のコードチェックを必ず行うこと
        無限ループによるリソースの食い潰し等には対処できないので、その場合はSnippetRunnerを使うこと

    """
    global_builtins = None # 使用できるビルトイン関数
    if len(allow_global_functions) > 0: # 使用できる関数が指定されていれば
        # グローバル名前空間の関数
        module_dict = __builtins__ if type(__builtins__) is dict else __builtins__.__dict__
        # 使用できるグローバル関数のみ含むbuiltinsを作る
        global_builtins = {name:module_dict.get(name, None) for name in allow_global_functions}
    if len(allow_import_modules) > 0: # インポートするモジュールが指定されていれば
        global_builtins = {} if global_builtins is None else global_builtins
        module_dict = __builtins__ if type(__builtins__) is dict else __builtins__.__dict__
        for modname in allow_import_modules: # インポートして利用できるようにする
            global_builtins[modname] = __builtins__['__import__'](modname)
    return global_builtins


