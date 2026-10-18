---
title: Library Checker 模板题单（LCG）
description: judge.yosupo.jp 官方题库 Library Checker 全量 253 题，按类目整理的算法模板题刷题计划。
tags: [Library Checker, 模板题, 刷题计划, 数据结构]
order: 30
items: 253
covered: 253
source: https://github.com/yosupo06/library-checker-problems
---

**Library Checker**（[judge.yosupo.jp](https://judge.yosupo.jp) 官方题库源 [yosupo06/library-checker-problems](https://github.com/yosupo06/library-checker-problems)，下称 **LCG**）是算法/数据结构库的「验证题」集：每题对应一个经典算法的标准接口，不讲故事、不设思维陷阱，考的是「把这个模板写对、写快」。全量 **253 题**（Apache 2.0），本单按类目整理，站内链接直达中文题面。

## 怎么用这份单子

- 括号里的 `snake_case` 是 LCG 原题名，方便对照原仓库的生成器与数据；
- 标注「special judge」的题输出任意合法解，**暂不可本地评测**（本地 judge 仅支持 diff 比对），待 checker 支持后开放；
- LCG 自带对抗性数据生成器与 naive/wa/tle 对拍解，适合当模板正确性与复杂度的「单元测试」；
- 勾选进度按题号全局共享，跨题目单不丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补 `https://roj.ac.cn` 前缀。

## 目录

- [数据结构](#sec-ds)（47 题）
- [树](#sec-tree)（20 题）
- [图论](#sec-graph)（38 题）
- [字符串](#sec-str)（12 题）
- [多项式](#sec-poly)（28 题）
- [卷积](#sec-conv)（16 题）
- [线性代数](#sec-la)（18 题）
- [数论](#sec-nt)（26 题）
- [组合计数](#sec-ec)（17 题）
- [集合幂级数](#sec-sps)（5 题）
- [计算几何](#sec-geo)（10 题）
- [高精度](#sec-bi)（6 题）
- [其他](#sec-other)（7 题）
- [入门样例](#sec-sample)（3 题）

<a id="sec-ds"></a>
## 数据结构

- [矩形加点求和](/problem/1415)（`rectangle_add_point_get`）
- [单点加区间求和](/problem/30000)（`point_add_range_sum`）
- [静态区间最小值](/problem/30001)（`staticrmq`）
- [并查集](/problem/30002)（`unionfind`）
- [矩形并面积](/problem/30027)（`area_of_union_of_rectangles`）
- [关联数组](/problem/30028)（`associative_array`）
- [双端队列](/problem/30029)（`deque`）
- [双端队列（带全体复合操作）](/problem/30030)（`deque_operate_all_composite`）
- [双端优先队列](/problem/30031)（`double_ended_priority_queue`）
- [动态点赋值矩形仿射矩形求和](/problem/30032)（`dynamic_point_set_rectangle_affine_rectangle_sum`）
- [动态序列区间仿射区间求和](/problem/30033)（`dynamic_sequence_range_affine_range_sum`）
- [直线加查询最小值](/problem/30034)（`line_add_get_min`）
- [多数投票](/problem/30035)（`majority_voting`）
- [有序集合](/problem/30036)（`ordered_set`）
- [可持久化队列](/problem/30037)（`persistent_queue`）
- [可持久化区间仿射区间求和](/problem/30038)（`persistent_range_affine_range_sum`）
- [可持久化并查集](/problem/30039)（`persistent_unionfind`）
- [单点加矩形求和](/problem/30040)（`point_add_rectangle_sum`）
- [单点赋值区间复合](/problem/30041)（`point_set_range_composite`）
- [单点赋值区间复合（大数组）](/problem/30042)（`point_set_range_composite_large_array`）
- [单点赋值区间元素出现次数](/problem/30043)（`point_set_range_frequency`）
- [单点赋值区间排序区间复合](/problem/30044)（`point_set_range_sort_range_composite`）
- [前驱问题](/problem/30045)（`predecessor_problem`）
- [队列（带全体复合操作）](/problem/30046)（`queue_operate_all_composite`）
- [区间加区间最小值](/problem/30047)（`range_add_range_min`）
- [区间仿射单点查询](/problem/30048)（`range_affine_point_get`）
- [区间仿射区间求和](/problem/30049)（`range_affine_range_sum`）
- [区间仿射区间求和（大数组）](/problem/30050)（`range_affine_range_sum_large_array`）
- [区间取 min/max、加 区间求和](/problem/30051)（`range_chmin_chmax_add_range_sum`）
- [区间第 k 小](/problem/30052)（`range_kth_smallest`）
- [区间线性加区间最小值](/problem/30053)（`range_linear_add_range_min`）
- [区间连边并查集](/problem/30054)（`range_parallel_unionfind`）
- [区间反转区间求和](/problem/30055)（`range_reverse_range_sum`）
- [区间赋值区间复合](/problem/30056)（`range_set_range_composite`）
- [矩形求和](/problem/30057)（`rectangle_sum`）
- [线段加查询最小值](/problem/30058)（`segment_add_get_min`）
- [集合异或最小值](/problem/30059)（`set_xor_min`）
- [静态区间不同元素个数](/problem/30060)（`static_range_count_distinct`）
- [静态区间元素出现次数](/problem/30061)（`static_range_frequency`）
- [静态区间逆序对查询](/problem/30062)（`static_range_inversions_query`）
- [静态区间最长上升子序列查询](/problem/30063)（`static_range_lis_query`）
- [静态区间众数查询](/problem/30064)（`static_range_mode_query`） · special judge
- [静态区间求和](/problem/30065)（`static_range_sum`）
- [静态区间求和（带上界）](/problem/30066)（`static_range_sum_with_upper_bound`）
- [静态矩形加矩形求和](/problem/30067)（`static_rectangle_add_rectangle_sum`）
- [带权并查集](/problem/30068)（`unionfind_with_potential`）
- [带权并查集（非交换群）](/problem/30069)（`unionfind_with_potential_non_commutative_group`）

<a id="sec-tree"></a>
## 树

- [最近公共祖先](/problem/30004)（`lca`）
- [笛卡尔树](/problem/30233)（`cartesian_tree`）
- [公共区间分解树](/problem/30234)（`common_interval_decomposition_tree`） · special judge
- [动态树子树加子树求和](/problem/30235)（`dynamic_tree_subtree_add_subtree_sum`）
- [动态树点加路径求和](/problem/30236)（`dynamic_tree_vertex_add_path_sum`）
- [动态树点加子树求和](/problem/30237)（`dynamic_tree_vertex_add_subtree_sum`）
- [动态树点赋值路径复合](/problem/30238)（`dynamic_tree_vertex_set_path_composite`）
- [树上距离频数表](/problem/30239)（`frequency_table_of_tree_distance`）
- [树上跳转](/problem/30240)（`jump_on_tree`）
- [单点赋值树路径复合和](/problem/30241)（`point_set_tree_path_composite_sum`）
- [单点赋值树路径复合和（固定根）](/problem/30242)（`point_set_tree_path_composite_sum_fixed_root`）
- [有根树同构分类](/problem/30243)（`rooted_tree_isomorphism_classification`） · special judge
- [有根树拓扑序最小逆序对](/problem/30244)（`rooted_tree_topological_order_with_minimum_inversions`） · special judge
- [树的直径](/problem/30245)（`tree_diameter`） · special judge
- [树路径复合和](/problem/30246)（`tree_path_composite_sum`）
- [点加路径求和](/problem/30247)（`vertex_add_path_sum`）
- [点加树上等距层求和](/problem/30248)（`vertex_add_range_contour_sum_on_tree`）
- [点加子树求和](/problem/30249)（`vertex_add_subtree_sum`）
- [树上等距层加点查询](/problem/30250)（`vertex_get_range_contour_add_on_tree`）
- [点赋值路径复合](/problem/30251)（`vertex_set_path_composite`）

<a id="sec-graph"></a>
## 图论

- [指派问题](/problem/30097)（`assignment`） · special judge
- [双连通分量](/problem/30098)（`biconnected_components`） · special judge
- [二分图边染色](/problem/30099)（`bipartite_edge_coloring`） · special judge
- [二分图最大匹配](/problem/30100)（`bipartitematching`） · special judge
- [弦图判定](/problem/30101)（`chordal_graph_recognition`） · special judge
- [色数](/problem/30102)（`chromatic_number`）
- [色多项式](/problem/30103)（`chromatic_polynomial`）
- [补图连通分量](/problem/30104)（`connected_components_of_complement_graph`） · special judge
- [四元环计数](/problem/30105)（`counting_c4`）
- [欧拉回路计数](/problem/30106)（`counting_eulerian_circuits`）
- [有向图生成树计数](/problem/30107)（`counting_spanning_tree_directed`）
- [无向图生成树计数](/problem/30108)（`counting_spanning_tree_undirected`）
- [有向图找环](/problem/30109)（`cycle_detection`） · special judge
- [无向图找环](/problem/30110)（`cycle_detection_undirected`） · special judge
- [有向图最小树形图](/problem/30111)（`directedmst`） · special judge
- [支配树](/problem/30112)（`dominatortree`）
- [动态图点加连通块求和](/problem/30113)（`dynamic_graph_vertex_add_component_sum`）
- [枚举团](/problem/30114)（`enumerate_cliques`）
- [枚举三角形](/problem/30115)（`enumerate_triangles`）
- [有向图欧拉路径](/problem/30116)（`eulerian_trail_directed`） · special judge
- [无向图欧拉路径](/problem/30117)（`eulerian_trail_undirected`） · special judge
- [一般图最大匹配](/problem/30118)（`general_matching`） · special judge
- [一般图最大权匹配](/problem/30119)（`general_weighted_matching`） · special judge
- [动态星形增广图全局最小割](/problem/30120)（`global_minimum_cut_of_dynamic_star_augmented_graph`）
- [增量最小生成森林](/problem/30121)（`incremental_minimum_spanning_forest`）
- [增量强连通分量](/problem/30122)（`incremental_scc`）
- [K 次最短路](/problem/30123)（`k_shortest_walk`）
- [最大独立集](/problem/30124)（`maximum_independent_set`） · special judge
- [最小费用 b-流](/problem/30125)（`min_cost_b_flow`） · special judge
- [最小直径生成树](/problem/30126)（`minimum_diameter_spanning_tree`） · special judge
- [最小生成树](/problem/30127)（`minimum_spanning_tree`） · special judge
- [最小斯坦纳树](/problem/30128)（`minimum_steiner_tree`） · special judge
- [强连通分量](/problem/30129)（`scc`） · special judge
- [最短路](/problem/30130)（`shortest_path`） · special judge
- [st 编号](/problem/30131)（`st_numbering`） · special judge
- [三边连通分量](/problem/30132)（`three_edge_connected_components`） · special judge
- [树分解（宽度 2）](/problem/30133)（`tree_decomposition_width_2`） · special judge
- [双边连通分量](/problem/30134)（`two_edge_connected_components`） · special judge

<a id="sec-str"></a>
## 字符串

- [Z 算法](/problem/30003)（`zalgorithm`）
- [Aho-Corasick 自动机](/problem/30222)（`aho_corasick`）
- [回文树（Eertree）](/problem/30223)（`eertree`）
- [枚举回文串](/problem/30224)（`enumerate_palindromes`）
- [最长公共子串](/problem/30225)（`longest_common_substring`） · special judge
- [Lyndon 分解](/problem/30226)（`lyndon_factorization`）
- [子串个数](/problem/30227)（`number_of_substrings`）
- [双端队列回文计数](/problem/30228)（`palindromes_in_deque`）
- [前缀-子串 LCS](/problem/30229)（`prefix_substring_lcs`）
- [Run 枚举](/problem/30230)（`runenumerate`）
- [后缀数组](/problem/30231)（`suffixarray`）
- [通配符模式匹配](/problem/30232)（`wildcard_pattern_matching`）

<a id="sec-poly"></a>
## 多项式

- [形式幂级数复合](/problem/30186)（`composition_of_formal_power_series`）
- [形式幂级数复合（大模数）](/problem/30187)（`composition_of_formal_power_series_large`）
- [形式幂级数复合逆](/problem/30188)（`compositional_inverse_of_formal_power_series`）
- [形式幂级数复合逆（大模数）](/problem/30189)（`compositional_inverse_of_formal_power_series_large`）
- [单项式基转牛顿基](/problem/30190)（`conversion_from_monomial_basis_to_newton_basis`）
- [多项式除法](/problem/30191)（`division_of_polynomials`）
- [形式幂级数 exp](/problem/30192)（`exp_of_formal_power_series`）
- [形式幂级数 exp（稀疏）](/problem/30193)（`exp_of_formal_power_series_sparse`）
- [多项式因式分解](/problem/30194)（`factorization_of_polynomials`） · special judge
- [形式幂级数求逆](/problem/30195)（`inv_of_formal_power_series`）
- [二元形式幂级数求逆](/problem/30196)（`inv_of_formal_power_series_2d`）
- [形式幂级数求逆（稀疏）](/problem/30197)（`inv_of_formal_power_series_sparse`）
- [多项式求逆](/problem/30198)（`inv_of_polynomials`）
- [形式幂级数 log](/problem/30199)（`log_of_formal_power_series`）
- [形式幂级数 log（稀疏）](/problem/30200)（`log_of_formal_power_series_sparse`）
- [多点求值](/problem/30201)（`multipoint_evaluation`）
- [多点求值（等比数列）](/problem/30202)（`multipoint_evaluation_on_geometric_sequence`）
- [多项式插值](/problem/30203)（`polynomial_interpolation`）
- [多项式插值（等比数列）](/problem/30204)（`polynomial_interpolation_on_geometric_sequence`）
- [多项式求根](/problem/30205)（`polynomial_root_finding`） · special judge
- [多项式平移（Taylor Shift）](/problem/30206)（`polynomial_taylor_shift`）
- [形式幂级数快速幂](/problem/30207)（`pow_of_formal_power_series`）
- [形式幂级数快速幂（稀疏）](/problem/30208)（`pow_of_formal_power_series_sparse`）
- [多项式前缀和](/problem/30209)（`prefix_sum_of_polynomial`）
- [多项式序列连乘积](/problem/30210)（`product_of_polynomial_sequence`）
- [多项式采样点平移](/problem/30211)（`shift_of_sampling_points_of_polynomial`）
- [形式幂级数开方](/problem/30212)（`sqrt_of_formal_power_series`） · special judge
- [形式幂级数开方（稀疏）](/problem/30213)（`sqrt_of_formal_power_series_sparse`） · special judge

<a id="sec-conv"></a>
## 卷积

- [按位与卷积](/problem/30011)（`bitwise_and_convolution`）
- [按位异或卷积](/problem/30012)（`bitwise_xor_convolution`）
- [卷积（F2^64 域）](/problem/30013)（`convolution_F_2_64`）
- [卷积](/problem/30014)（`convolution_mod`）
- [卷积（模 1000000007）](/problem/30015)（`convolution_mod_1000000007`）
- [卷积（模 2^64）](/problem/30016)（`convolution_mod_2_64`）
- [卷积（大模数）](/problem/30017)（`convolution_mod_large`）
- [最大公约数卷积](/problem/30018)（`gcd_convolution`）
- [最小公倍数卷积](/problem/30019)（`lcm_convolution`）
- [Min-Plus 卷积（凹 × 任意）](/problem/30020)（`min_plus_convolution_concave_arbitrary`）
- [Min-Plus 卷积（凸 × 任意）](/problem/30021)（`min_plus_convolution_convex_arbitrary`）
- [Min-Plus 卷积（凸 × 凸）](/problem/30022)（`min_plus_convolution_convex_convex`）
- [乘法幺半群卷积（Z/2^N Z）](/problem/30023)（`mul_mod2n_convolution`）
- [乘法幺半群卷积（Z/P Z）](/problem/30024)（`mul_modp_convolution`）
- [多维卷积（截断）](/problem/30025)（`multivariate_convolution`）
- [多维卷积（循环）](/problem/30026)（`multivariate_convolution_cyclic`）

<a id="sec-la"></a>
## 线性代数

- [伴随矩阵](/problem/30135)（`adjugate_matrix`）
- [特征多项式](/problem/30136)（`characteristic_polynomial`）
- [矩阵的 Hafnian](/problem/30137)（`hafnian_of_matrix`）
- [F2 向量空间的交](/problem/30138)（`intersection_of_f2_vector_spaces`） · special judge
- [矩阵求逆](/problem/30139)（`inverse_matrix`）
- [矩阵求逆（模 2）](/problem/30140)（`inverse_matrix_mod_2`）
- [矩阵行列式](/problem/30141)（`matrix_det`）
- [矩阵行列式（任意模数）](/problem/30142)（`matrix_det_arbitrary_mod`）
- [矩阵行列式（模 2）](/problem/30143)（`matrix_det_mod_2`）
- [矩阵乘法](/problem/30144)（`matrix_product`）
- [矩阵乘法（模 2）](/problem/30145)（`matrix_product_mod_2`）
- [矩阵的秩](/problem/30146)（`matrix_rank`）
- [矩阵的秩（模 2）](/problem/30147)（`matrix_rank_mod_2`）
- [矩阵的 Pfaffian](/problem/30148)（`pfaffian_of_matrix`）
- [矩阵快速幂](/problem/30149)（`pow_of_matrix`）
- [稀疏矩阵行列式](/problem/30150)（`sparse_matrix_det`）
- [线性方程组](/problem/30151)（`system_of_linear_equations`） · special judge
- [线性方程组（模 2）](/problem/30152)（`system_of_linear_equations_mod_2`） · special judge

<a id="sec-nt"></a>
## 数论

- [Bernoulli 数](/problem/30153)（`bernoulli_number`）
- [质数计数](/problem/30154)（`counting_primes`）
- [无平方因子数计数](/problem/30155)（`counting_squarefrees`）
- [狄利克雷卷积与前缀和](/problem/30156)（`dirichlet_convolution_and_prefix_sums`）
- [狄利克雷逆与前缀和](/problem/30157)（`dirichlet_inverse_and_prefix_sums`）
- [离散对数（固定模数）](/problem/30158)（`discrete_logarithm_fixed_mod`）
- [离散对数](/problem/30159)（`discrete_logarithm_mod`） · special judge
- [枚举质数](/problem/30160)（`enumerate_primes`）
- [枚举整除商](/problem/30161)（`enumerate_quotients`）
- [分解质因数](/problem/30162)（`factorize`）
- [高斯整数最大公约数](/problem/30163)（`gcd_of_gaussian_integers`） · special judge
- [整数开 k 次方](/problem/30164)（`kth_root_integer`）
- [模意义下开 k 次方](/problem/30165)（`kth_root_mod`） · special judge
- [线性函数取模最小值](/problem/30166)（`min_of_mod_of_linear`）
- [Nim 积](/problem/30167)（`nim_product_64`）
- [质数判定](/problem/30168)（`primality_test`）
- [原根](/problem/30169)（`primitive_root`） · special judge
- [有理数逼近](/problem/30170)（`rational_approximation`）
- [模意义下开平方](/problem/30171)（`sqrt_mod`） · special judge
- [Stern-Brocot 树](/problem/30172)（`stern_brocot_tree`）
- [线性函数取整求和](/problem/30173)（`sum_of_floor_of_linear`）
- [积性函数前缀和](/problem/30174)（`sum_of_multiplicative_function`）
- [积性函数前缀和（大范围）](/problem/30175)（`sum_of_multiplicative_function_large`）
- [欧拉函数前缀和](/problem/30176)（`sum_of_totient_function`）
- [迭代幂次取模](/problem/30177)（`tetration_mod`）
- [平方和表示](/problem/30178)（`two_square_sum`） · special judge

<a id="sec-ec"></a>
## 组合计数

- [Bell 数](/problem/30070)（`bell_number`）
- [二项式系数](/problem/30071)（`binomial_coefficient`）
- [二项式系数（质数模）](/problem/30072)（`binomial_coefficient_prime_mod`）
- [阶乘](/problem/30073)（`factorial`）
- [批量阶乘](/problem/30074)（`many_factorials`）
- [错排数（Montmort 数）](/problem/30075)（`montmort_number_mod`）
- [两序列间递增序列个数](/problem/30076)（`number_of_increasing_sequences_between_two_sequences`）
- [子序列个数](/problem/30077)（`number_of_subsequences`）
- [分拆数](/problem/30078)（`partition_function`）
- [q-二项式系数（质数模）](/problem/30079)（`q_binomial_coefficient_prime_mod`）
- [模 p 子集和计数](/problem/30080)（`sharp_p_subset_sum`）
- [第一类斯特林数](/problem/30081)（`stirling_number_of_the_first_kind`）
- [第一类斯特林数（固定 k）](/problem/30082)（`stirling_number_of_the_first_kind_fixed_k`）
- [第一类斯特林数（小 p 大 n）](/problem/30083)（`stirling_number_of_the_first_kind_small_p_large_n`）
- [第二类斯特林数](/problem/30084)（`stirling_number_of_the_second_kind`）
- [第二类斯特林数（固定 k）](/problem/30085)（`stirling_number_of_the_second_kind_fixed_k`）
- [第二类斯特林数（小 p 大 n）](/problem/30086)（`stirling_number_of_the_second_kind_small_p_large_n`）

<a id="sec-sps"></a>
## 集合幂级数

- [集合幂级数 exp](/problem/30217)（`exp_of_set_power_series`）
- [集合幂级数 log](/problem/30218)（`log_of_set_power_series`）
- [多项式复合集合幂级数](/problem/30219)（`polynomial_composite_set_power_series`）
- [集合幂级数幂投影](/problem/30220)（`power_projection_of_set_power_series`）
- [子集卷积](/problem/30221)（`subset_convolution`）

<a id="sec-geo"></a>
## 计算几何

- [凸多边形各顶点最远点](/problem/30087)（`all_furthest_neighbors`） · special judge
- [最近点对](/problem/30088)（`closest_pair`） · special judge
- [凸层](/problem/30089)（`convex_layers`）
- [三角形内点计数](/problem/30090)（`count_points_in_triangle`）
- [欧几里得最小生成树](/problem/30091)（`euclidean_mst`） · special judge
- [最远点对](/problem/30092)（`furthest_pair`） · special judge
- [曼哈顿最小生成树](/problem/30093)（`manhattanmst`） · special judge
- [最小圆覆盖](/problem/30094)（`minimum_enclosing_circle`）
- [极角排序](/problem/30095)（`sort_points_by_argument`） · special judge
- [静态凸包](/problem/30096)（`static_convex_hull`） · special judge

<a id="sec-bi"></a>
## 高精度

- [高精度整数加法](/problem/30005)（`addition_of_big_integers`）
- [十六进制高精度整数加法](/problem/30006)（`addition_of_hex_big_integers`） · special judge
- [高精度整数除法](/problem/30007)（`division_of_big_integers`）
- [十六进制高精度整数除法](/problem/30008)（`division_of_hex_big_integers`） · special judge
- [高精度整数乘法](/problem/30009)（`multiplication_of_big_integers`）
- [十六进制高精度整数乘法](/problem/30010)（`multiplication_of_hex_big_integers`） · special judge

<a id="sec-other"></a>
## 其他

- [线性递推序列连续项](/problem/30179)（`consecutive_terms_of_linear_recurrent_sequence`）
- [求线性递推式](/problem/30180)（`find_linear_recurrence`） · special judge
- [线性递推第 k 项](/problem/30181)（`kth_term_of_linearly_recurrent_sequence`）
- [最长上升子序列](/problem/30182)（`longest_increasing_subsequence`） · special judge
- [指数乘多项式之和](/problem/30183)（`sum_of_exponential_times_polynomial`）
- [指数乘多项式无穷和](/problem/30184)（`sum_of_exponential_times_polynomial_limit`）
- [2-SAT](/problem/30185)（`two_sat`） · special judge

<a id="sec-sample"></a>
## 入门样例

- [A+B 问题](/problem/30214)（`aplusb`）
- [多组 A+B](/problem/30215)（`many_aplusb`）
- [多组 A+B（128 位）](/problem/30216)（`many_aplusb_128bit`）
