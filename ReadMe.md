# このソフトウェアについて

GitHubアップロードツール。

`UserRegister.py`の起動時エラーを解消したいが作業中。

* DBテーブル作成と初期値挿入をSQL,TSV,Pyで実行するフレームワークを仮作成した（未テスト）
* 初期処理を4つのメソッドに抽象化したが引数が共通化できない（WebAPI叩くときclient必要）
* 初期処理でWebAPIを叩くときDB要求される。DB生成前なのに。依存解決すべくビジネスロジック作成すべき。
* Databaseクラスをシングルトンにしてコンストラクタ引数から排除する予定。./src/cui/register/command/Inserter.pyなどの呼出箇所のように変更したい。
* Databaseクラスをシングルトンにした（未テスト）
* SettingMeta.pyを書いた（未テスト）

Contributionsツールのせいで面倒になっている。

* `cui/`でなく`batch/`
* `.ini`でなく`.yml`
    * `Github.Contributions.IsGet`のように2階層以上になる
* マルチスレッド化
    * SQLite3はシングルスレッドでないと使えない
* DbInitializer.__InsertInitData()の処理をするかしないか
    * Contributionsだけ実行の是非をconfigファイルで設定したい

Contributionsを別プロジェクトにすべきか。とりあえず実装中。

Upload.py引数なしでの起動エラーを解消した。


* [修正ログ_201802212030.md](memo/修正ログ_201802212030.md)参照。
    * `SSL`でなく`SSH`
    * UserRegister.py
        * 起動エラー（Database.pyコンストラクタ引数変更の影響）
        * `insert`サブコマンドで `-s` フラグなし時にフリーズする（SSH通信応答返らず）
        * `sqlite3`コマンドがない（pythonのsqlite3だけで実行できるようコード変更したい）

# 前回

