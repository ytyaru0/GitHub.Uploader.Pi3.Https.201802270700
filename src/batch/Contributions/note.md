草データ蓄積。

DB作成とデータ挿入はフレームワークで実行する。
草データ取得はUploaderと直接関係ないので、実行しないよう設定できると嬉しい。
いつか以下のうちどれかの対応をしたい。

* config.iniで設定するようにする
* Uploaderとは別プロジェクトにする

なお、SvgCreator.py（ContributionSvg.py）はツール。DBからSVGファイルを生成する。管理できていない。Uploaderと直接関係ない。
