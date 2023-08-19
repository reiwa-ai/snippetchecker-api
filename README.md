# SnippetChecker API実行版



## SnippetCheckerとは



SnippetCheckerとは、大規模言語モデル（LLM）が生成した断片的なソースコード（スニペット）を、実行前にチェックするためのパッケージです。

SnippetChecker API実行版は、フリーAPI版のSnippetCheckerで、商用非商用を問わず、自由に利用することが出来ます。

ここにあるパッケージは、APIを利用するためのクライアントです。APIそのものは[株式会社令和AI](https://www.reiwa-ai.co.jp/)によって提供されています。

**[サービス提供ポリシー](https://www.reiwa-ai.co.jp/policy.html)**

必ず[サービス提供ポリシー](https://www.reiwa-ai.co.jp/policy.html)を読んでから利用してください。クライアントおよびAPIの機能は、すべて「ASIS」で提供されています。株式会社令和AIは該当APIの利用に伴う一切の責任を負いません。



### なぜLLMが出力したコードをそのまま実行してはいけないのでしょうか？



ソースコードの生成能力に長けているLLMを使うと、人間の指示を機械が理解可能なソースコードに落とし込むことが出来ます。

そして、そのコードを実行するようにプログラムを作成すれば、人間の自然言語による指示に従う機能を作ることが出来ます。

しかし、LLMが生成するコードは**「本質的に安全ではない」**ため、それをそのまま実行してはいけません。

これは、単にコードが間違っている場合がある、という以上の、セキュリティリスクに関するものです。

例えば、重要なシステムファイルを上書きするようなコードを生成するように、悪意のあるユーザーがLLMに指示を与えるかもしれません。

プログラマーが指定したプロンプト指示を‘上書’きして、悪意のあるコードを出力させる**「脱獄（ジェイルブレイク）」**というテクニックが知られているため、一般に公開するサービスや製品にLLMによる制御を組み込むには、相応のセキュリティ対策が必要になります。



### なぜDocker等のコンテナを使用するだけでは不十分なのでしょうか？

コンテナ技術による仮想化は、詳細が不明なソースコードを実行する際に、安全性を担保するためのサンドボックスとして利用されることがあります。

しかしコンテナ化は、コンテナの外側にあるコンピューター環境にアクセス出来なくなるだけで、不適切な制御コードを生成させたり、ハードウェアに危険な行動を取らせたりという‘攻撃’を防御することは出来ません。

多くのコンテナ技術は、あくまで仮想化されたコンピューター環境を提供するだけであり、その中で動くコードの実行結果が、ハードウェア制御などの用途において安全であるかは、別の技術を使って確認する必要があります。



## 部分コード（スニペット）による制御の例



[AIテック&実験サイト](https://www.reiwa-ai.co.jp/aitechsite/surveillancecamera_craft1.html)



## SnippetChecker API実行版の利用準備



AIが生成したコードを利用するためには、**以下の3つが必須**となります。

- **LLMに入力するプロンプトを事前にチェックする機構**
- **LLMが出力したコードを実行前にチェックする機構**
- **チェック済みのコードを安全に実行するサンドボックス**

3つの要素のうち、**1つでも欠けると、AIの生成したコードを安全に実行することは出来ません**。

SnippetCheckerは、そのうちのコードの実行前チェックのみを行うパッケージです。

その他の2つは別の手段で実装する必要があります。具体的な手法については、[こちら](#部分コード（スニペット）による制御の例)にあるサンプルを参照してください。



### インストール



「pip install」でインストールできます。

```sh
$ pip install snippetchecker-api
```

又は

```sh
$ pip install git+https://github.com/reiwa-ai/snippetchecker-api.git
```

正しくインストールされると、[サービス提供ポリシー](https://www.reiwa-ai.co.jp/policy.html)へのリンクが表示されます。



### アンインストール



完全に環境から削除するには、パッケージのアンインストールと「~/.snippetchecker」を削除します。

```sh
$ pip uninstall snippetchecker-api
$ rm ~/.snippetchecker
```



### SnippetCheckerクラスの作成



```python
>>> from snippetchecker.api import SnippetChecker, SnippetType, LoopType, LoopStructure
>>> c = SnippetChecker()
```

エラーが出る場合は「~/.snippetchecker」を削除してパッケージを再インストールしてください。



## スニペットの判定



SnippetChecker API実行版では、スニペットの種類の判定、コード中で定義されているクラスやパッケージ・関数・変数の列挙、ループの入れ子構造のチェック、コードの実行前チェックを行うことが出来ます。

```python
>>> assign_code = "new_enemy_hp = enemy_hp - my_attack"

>>> short_code = """for angle in range(180):
    camera.move(angle)
    time.sleep(60/180)"""

>>> long_code = """import cv2

# Haar Cascadesを使用して顔を検出する
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    for angle in [0, 45, 90, 135, 180]:
        camera.move(angle)

        # 画像を取得
        img = cv2.imread('image.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # 道路を監視している角度（0度または45度）で人の姿が検出された場合、
        # カメラをその角度に固定して集中的に撮影する
        if angle in [0, 45] and len(faces) > 0:
            time.sleep(60)  # 1分間その角度で撮影
            break  # その後、再び全周監視ルーチンに戻る

        time.sleep(10)  # 他の角度では10秒間撮影"""
```



### スニペットの種類の判定



おおまかなスニペットの種類の判定を行うには、「**determine_snippet_type**()」を使います。



```python
>>> c.determine_snippet_type(assign_code)
<SnippetType.LINE_ASSIGN: 2>

>>> c.determine_snippet_type(short_code)
<SnippetType.CODE_SNIPPET: 1>

>>> c.determine_snippet_type(long_code)
<SnippetType.CODE_SNIPPET: 1>
```



### 呼び出されている関数の列挙



スニペット内で呼び出されている関数の名前を列挙するには、「**enumerate_functions_called**()」を使います。



```python
>>> c.enumerate_functions_called(assign_code)
[]

>>> c.enumerate_functions_called(short_code)
['range', 'time.sleep', 'camera.move']

>>> c.enumerate_functions_called(long_code)
['time.sleep', 'cv2.CascadeClassifier', 'cv2.cvtColor', 'cv2.imread', 'camera.move', 'len', 'face_cascade.detectMultiScale']
```



### ループ構造のチェック



スニペット内にあるループの入れ子構造をチェックするには、「**find_loop_in_snippet**()」を使います。



```python
>>> c.find_loop_in_snippet(assign_code)
[]

>>> c.find_loop_in_snippet(short_code)
[<LoopType.CONSTANT_LOOP: 2>]

>>> c.find_loop_in_snippet(long_code)
[LoopStructure(loop=<LoopType.GENERAL_LOOP: 3>, body=[<LoopType.CONSTANT_LOOP: 2>])]
```



### スニペットの実行前チェック



スニペットの実行前チェックには、「**check_formal_assign**()」「**check_formal_snippet**()」を使います。



```python
>>> c.check_formal_assign(assign_code,
                        target_name='new_enemy_hp',
                        safe_function=[])
True

>>> c.check_formal_snippet(short_code,
                         safe_function=['range', 'camera.move', 'time.sleep'],
                         safe_objects=['camera'],
                         safe_modules=['time'])
True

>>> c.check_formal_snippet(long_code,
                         safe_function=['cv2.CascadeClassifier', 'camera.move',
                                        'cv2.imread', 'cv2.cvtColor', 
                                        '*.detectMultiScale', 'len', 'time.sleep'],
                         safe_objects=['camera'],
                         safe_modules=['time','cv2'])
True
```



これらの関数は、あらゆるPythonコードを確実にチェックするものではありません。

使用を許可するパッケージや関数名は、コード上における名前のチェックなので、実際の実行時に呼び出されるインスタンスの実態を保証しません。そのため、実際のパイプラインにおいては、LLM入力プロンプトの事前チェックと、コード実行のためのサンドボックスが別途必要になります。



## お問い合わせ



本パッケージに関するメッセージは、

contact@reiwa-ai.biz

までお問い合わせください。