* [GitHub.Uploader.Pi3.Https.201802211300](https://github.com/ytyaru/GitHub.Uploader.Pi3.Https.201802211300)

# 開発環境

* [Raspberry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 3 Model B
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) GNU/Linux 8.0 (jessie)
        * [pyenv](http://ytyaru.hatenablog.com/entry/2019/01/06/000000)
            * Python 3.6.4

## WebService

* [GitHub](https://github.com/)
    * [アカウント](https://github.com/join?source=header-home)
    * [AccessToken](https://github.com/settings/tokens)
    * [Two-Factor認証](https://github.com/settings/two_factor_authentication/intro)
    * [API v3](https://developer.github.com/v3/)

# コマンド概要

コマンド|説明
--------|----
UserRegister.py|対象とするGitHubアカウントを本ツールに登録する。
Uploader.py|指定ディレクトリをリポジトリとして作成、アップロードする。
OtpCreator.py|指定ユーザのOTP(ワンタイムパスワード)をクリップボードにコピーする。

今回追加したコマンドは`./database/src/contributions/SvgCreator.py`。以下のように実行する。

# 準備

`UserRegister.py`でユーザ登録済みであること。

## 実行

### ユーザ登録

`./src/Uploader.py`でGitHubユーザ名やパスワードなどを登録する。詳細はコマンドのヘルプや[OtpCreator.py](src/Uploader.py)参照。

### アップローダ起動

アップロードしたいリポジトリのrootディレクトリに、以下のようなファイルを配置する。（[CallMe.sh](memo/CallMe.sh)参考）

`user`,`desc`,`url`をリポジトリごとに任意に設定する。
```sh
#!/bin/bash
user=任意GitHubユーザ名
desc="任意リポジトリ説明文。"
url=http://リポジトリ説明の任意URL
target=$(cd $(dirname $0) && pwd)

# Python環境
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
# venv仮想環境
. ~/root/env/py/auto_github/bin/activate

script=~/root/script/py/GitHub.Uploader.Pi3.Https.201802210700/src/Uploader.py
python3 ${script} "${target}" -u  "${user}" -d "${desc}" -l "${url}"
```

実行する。
```sh
$ bash ~/.../target_repo/CallMe.sh
```

以下、画面に従い操作する。

初回時はローカルリポジトリ、リモートリポジトリ作成の確認。
```sh
ユーザ名: xxxxx
メアド: xxxxx
SSH HOST: xxxxx
リポジトリ名: xxxxx
説明: xxxxx
URL: xxxxx
リポジトリ情報は上記のとおりで間違いありませんか？[y/n]
```

commitメッセージ入力。
```sh
リポジトリ名： user/repo
説明: xxxxx
URL: xxxxx
----------------------------------------
add 'src/some1.py'
...
add 'src/some9.py'
commit,pushするならメッセージを入力してください。Enterかnで終了します。
サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成
```

集計結果の例。
```sh
開始日: 2016-06-16T13:13:25Z
最終日: 2018-02-21T04:11:13Z
期  間: 614 日間
リポジトリ総数  : 440
リポジトリ平均数: 0.7166123778501629 repo/日
コード平均量    : 33077.52117263844 Byte/日
コード総量      : 20309598 Byte
  Python      : 15938477 Byte
  HTML        :  2743953 Byte
  Shell       :   590422 Byte
  C++         :   406817 Byte
  CSS         :   210923 Byte
  C#          :   198952 Byte
  JavaScript  :   167782 Byte
  Batchfile   :    44869 Byte
  Makefile    :     3755 Byte
  Visual Basic:     1717 Byte
  C           :     1076 Byte
  PowerShell  :      855 Byte
```

### おまけツール

#### ワンタイムパスワード生成

詳細はコマンドのヘルプや[OtpCreator.py](src/OtpCreator.py)参照。

```sh
$ python3 ./src/OtpCreator.py
```

#### 草SVG生成

```python
$ bash ./src/database/contributions/outputsvg.sh
```

一度作成したら動作しないようになっている。is_overwriteフラグで指定可能。変更したければコード修正すること。

`GitHub.Contributions.{username}.{year}.svg`の書式で出力される。

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

利用ライブラリは以下。

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[dataset](https://dataset.readthedocs.io/en/latest/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/dataset/blob/master/LICENSE.txt)
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright © 1996-2011 Leonard Richardson](https://pypi.python.org/pypi/beautifulsoup4),[参考](http://tdoc.info/beautifulsoup/)
[pytz](https://github.com/newvem/pytz)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>](https://github.com/newvem/pytz/blob/master/LICENSE.txt)
[PyYAML](https://github.com/yaml/pyyaml)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2006 Kirill Simonov](https://github.com/yaml/pyyaml/blob/master/LICENSE)
[pyotp](https://github.com/pyotp/pyotp)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2011-2017 Mark Percival m@mdp.im, Nathan Reynolds email@nreynolds.co.uk, Andrey Kislyuk kislyuk@gmail.com, and PyOTP contributors](https://github.com/pyotp/pyotp/blob/master/LICENSE)
[SQLAlchemy](https://www.sqlalchemy.org/)|[MIT](https://opensource.org/licenses/MIT)|[Mike Bayer](https://pypi.python.org/pypi/SQLAlchemy/1.2.2)
[furl](https://github.com/gruns/furl)|[Unlicense](http://unlicense.org/)|[gruns/furl](https://github.com/gruns/furl/blob/master/LICENSE.md)

以下、依存ライブラリ。

Library|License|Copyright
-------|-------|---------
[alembic](https://github.com/zzzeek/alembic)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2009-2018 by Michael Bayer.](https://github.com/zzzeek/alembic/blob/master/LICENSE)
[banal](https://github.com/pudo/banal)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2017 Friedrich Lindenberg](https://github.com/pudo/banal/blob/master/LICENSE)
[certifi](https://github.com/certifi/python-certifi)|[MPL2.0](https://www.mozilla.org/en-US/MPL/2.0/)|[MPL2.0](https://github.com/certifi/python-certifi/blob/master/LICENSE)
[chardet](https://github.com/chardet/chardet)|[LGPL2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.ja.html)|[Copyright (C) 1991, 1999 Free Software Foundation, Inc.](https://github.com/chardet/chardet/blob/master/LICENSE)
[idna](https://github.com/kjd/idna)|All rights reserved.|[Copyright (c) 2013-2017, Kim Davies. All rights reserved.](https://github.com/kjd/idna/blob/master/LICENSE.rst)
[mako](https://github.com/zzzeek/mako)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2006-2016 the Mako authors and contributors see AUTHORS file.](https://github.com/zzzeek/mako/blob/master/LICENSE)
[normality](https://github.com/pudo/normality)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/normality/blob/master/LICENSE)
[dateutil](https://pypi.python.org/pypi/python-dateutil/2.6.1)|[Simplified BSD](https://opensource.org/licenses/BSD-2-Clause)|[© Copyright 2016, dateutil.](https://dateutil.readthedocs.io/en/stable/)
[python-editor](https://github.com/fmoo/python-editor)|[Apache License 2.0](https://opensource.org/licenses/Apache-2.0)|[fmoo/python-editor](https://github.com/fmoo/python-editor/blob/master/LICENSE)
[six](https://pypi.python.org/pypi/six)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2010-2018 Benjamin Peterson](https://github.com/benjaminp/six/blob/master/LICENSE)

