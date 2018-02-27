# コマンド

コマンド|説明
--------|----
GitHubUserRegister.py|アップローダを利用するためのGitHubのアカウント情報登録ツール。
GitHubUploader.py|リポジトリを生成するツール。（ローカル、リモート両方）
GitHubOtpCreator.py|ユーザのOTPを表示しクリップボードにコピーするツール。
GitHubIssue.py|Issue作成ツール。

## GitHubUploader.py

```sh
usage: GitHubUploader.py [-h] [-u USERNAME] [-d DESCRIPTION] [-l HOMEPAGE]
                         [-m MESSAGES]
                         path_dir_pj
```

* リモートリポジトリ生成([GitHub API](https://developer.github.com/v3/repos/#create))
* ローカルリポジトリ生成(`git init`)
    * 追加するファイル確認(`git -n add .`)
    * ファイルを追加する(`git add .`)
    * commitする(`git commit -m`)
* pushする
* プログラミング言語別ファイルサイズを取得する(`GitHub API`)
* 集計表示

以下の要件がある。

* CUI画面確認の入力を省略したい(リポジトリ生成、コミット)
* Issue作成を追加したい

### コマンド引数の名前

#### 共通

略記|フルネーム|説明
----|---------|----
`-u`|`--username`|対象GitHubユーザ名

#### リポジトリ作成

略記|フルネーム|説明
----|---------|----
`-d`|`--description`|対象リポジトリの説明文。
`-h`|`--homepage`|対象リポジトリの関連URL。
`-t`|`--topics`|対象リポジトリのtopic。複数可。

`--homepage`の略記`-l`を`-h`に変える。`--label`に備えて。

#### リポジトリ作成

略記|フルネーム|説明
----|---------|----
`-m`|`--messages`|今回コミットのメッセージ。複数可。1つ目は概要。2つ目以降は詳細。

### Issue作成

略記|フルネーム|説明
----|---------|----
`-i`|`--issues`|今回コミットメッセージ。複数可。1つ目は概要。2つ目以降は詳細。
`-l`|`--labels`|今回コミットメッセージのtopic。複数可。

## Issueのインタフェースをどうするか

* CUI入力
* ファイル入力
* コマンド入力

### CUI入力

```sh
リポジトリ名： trysrv/GitHub.Uploader.Issue.201706191032
説明: None
URL: None
----------------------------------------
commit,pushするならメッセージを入力してください。Enterかnで終了します。
サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成
```

サブコマンド`i`にて標準入力させる案。

* 1回目の入力はタイトル
* 2回目の入力は本文
    * 2回目が空値のままEnterキー押下したら本文なし
    * 2回目が空値以外の場合、3行目以降の入力ができる
        * 空値のままEnterキー押下が2回連続で続いたら終了する

書き直しができないため不便。実装も面倒。

### ファイル入力

IssueはMarkdown形式で書くことが可能。改行により複数行にすることが必要な書式なので、CUI入力では難しい。そこで外部ファイル化して渡す。

```markdown
1行目はIssueのタイトル
# 2行目以降がIssueの本文

* Markdonwの構文として改行が必要なので都合が良い
```

### GUI入力

テキストエリアで入力させる。できればMarkdwonをHTML表示して表示確認もできたら最高。

だが、自動化できなくなる。

### コマンド入力

* GitHubUploader.pyに追加する
* GitHubUpIssue.pyを新規作成する

#### GitHubUploader.pyに追加する

リポジトリをアップロードするという本分からはずれる。コミットのついでにIssueを作成して閉じるならOK。しかし、Issueを作りっぱなしで閉じないのはこのツールの使い方として微妙。Issue作成を本分とした別ツールを作ったほうがいい。それを作ってしまったほうがIssue本来の使い方ができる。

#### GitHubUpIssue.pyを新規作成する

```sh
$ python3 GitHubUpIssue.py --labels Python --labels Tools -i "1つ目はタイトル" -i "# 2つ目からは本分。" -i "" -i "* Markdown形式も可能"
```

Issue番号を表示させれば、コミットメッセージに含めてIssueを閉じることができる。`fix #Issue番号`のように。

* あらかじめリポジトリ作成しておくこと
* どうやってリポジトリ名とユーザ名を取得するか
    * 対象ローカルリポジトリのパスを渡して`.git`からユーザ名を取得できればユーザ名を省略できそう
    * GitHubUploader.pyが参照している`config.ini`からユーザ名を参照すれば省略できる
        * リポジトリを指定した時点でユーザも確定するはずである。もし違うユーザ名ならリモートリポジトリを特定できなくなってしまう

## CUI入力を求められる場合と省略できる場合

### リポジトリ新規生成

* ローカルリポジトリ`.git`がない
    * 起動引数に`-m`, `-d`, `-l`, `-t`が一つもない

せめてコミットメッセージだけは入力すべき。`初回コミット。`など意味のないメッセージでも良いから入力すべき。毎回意味があるコミットにすべきだから。推奨方法にそぐわぬ用途の場合、CUI入力で推奨形式にさせるように仕向ける。

`-m`があれば、リポジトリ生成の確認を省略してしまう。これまでは必ず確認していた。ミスして異なるユーザに生成してしまうなどを防いでいた。

### コミット

* 起動引数`-m`がない

`-m`があれば、コミットの確認を省略してしまう。これまでは必ず`git -n add .`で対象ファイルを確認させていた。ミスして対象外ファイルまでアップロードしてしまうのを未然に防いでいた。


## CUI入力を省略できる場合








#### topics

topicsはリポジトリのメタデータの一つ。一般的なtagのようなもの。

topics追加は現時点ではGitHubAPIの引数で設定できない。将来変わる可能性はあるのでコマンド引数`-t`として予約しておく。

GitHubサイトのHTMLからtopics追加部分を抽出してみた。これを解析すれば自動化できるかもしれない。

```html
<form accept-charset="UTF-8" action="/ytyaru/Github.Uploader.RequestParameter.unittest.201705041425/settings/update_topics" class="js-repo-topics-edit-form" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" value="✓" type="hidden"><input name="_method" value="put" type="hidden"><input name="authenticity_token" value="pOeqfo/Y7rtDD39c+B6w61oNurdW8HGR+z/7qeCBIDfgsrisM0LY8G3As213il3cDOSmO4CS6zjiIxNoc8ilCQ==" type="hidden"></div>
        <div class="tag-input form-control d-inline-block bg-white py-0">
          <ul class="js-tag-input-selected-tags d-inline">
            <li class="d-none topic-tag-action f6 float-left js-tag-input-tag js-template">
              <span class="js-placeholder-tag-name"></span>
              <button type="button" class="delete-topic-button f5 no-underline ml-2 js-remove" tabindex="-1">
                ×
              </button>
              <input name="repo_topics[]" class="js-topic-input" value="" type="hidden">
            </li>

          </ul>

          <input id="repo_topics" class="tag-input-inner form-control bg-white shorter d-inline-block p-0 my-1 border-0" autocomplete="off" autofocus="" type="text">
        </div>

        <button type="button" class="btn float-right js-repo-topics-form-done" data-initial-state="false" aria-expanded="false">
          Done
        </button>
</form>
```

# 実装

* `Client.py`
* TinyDB

## Client.py

`Client.py`はGitHubAPIのまとめクラス。この辺一式のコードが汚い。コンストラクタの引数を何とかしたい。

## TinyDB

これまでSQLite3とdatasetを使っていた。しかしjson形式と異なる形式なので面倒が多い。TinyDBを使って解消できないか。
