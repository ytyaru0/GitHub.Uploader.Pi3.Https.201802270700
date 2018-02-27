
## 2018-02-27

* ./src/database/init/Contributions
* ./src/batch/Contributions

Contributionsは別プロジェクトにすべきか。

Contributionsツールのせいで面倒になっている。そもそもContributionsはツイデのオマケ機能にすぎない。

* `cui/`でなく`batch/`
    * Contributionsのためだけに用意
* `.ini`でなく`.yml`
    * `Github.Contributions.IsGet`のように2階層以上になる
* マルチスレッド化
    * SQLite3はシングルスレッドでないと使えない
* DbInitializer.__InsertInitData()の処理をするかしないか
    * Contributionsだけ実行の是非をconfigファイルで設定したい


## 2018-02-24

草データ蓄積。

DB作成とデータ挿入はフレームワークで実行する。
草データ取得はUploaderと直接関係ないので、実行しないよう設定できると嬉しい。
いつか以下のうちどれかの対応をしたい。

* config.iniで設定するようにする
* Uploaderとは別プロジェクトにする

なお、SvgCreator.py（ContributionSvg.py）はツール。DBからSVGファイルを生成する。管理できていない。Uploaderと直接関係ない。
