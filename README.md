# SHIMZ-AECTech_Tunny-Master-Course

<p align="center">
  <img src="https://raw.githubusercontent.com/hrntsm/Tunny-docs/main/static/home-og.png" />
</p>

## 開発経緯

なぜいまさら日本で新しい最適化の Grasshopper コンポーネントを作成するのか。

既存の Grasshopper での最適化を考えた場合、いくつか挙げられる。
基本的には遺伝的アルゴリズムがベースにある最適化コンポーネントが主になっている。

| 名称      | 対応アルゴリズム                                                        | 備考                                              |
| --------- | ----------------------------------------------------------------------- | ------------------------------------------------- |
| Galapagos | **GA**, SA                                                              | デフォルトで搭載                                  |
| Wallacei  | **GA(NSGA-II)**                                                         | GA の分析に特化した UI。ユーザーが多く資料も多い  |
| Octopus   | **GA(SPEA-II)**, HypE                                                   | 機械学習機能を含む                                |
| Opossum   | **GA(NSGA-II)**, RBFOpt, CMA-ES, Particle Swarm, MOEA/D, Ant Colony     | 代理モデルを使った Performance Explorer が強力    |
| Tunny     | **GA(NSGA-II, NSGA-III)**, ベイズ最適化(GP, TPE), CMA-ES, QMC, ランダム | Optuna を利用。Dashboard 機能による強力な結果分析 |

Nature Architects では、1 回の解析に時間がかかる解析（例えば 15 分/1 解析）を多く行います。
GA はアルゴリズムとしてはあまり収束が早いアルゴリズムではありません。
より効率的に最適化を行うために、SMBO に対応した Grasshopper コンポーネントの作成が必要になった。

### 仕組み

