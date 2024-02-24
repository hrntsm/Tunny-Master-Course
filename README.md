# SHIMZ-AECTech_Tunny-Master-Course

## 概要

なぜいまさら日本で新しい最適化の Grasshopper コンポーネントを作成するのか。

既存の Grasshopper での最適化を考えた場合、いくつか挙げられる。

| 名称      | 対応アルゴリズム                                                    | 備考                                              |
| --------- | ------------------------------------------------------------------- | ------------------------------------------------- |
| Galapagos | GA, SA                                                              | デフォルトで搭載                                  |
| Wallacei  | GA(NSGA-II)                                                         | GA の分析に特化した UI。ユーザーが多く資料も多い  |
| Octopus   | GA(SPEA-II, HypE)                                                   | 機械学習機能を含む                                |
| Opossum   | GA(NSGA-II), RBFOpt, CMA-ES, Particle Swarm, MOEA/D, Ant Colony     | 代理モデルを使った Performance Explorer が強力    |
| Tunny     | GA(NSGA-II, NSGA-III), ベイズ最適化(GP, TPE), CMA-ES, QMC, ランダム | Optuna を利用。Dashboard 機能による強力な結果分析 |

-
-

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
