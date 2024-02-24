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

これらはTunnyのUIからどの手法を採用するか選択することができます。

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
ここに入力されている値の全てが0以下の場合、その試行は制約条件を満たす試行だと判断されます。

<img width="672" alt="Screenshot 2024-02-24 at 15 43 02" src="https://github.com/hrntsm/SHIMZ-AECTech_Tunny-Master-Course/assets/23289252/2792c746-5ed2-4915-a236-1be8505dcbf2">

### 最適化の永続化

Tunny は最適化の永続化を行うことができます。

1. 最適化の永続化と最適化速度
   1. Tunny は遅い部類に入るので注意
2. 結果の永続化
   1. log や sql 形式で保存でき、最適化を再開できる
   2. 結果（Fish）は Fish コンポーネントに Internalize できるので結果はそういった方法でも保存できる
   3. グラフの編集、永続化。html で保存できるので、いつまでもインタラクティブ
      1. 例えば平行座標図は横軸を動かしたり範囲を設定したりもできる
3. Artifact で結果を保存できる
4. note でコメントを残せる
5. 各アルゴリズムの違いについて
6. 機械学習との連携について
7. Human-in-the-loop 最適について
8. なぜ世代の入力がないのか