これまでの多くの最適化コンポーネントと違って、最適化部分は自分で開発していません。
[Optuna](https://www.preferred.jp/ja/projects/optuna/) という最新の機械学習のハイパーパラメータ最適化に多く使われている Python のライブラリを使用しています。
開発は日本のスタートアップである [Preferred Networks](https://www.preferred.jp/ja/) が OSS として行っています。

Tunny の開発に合わせて私もコントリビューターとして開発に関わっています。

- [Optuna - Github](https://github.com/optuna/optuna)

公式サイトには以下のような記述があります。

> Optuna™, an open-source automatic hyperparameter optimization framework,
> automates the trial-and-error process of optimizing the hyperparameters.
> It automatically finds optimal hyperparameter values based on an optimization target.
>
> Optuna is framework agnostic and can be used with most Python frameworks,
> including Chainer, Scikit-learn, Pytorch, etc.
>
> Optuna is used in PFN projects with good results.
> One example is the second place award in the Google AI Open Images 2018 – Object Detection Track competition.

私自身は最適化アルゴリズムの研究者ではないので、最新の知見が常に反映される"イケてる"ライブラリを使用することで最新の機能をキープしています。

また開発者が日本人であることから日本語での資料も多くあります。
特に最適化手法について日本語でまとまった書籍が発売されており、他の最適化コンポーネントに対して理論の理解という面でもアドバンテージがあります。

- [Optuna によるブラックボックス最適化](https://www.ohmsha.co.jp/book/9784274230103/)

## Tunny の特徴

### 複数の最適化手法の採用

Tunny は非常に多くの最適化手法をサポートしています。
他に比べてなぜ最適化手法が疑問に思われるかもしれませんが、最適化ソフトを考えると少ないほうが稀です。
例えば modeFRONTIER などは非常に多くの手法をサポートしています。

Tunny で採用しているのは以下の手法です。

1. ベイズ最適化
   1. TPE
   2. GP
1. 進化アルゴリズム
   1. NSGA-II
   2. NSGA-III
   3. CMA-ES
1. 乱数
   1. QMC（準モンテカルロ）
   1. ランダム

これらは Tunny の UI からどの手法を採用するか選択することができます。

<img width="291" alt="Screenshot 2024-02-24 at 15 46 23" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/68ecebad-d18f-48fd-bab8-c613180701ff">

### 制約条件の対応

Tunny は明示的に制約条件に対応しています。
これまでの最適化コンポーネントでは、ペナルティ法で制約を考慮することが主でした。
（ペナルティ法：制約を満たさないときに目的関数の値にペナルティを与える方法。例えば値を他に比べて非常に大きくするなど）

手法としてはソフト制約（Soft Constraint）と呼ばれる手法です。
この手法では制約条件を満たさない探索も行うため、その点に注意してください。
イメージとしては、得られた結果が制約条件を満たさない場合は、その点付近を"あまり"探索しなくなるものだと考えてください。

#### 設定方法

Constraint Fish Attribute コンポーネントの 「Constraint」の入力に数字を入力します。
リストでの入力に対応しています。
ここに入力されている値の全てが 0 以下の場合、その試行は制約条件を満たす試行だと判断されます。

<img width="672" alt="Screenshot 2024-02-24 at 15 43 02" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/2792c746-5ed2-4915-a236-1be8505dcbf2">

サンプルファイルは以下です。

- optimization_with_constraint.ghß

### 最適化の永続化

#### 最適化のファイルへの保存

Tunny は最適化の永続化を行うことができます。
つまり、Grasshopper とは独立したファイルとして最適化結果を保存して、一度最適化を止めたあと、再開することができます。

一方でそのせいで、1 試行毎に結果を保存する処理が入ります。
そのせいで他の最適化コンポーネントより遅いので、その点は留意してください。

比較用にサンプルを用意しました。
Galapagos と Tunny の比較するファイルになっています。
Tunny は仕組み上、必ず結果を保存しないといけません。
最適化終了時に結果を保存するインメモリーモードがあり、こちらのほうが若干最適化が早くなります。
ですが、インメモリーでの再スタートはできません。

- opt-speed_check.gh
  1. Galapagos
  2. Tunny（永続化あり）
  3. Tunny（インメモリー）

インメモリー機能は以下の InMemory にチェックをいれることで有効化されます。

<img width="288" alt="Screenshot 2024-02-24 at 17 25 23" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/cff43f79-4d48-48eb-8afa-ed1e03c4ea3f">

最適化結果は、リレーショナルデータベースである SQLite 形式（.sqlite, .db）か、テキストで保存されるジャーナル形式（.log）で保存することができます。
どの保存形式でどこに保存するかは以下で設定することができます。
ジャーナル形式を推奨しています。

<img width="292" alt="Screenshot 2024-02-24 at 17 24 53" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/4f7f9391-f232-4a32-8aee-73bf98cdc528">

なお、後で説明する Human in the loop モードは現状では SQLite 形式でしか動きませんが、次のバージョンからジャーナル形式で保存できるようになります。

#### Grasshopper 内への保存

最適化結果は、上記の外部のファイルに保存する以外に、Grasshopper 内に保存することもできます。
Fish コンポーネントは Internalize に対応しているため、結果のみを保存したい場合はこちらのほうが便利です。

<img width="675" alt="Screenshot 2024-02-24 at 20 39 33" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/2dd753fc-1717-4cce-83fb-bbed6c65e716">

### カテゴリカルな最適化への対応

これまでの最適化ツールは連続値に対する最適化をサポートしていました。
ですが建築では連続しない値を最適化したい場合があります。
そのためにカテゴリカルな最適化への対応を行いました。

では具体的にはどういうことでしょうか。
以下の数列、左から右に大小関係があります。

- 1,2,3,4,5

では次の組み合わせはどうでしょうか
これらは大小関係がありません。

- ブレース、ラーメン、壁式

これまでの Grasshopper での最適化では例えばブレース ＜ ラーメン ＜ 壁式
のような本来存在しない順番付をして最適化をしてしまうため、
うまく最適化できないことがありました。

そのため Tunny ではカテゴリーを用いた最適化に対応しています。
最適化でよく使用する NumberSlider では数字しか扱えないので、文字列を扱うために Value List に対応しています。
以下の例では計算手法（AlgorithmType）として Ad, Su, Mu, Di の４つの中から選択するようにしています。
当然これらは計算手法なので、大小関係がありません。

<img width="783" alt="Screenshot 2024-02-25 at 13 39 57" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/8ab589f0-fcec-4d16-b0e3-9b7b2e86834f">

上記は以下のファイルになります。

- categorical_optimization.gh

### 高度な結果分析機能

Tunny は高度な結果分析を行うことができます。
確認可能な結果は以下です。

1. EDF 図
1. コンター図
1. 平行座標図
1. スライス図
1. 重要度図
   - これらの指標を見ることでどの変数にどの程度の感度があるかを確認することができます。
   - 一般的にどんな最適化で変数がたくさんあっても重要な変数は数個程度だと言うことが知られています。
     - https://proceedings.mlr.press/v32/hutter14.html
   - なおこういった感度を可視化するツールを使うときは最適化ではなくランダムや QMC を使いましょう。
1. 最適化ヒストリー図
1. パレートフロント図
1. ハイパーボリューム図
   - 単一目的の場合は、ヒストリーを見れば収束しているか概ね判断できます。
   - 多目的最適化の場合の収束判定は、パレートフロント図を見る以外に、ハイパーボリュームを使うことで判断することができます。
1. クラスタリング図
1. ランク図
   - どの変数がどの程度影響するのか図で確認することができます。
1. タイムライン図
1. 3D モデルなどのファイル
   - 最適化結果の数字と合わせてモデルを確認することができます。

これらの図は全てインタラクティブに操作可能です。
例えば平行座標図は順番を変えたり、表示する範囲を変更することができます。

通常の最適化結果は Grasshopper 内の UI や Rhino のビューポート上に表示することしかできません。
そのため、結果は Rhino を起動するかスクリーンショットを確認するしか方法はありません。
Tunny は上記の結果の図を以下の 2 つの方法で保存することができます。

- png
- html

これらの結果は Dashboard でも確認することができます。
Dashboard は Tunny の UI だけでなく Grasshopper のツールバーからも開くことができます。

|                                                                                                                                                                                  |                                                                                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="500" alt="Screenshot 2024-02-25 at 14 34 06" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/8533b74e-8b94-427d-97f6-df568c0dd7f3"> | <img width="500" alt="Screenshot 2024-02-25 at 14 34 45" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/ce0edeb2-07d2-47ed-9ac8-dc1fe7e4b55b"> |

Dashboard はプロットされた点をダブルクリックするとその点の詳細に飛ぶことができます。

#### 感度を確認するときの注意点

以下は同じ試行回数を行った場合の、コンター図です。
前半3つは最適値周りはよくサンプリングされていますが、それ以外の点が少なくうまくコンターが作成できていないことがわかります。
後半の2つは最適化の手法ではなく全体を確認するための手法のため、きれいなコンターが描けています。

感度を可視化するツールはきれいに点が取れていることが前提になります。
最適化を行ってしまうと、最適値付近の情報しかえられないので注意してください。

|ベイズ最適化|GA|CMA-ES|ランダム|QMC|
|---|---|---|---|---|
|<img width="220" alt="Screenshot 2024-02-25 at 14 43 33" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/12191aa7-0e3e-4320-99f9-7912e8a898a2">|<img width="220" alt="Screenshot 2024-02-25 at 14 43 56" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/05030f89-ea4f-41c6-bd03-0ff416382162">|<img width="220" alt="Screenshot 2024-02-25 at 14 44 26" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/86c6f103-a63b-49ed-a056-f0b4a1c4d418">|<img width="220" alt="Screenshot 2024-02-25 at 14 44 49" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/5bcbd0d5-f6e7-43b7-9474-e8e4c7e64cc3">|<img width="220" alt="Screenshot 2024-02-25 at 14 45 22" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/81cad646-2dec-4bb1-940c-ec7686e518f8">

#### aaa

14. Artifact で結果を保存できる
15. note でコメントを残せる
16. 各アルゴリズムの違いについて
17. 機械学習との連携について
18. Human-in-the-loop 最適について
19. なぜ世代の入力がないのか

## より高度な使用法

### Optuna から Grasshopper を使う

### 機械学習との連携

### 変化するモデル形状の GIF 化
