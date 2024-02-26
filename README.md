# Tunny-Master-Course

<p align="center">
  <img src="https://raw.githubusercontent.com/hrntsm/Tunny-docs/main/static/home-og.png" />
</p>

## 環境

- 必須
  - Windows11
  - Rhino 8
  - Tunny 0.11.0
    - このリポジトリにあるのものが対応しているバージョン
- 任意
  - [LunchBoxML](https://www.food4rhino.com/en/app/lunchbox)
  - Karamba3d
  - VS Code（または任意の Python コードの編集環境）

## 簡単なデモ

簡単なデモを行います。

## 開発経緯

なぜいまさら日本で新しい最適化の Grasshopper コンポーネントを作成するのでしょうか。

既存の Grasshopper での最適化を考えた場合、いくつか挙げられます。
太字で示したように、基本的には遺伝的アルゴリズムがベースにある最適化コンポーネントが主になっています。

| 名称      | 対応アルゴリズム                                                        | 備考                                              |
| --------- | ----------------------------------------------------------------------- | ------------------------------------------------- |
| Galapagos | **GA**, SA                                                              | デフォルトで搭載                                  |
| Wallacei  | **GA(NSGA-II)**                                                         | GA の分析に特化した UI。ユーザーが多く資料も多い  |
| Octopus   | **GA(SPEA-II)**, HypE                                                   | 機械学習機能を含む                                |
| Opossum   | **GA(NSGA-II)**, RBFOpt, CMA-ES, Particle Swarm, MOEA/D, Ant Colony     | 代理モデルを使った Performance Explorer が強力    |
| Tunny     | **GA(NSGA-II, NSGA-III)**, ベイズ最適化(GP, TPE), CMA-ES, QMC, ランダム | Optuna を利用。Dashboard 機能による強力な結果分析 |

Nature Architects では、1 回の解析に時間がかかる解析（例えば 15 分/1 解析）を多く行います。
1 解析に 15 分というと許容できる時間だと感じるかもしれません。

ここで最適化について考えてみます。変数の数にもよりますが、少なくとも 100 回の試行を行いたいと考えます。
1 解析 15 分ということは、1 時間に 4 回、業務時間（8 時間）に 32 回しか結果を得ることができません。
解析設定の確認などをもろもろやっていると 100 回の結果を取得するだけでも 1 週間はかかります。

そういった状況の中で効率的に最適結果を取得することを考えた場合、GA はアルゴリズムとしてはあまり収束が早いアルゴリズムではありません。
より効率的に最適化を行うために、SMBO(Sequential Model Based Optimization) に対応した Grasshopper コンポーネントの作成が必要になり、開発を始めました。

### 仕組み

これまでの多くの最適化コンポーネントと違って、最適化部分は自分で開発していません。
Grasshopper と最適化ライブラリを接続する部分のみを開発していることも特徴です。

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
他に比べてなぜ多くの最適化手法が使用可能か疑問に思われるかもしれませんが、最適化ソフトを考えると少ないほうが稀です。
例えば modeFRONTIER などは非常に多くの手法をサポートしています。

Tunny で採用しているのは以下の手法です。
この中でベイズ最適化が SMBO に該当する手法になります。

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

#### 収束速度

冒頭でより早く収束する手法が必要として、Tunny の開発を始めたと書きました。
実際に各手法でどの程度結果が違うのか確認してみます。

比較の対象として、Rosenbrock function という関数に置いて、どの様に収束していくのか比較してみます。
以下のような条件で探索します。

<img width="600" alt="Screenshot 2024-02-25 at 20 34 27" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/485d019b-e204-49de-967b-df5995919ebc">

[最適化アルゴリズムを評価するベンチマーク関数まとめ](https://qiita.com/tomitomi3/items/d4318bf7afbc1c835dda#rosenbrock-function)

複数のケースを確認します。

1. 変数：3、試行回数：126
2. 変数：3、試行回数：1024
3. 変数：10、試行回数：126
4. 変数：10、試行回数：1024

以下に最適化のヒストリーと計算時間をまとめます。
Rosenbrock function はただの式なので計算は一瞬です。
そのため計算時間は、ほぼ最適化で次のどの点を探索するかの計算にかかっている時間だと考えてください。
なお SMBO に該当する TPE と GP は代理モデルの作成のため、試行回数の半分だけランダムサンプリングを行った後に各手法で最適化を行っています。

|               | 変数 3                                                                                                                                               | 変数 10                                                                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 試行回数 128  | ![3_variables_128_trials](https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/28b0fd02-e0a4-46d7-86e0-96183f11a926)          | ![10_variables_128_trials](https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/5d076dd4-311b-4d74-bf7a-40c9ce76bc03)         |
| 最小値        | <img width="362" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/4215c0d2-8493-4968-853c-b54de73980e6"> | <img width="362" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/11bda4e1-85a5-4c9b-86bc-70fdbe0032b5"> |
| 計算時間      | <img width="361" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/bcab8b97-2e97-4872-b109-b25addecf429"> | <img width="361" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/d296953a-ca63-41d4-9a99-51e9bd5b7a29"> |
| 試行回数 1024 | ![3_variables_1024_trials](https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/a2e5c61e-f977-4e82-becf-d35a9e50dc31)         | ![10_variables_1024_trials](https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/19d68499-d1d3-452a-8010-8360415195c0)        |
| 最小値        | <img width="362" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/f05bb1cb-09c6-4cfc-8587-18a52278c85e"> | <img width="368" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/0c5bf81e-2026-4089-88b7-0507727e532c"> |
| 計算時間      | <img width="361" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/8d790e7d-7c52-4ecf-9cef-0dfb6a7d4965"> | <img width="361" alt="image" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/d6cccee1-5317-4c39-a6cc-4c5eefb637c3"> |

結果を見るとどのケースでも GP が優秀ですが、最適化にかかる時間が最もかかっています。
同じベイズ最適化でも TPE はあまり計算時間がかからず良い結果が得られています。
少ない試行回数では NSGA-II はあまり良い結果を得ることができないこともここからわかります。

この例では、目的関数を計算する時間がほぼ 0 なため、最適化処理にかかる**時間**という観点では、GP はあまり優秀でないように見えるかもしれません。
ですが、目的関数の計算に数分以上かかる場合は、少ない計算回数で良い結果が得られる GP がかなり有効な手法になります。

試行回数が多く、変数が少ない場合は、TPE と NSGA-II は同程度の結果が得られています。
試行回数が多く、変数も多い場合は TPE よりも NSGA-II のほうが良い結果が得られています。
また CMA-ES は明確に良い結果が得られています。

つまり変数が多く、多くの試行回数を実行できる(1 回の目的関数の計算時間が短い)場合は NSGA-II のほうが良い場合があります。

これらの結果を見ると CMA-ES も最適化において有効な手法だと考えられますが、単一目的の制約条件がない場合にしか使えない手法のため、いつもこの手法が選択できるわけではありません。

最適化途中の試行点のばらつきを確認すると、TPE、GP、CMA-ES はかなり集中して探索しています。
一方で NSGA-II は確実に結果が改善しながらも比較的ばらつきながら探索しています。
このことから、変数が多い場合や多峰性が強いと想定される場合は、NSGA-II を選択したほうが、広い範囲から探索してくれる場合があります。

これらの結果ファイルは compare のフォルダに入っています。

※ これはあくまで一例です。
最適化の設定などによって多少変化することもありますが、一般的にこのような傾向があると考えてください。

#### 最適化手法について

Optuna の公式サイトでは、一般に以下の回数がそれぞれの手法で推奨される試行回数だとされています。
他の情報と合わせて[公式のドキュメント](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html)から抜粋しています。

| 手法         | GP     | TPE       | NSGA-II    | CMA-ES       |
| ------------ | ------ | --------- | ---------- | ------------ |
| 試行回数     | 10-100 | 100-1,000 | 100-10,000 | 1,000-10,000 |
| 多目的最適化 | ◯      | ◯         | ◯          | ✗            |
| 制約条件     | ◯      | ◯         | ◯          | ✗            |

Tunny の最適化では、入力が以下のように試行回数(Number of trials)しかありません。
よくなぜ "世代(generation)" の入力や "世代に含まれる個体数(population)" の設定がないのかという質問をもらいます。
回答としては、これらの概念があるのは進化アルゴリズムに分類される手法に限るからです。
ベイズ最適化、ランダム、QMC には世代や世代の個体数という概念がありません。
そのため入力としては "試行回数" のみになっています。

では NSGA での世代数はどうのように設定するとかというと、Settings のタブから設定できます。
Population Size が世代に含まれる個体数になります。
つまり Number of Trials / Population Size が世代数になります。

例えば Number of Trials が 100、Population Size が 30 の場合、4 世代目の途中まで最適化が実行されます。
この結果に対して追加で 20 回の最適化を行うと 4 世代目の全ての個体の評価が完了することになります。

| 試行回数の設定                                                                                                                                                                   | 個体数の設定                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="283" alt="Screenshot 2024-02-25 at 22 09 38" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/3d048a05-6682-4b3f-a6a6-bd7beb97d044"> | <img width="287" alt="Screenshot 2024-02-25 at 22 09 18" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/8071894c-1ba8-428d-a537-7cd0fd8d354b"> |

各手法についてより詳しく知りたい場合は、optuna の本を読まれることを推奨します。

- [Optuna によるブラックボックス最適化(再掲)](https://www.ohmsha.co.jp/book/9784274230103/)

### 制約条件の対応

これまでの最適化コンポーネントでは、ペナルティ法で制約を考慮することが主でした。
（ペナルティ法：制約を満たさない場合に目的関数の値にペナルティを与える方法。例えば値を他に比べて非常に大きくするなど）

Tunny は明示的に制約条件に対応しています。

手法としてはソフト制約（Soft Constraint）と呼ばれる手法です。
この手法では制約条件を満たさない探索も行うため、その点に注意してください。
イメージとしては、得られた結果が制約条件を満たさない場合は、その点付近を"あまり"探索しなくなるものだと考えてください。

#### 設定方法

Constraint Fish Attribute コンポーネントの 「Constraint」の入力に数字を入力します。
リストでの入力に対応しています。
ここに入力されている値の全てが 0 以下の場合、その試行は制約条件を満たす試行だと判断されます。

<img width="600" alt="Screenshot 2024-02-24 at 15 43 02" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/2792c746-5ed2-4915-a236-1be8505dcbf2">

サンプルファイルは以下です。

- optimization_with_constraint.gh

### 初期解の設定

最適化を実施するとき、手動で良い値の組み合わせが複数わかっていても、それらを最適化に反映することはこれまではできませんでした。
収束性は最初に良い解を与えるとかなり改善するので、わかっているならば与えたくなります。

Tunny では Fish Egg という機能を使うことでそれを実現できます。
与えたい変数の組み合わせにした状態で lay(卵を産む)を true にするとその値の組み合わせが記録されます。
複数の組み合わせを初期解として登録することができます。

<img width="600" alt="Screenshot 2024-02-25 at 23 02 26" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/ee66f488-3974-46ea-be5d-0c25d127819b">

サンプルファイルは以下です。

- Optimization_with_initial_values.gh

### 最適化の永続化

#### 最適化のファイルへの保存

Tunny は最適化の永続化を行うことができます。
つまり、Grasshopper とは異なる独立したファイルとして最適化結果を保存します。
そのため、一度最適化を止めたあとでもそのファイルを読み込むことによって最適化を再開することができます。

最近では会社の業務管理の都合で、業務時間外は PC の電源をつけていられないという話も聞きます。
通常の最適化では、業務時間内に最適化を完了させないといけませんが、Tunny の場合は最適化を再開できるため、この問題を解決できます。

一方でその影響で、1 試行毎に結果を保存する処理が入ります。
その結果、他の最適化コンポーネントより遅いので、その点は留意してください。

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

具体的にはどういうことでしょうか。
以下の数列、左から右に大小関係があります。

- 1,2,3,4,5

では次の組み合わせはどうでしょうか
これらは大小関係がありません。

- ブレース、ラーメン、壁式

これまでの Grasshopper での最適化では例えば「ブレース ＜ ラーメン ＜ 壁式」
のような本来存在しない大小関係を仮定して最適化をしてしまうため、
うまく最適化できないことがありました。

そのため Tunny ではカテゴリーを用いた最適化に対応しています。
最適化でよく使用する NumberSlider では数字しか扱えないので、文字列を扱うために Value List に対応しています。
以下の例では計算手法（AlgorithmType）として Ad, Su, Mu, Di の４つの中から選択するようにしています。
当然これらは計算手法なので、大小関係がありません。

<img width="783" alt="Screenshot 2024-02-25 at 13 39 57" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/8ab589f0-fcec-4d16-b0e3-9b7b2e86834f">

上記は以下のファイルになります。

- categorical_optimization.gh

### 高度な結果分析機能

Tunny は最適化結果に対して、複数の視点から結果の分析を行うことができます。
確認可能な結果は以下です。

1. EDF 図
2. コンター図
3. 平行座標図
4. スライス図
5. 重要度図
   - これらの指標を見ることでどの変数にどの程度の感度があるかを確認することができます。
   - 一般的に最適化で変数がたくさんあっても重要な変数は数個程度だと言うことが知られています。
     - https://proceedings.mlr.press/v32/hutter14.html
   - なおこういった感度を可視化するツールを使うときは最適化ではなくランダムや QMC を使いましょう。
6. 最適化ヒストリー図
7. パレートフロント図
8. ハイパーボリューム図
   - 単一目的の場合は、ヒストリーを見れば収束しているか概ね判断できます。
   - 多目的最適化の場合の収束判定は、パレートフロント図を見る以外に、ハイパーボリュームを使うことで判断することができます。
9. クラスタリング図
10. ランク図

- どの変数がどの程度影響するのか図で確認することができます。

11. タイムライン図
12. 3D モデルなどのファイル

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
前半 3 つは最適値周りはよくサンプリングされていますが、それ以外の点が少なくうまくコンターが作成できていないことがわかります。
後半の 2 つは最適化の手法ではなく全体を確認するための手法のため、きれいなコンターが描けています。

感度を可視化するツールは便利ですが、きれいに点が取れていることが前提になります。
最適化を行ってしまうと、偏った情報しかえられず間違った判断になってしまうので注意してください。

| TPE                                                                                                                                                                              | NSGA-II                                                                                                                                                                          | CMA-ES                                                                                                                                                                           | ランダム                                                                                                                                                                         | QMC                                                                                                                                                                              |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="220" alt="Screenshot 2024-02-25 at 15 01 09" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/902375ec-73d8-4349-863b-cd162eb2d6e0"> | <img width="220" alt="Screenshot 2024-02-25 at 15 00 21" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/5ee15980-9590-494f-8f71-920ecea33f4f"> | <img width="220" alt="Screenshot 2024-02-25 at 14 59 25" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/9ec4f50f-4f19-40af-95d2-632f908a5adb"> | <img width="220" alt="Screenshot 2024-02-25 at 14 58 04" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/e6324a2c-e5d0-406f-8e1e-7404e0f2afed"> | <img width="220" alt="Screenshot 2024-02-25 at 14 57 06" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/fd7b8e93-a255-4027-bfc2-ae413ac687a0"> |
| <img width="220" alt="Screenshot 2024-02-25 at 15 01 57" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/66a8f3ee-c8b2-459a-bf0e-48bae18033d7"> | <img width="220" alt="Screenshot 2024-02-25 at 15 02 27" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/d84088b7-712a-4228-a494-de5d2233ffec"> | <img width="220" alt="Screenshot 2024-02-25 at 15 02 58" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/0b3cd83e-c959-45cf-b730-f1462ef9105c"> | <img width="220" alt="Screenshot 2024-02-25 at 15 03 41" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/9c92234a-90e1-4341-a8e5-7e435def043d"> | <img width="220" alt="Screenshot 2024-02-25 at 15 04 12" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/5aa2ada9-7794-427c-a865-602b41fc6500"> |
| x1:0.51, x2:0.49                                                                                                                                                                 | x1:0.77, x2:0.23                                                                                                                                                                 | x1:0.77, x2:0.23                                                                                                                                                                 | x1:0.67, x2:0.33                                                                                                                                                                 | x1:0.71, x2:0.29                                                                                                                                                                 |

なお正解の値は以下になります。
きれいにサンプリングしても、十分に一様なサンプリングをしないと正解をえられないのでその点についても注意してください。

| 重要度                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="300" alt="Screenshot 2024-02-25 at 15 14 22" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/f84f1b61-e257-4ce8-ba4c-16d0ebcfc751"> |
| x1:0.6, x2:0.4                                                                                                                                                                   |

この例は以下のファイルになります。

- compare_contour.gh

### Human-in-the-loop

以下のビルのファサードを想定したいくつかのパターンを作成しました。
あなたはどれが好きですか？

<img width="600" alt="Screenshot 2024-02-26 at 16 40 54" src="https://github.com/hrntsm/Tunny-Master-Course/assets/23289252/777e469d-d21f-4385-a88d-6fd0b44741bc">

Tunny の Human-in-the-loop 機能を使うことであなたの好みを学習させることができます。
以下のような選択画面が現れ、最も好きではないもの（WORST）なものを選択してください。
徐々に形状が収束していきます。

<img width="600" alt="Screenshot 2024-02-26 at 17 24 03" src="https://github.com/hrntsm/Tunny-Master-Course/assets/23289252/96e23501-bda1-4880-b765-65fc7383751b">

こちらは以下のサンプルファイルになります。

- Facade_Human-in-the-loop.gh

この機能は一人で扱っていても技術的に面白い程度にだと思います。

複数の人間に対して行った場合に面白い使い方ができます。
例えば設計対象地域でワークショップなどを行い、本機能を使用することで
「この地域の人が好きな形」のようなものを数値化することができます。
この様に複数人（群衆）の好みを最適化することを「Crowd in the loop」といったりもします。

デモで示した手法は Preferential Bayesian Optimization（選好ベイズ最適化）と呼ばれる手法になります。
例えば以下のスライドなどを読むとより理解が深まると思われます。

- [2023-07-25 好みを学習して支援するデザイン支援システム（産総研 AI セミナー）](https://speakerdeck.com/yuki_koyama/aist-ai-seminar-preferential-bayesian-optimization?slide=64)

## より高度な使用法

### 機械学習との連携

この例では Karamba3d と LunchboxML を使用します。
ただし、Karamba3d はライセンスが必要なので、Karamba3D がなくても機械学習の部分は動作するようにしています。

以下のような 1 スパン × 5 スパン 11 階建てのビルの部材断面どうしますか？

<img width="200" alt="Screenshot 2024-02-26 at 17 28 14" src="https://github.com/hrntsm/Tunny-Master-Course/assets/23289252/b8690e39-837a-4e0f-8ced-77f06560c417">

部材断面と層間変形角の関係を機械学習で学習し、断面を予測するモデルを作成してみます。
これまでの最適化ツールでは、"最適値"のみを探索するのでこういった機械学習の学習データを作成することができませんでした。

Tunny はランダムや QMC などの一様にサンプリングするツールを持っているため、こういった用途にも使うことができます。
LunchbocML と Tunny を組み合わせることで、Grasshopper 単独でこの処理を行うことができます。
機械学習の手法には LightGBM という手法を使用します。

<img width="450" alt="Screenshot 2024-02-26 at 17 34 26" src="https://github.com/hrntsm/Tunny-Master-Course/assets/23289252/1bbe5779-0f86-4117-a50a-1b68903fd905">

以下が機械学習で断面と層間変形角を学習した結果です。
概ね ±10% 程度の精度で予測できていました。

<img width="1000" alt="Screenshot 2024-02-26 at 17 36 17" src="https://github.com/hrntsm/Tunny-Master-Course/assets/23289252/1b0eac8b-a764-427d-9709-5350230c6102">

### 変化するモデル形状の GIF 化

ここでは Python を使います。
Python そのものをインストールしている必要はありませんが、Python コードを編集するので、テキストエディタが必要になります。
ここでは VSCode を使用します。

Tunny の機能で最適化のヒストリーを作成することができます。
そのため数字としての最適化の状態を確認することは簡単にできます。

建築での最適化を考えると形に対して最適化する場合が多いと思います。
なので、最適化途中で作成された形状の変化がどうなるかも合わせて知りたい場合が多いのではないでしょうか。

Tunny の機能として、Rhino のビューポートの状態を画像として保存することができます。
その画像をつなぎ合わせ GIF 動画とすることで最適化での形状の変化を可視化することができます。

これは Tunny の最適化の多くの部分に Python で作られている Optuna を用いており、高い互換性があるためできることです。

まず以下のサンプルファイルを実行して最適化結果の画像を作成します。
デモ用なので早く最適化が終わるように単純なカーブの長さ最小化問題としています。

- create_gif_animation.gh

GIF を作成するために実行する Python コードは以下です。

```py
import json
import os
from PIL import Image
import optuna

# 以下にそれぞれパスを入れてください
storage_path = "STORAGE_PATH"
artifact_dir_path = "ARTIFACT_DIR_PATH"
gif_path = "GIF_PATH"

# 対象のTunnyのStudyNameを入れてください
study_name = "STUDY_NAME"

# Tunnyの最適化の結果ファイルを読み込みます
lock_obj = optuna.storages.JournalFileOpenLock(storage_path)
storage = optuna.storages.JournalStorage(
    optuna.storages.JournalFileStorage(storage_path, lock_obj=lock_obj),
)
study = optuna.study.load_study(study_name=study_name, storage=storage)
sys_attr_list = [trial.system_attrs for trial in study.trials]

# もし最適化結果のヒストリーの図を確認したい場合は、以下のコメントアウトを解除してください
# optuna.visualization.plot_optimization_history(study).show()

# GIF アニメーションの作成
images = []
for attr in sys_attr_list:
    for key in attr.keys():
        if "artifact" in key:
            artifact_json = json.loads(attr[key])
            images.append(
                Image.open(
                    os.path.join(artifact_dir_path, artifact_json["artifact_id"])
                )
            )
            break

images[0].save(
    gif_path,
    save_all=True,
    append_images=images[
        1:
    ],  # すべての画像ではなく、5つおきに動画化したい場合は 1::5 としてください
    optimize=False,
    duration=40,
    loop=0,
)
```

必要なライブラリをインストールして gif 化を実行するために以下をターミナルで実行してください。

```
./python.exe -m pip install
./python.exe create_gif_animation.py
```

この Python ファイルは以下にあります。

- create_gif_animation.py

作成されたカーブの長さが最小化されていく動画です。
