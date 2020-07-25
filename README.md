<!--
 * @Author: your name
 * @Date: 2020-07-13 10:35:16
 * @LastEditTime: 2020-07-25 09:44:52
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \szcup2020_simulation\README.md
--> 


深圳杯2020——数学建模模拟赛——C题
====

## 依赖库
- Google or-tools
- xlrd
- matplotlib
- sys
- numpy
- math
- sympy (符号计算)
## 计算公式
- 经度（东西方向）1M实际度：31544206M*cos(纬度)/360°=
  
  $31544206\cdot\cos(latitude=36)/360 = 708883.29m/longtitude$

- 纬度（南北方向）1M实际度：40030173M360°=

  $40030173/360 = 111194.92m/latitude$

## 第一题

#### 使用first solution strategy获得计算近似解
求得结果
```bash
Route:
Route:
 0 -> 10 -> 16 -> 27 -> 12 -> 8 -> 9 -> 15 -> 7 -> 11 -> 6 -> 14 -> 25 -> 18 -> 26 -> 19 -> 20 -> 1 -> 2 -> 17 -> 29 -> 21 -> 23 -> 24 -> 28 -> 22 -> 3 -> 4 -> 5 -> 13 -> 0
Distance: 39410m
```
![](img/1/local_shortest.svg)
#### 使用guided local search获得最优解
求得结果
```bash
Route:
 0 -> 29 -> 17 -> 2 -> 1 -> 20 -> 19 -> 26 -> 18 -> 25 -> 14 -> 6 -> 11 -> 7 -> 15 -> 9 -> 8 -> 12 -> 27 -> 16 -> 10 -> 13 -> 5 -> 4 -> 3 -> 22 -> 28 -> 24 -> 23 -> 21 -> 0
Distance: 39305m
```
![](img/1/global_shortest.svg)

## 第二问：数值解法（numerical）

要使传感器一直工作的最低要求：在移动电源走完一整个回路后，电池容量刚好达到最低要求为最优

假设初始条件：当到达该节点时，剩余电池容量刚好为最低要求

### 参数定义
  
- $x_1,x_2,\cdots,x_{30}$：假设每个节点的电池容量
- $c_1,c_2,\cdots,c_{30}$：每个节点的电池消耗速度
- $r(mA/s)$：电池充电速度
- $f$：最低工作电量
- $v(m/s)$：移动充电器移动速度
- $dst$：总路程

### 等式
- **时间总花费**：$t_{tot}=dst/v+\sum_{i=1}^{30}{(x_i - f)/r_i}$
- **电池容量推导**：$x_i=t_{tot}\cdot c_i+f$

### 约束条件
去掉数据中心节点的充电计算

$$x_{i} = [dst/v+\sum_{i=2}^{30}{(x_{i} - f)/r_i}]\cdot c_i+f$$

### 根据约束条件得出线性方程组
组合结果为一个29*29的矩阵：

$$
\left[ \begin{array}{l}
	\boldsymbol{x}_2\\
	\vdots\\
	\boldsymbol{x}_{30}\\
\end{array} \right] =\left[ \begin{array}{c}
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_2}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots\\
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_{30}}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
\end{array} \right] +\left[ \begin{array}{c}
	\frac{\boldsymbol{x}_2\cdot \boldsymbol{c}_2}{\boldsymbol{r}}+\cdots +\frac{\boldsymbol{x}_{30}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots\\
	\frac{\boldsymbol{x}_2\cdot \boldsymbol{c}_2}{\boldsymbol{r}}+\cdots +\frac{\boldsymbol{x}_{30}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
\end{array} \right] 
$$


化简：

$$
\left[ \begin{array}{l}
	\boldsymbol{x}_2\\
	\vdots\\
	\boldsymbol{x}_{30}\\
\end{array} \right] =\left[ \begin{array}{c}
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_2}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}_2}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}_{30}}\\
	\vdots\\
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_{30}}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}_2}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}_{30}}\\
\end{array} \right] +\left[ \begin{array}{c}
	\frac{\boldsymbol{x}_2\cdot \boldsymbol{c}_2}{\boldsymbol{r}_2}+\cdots +\frac{\boldsymbol{x}_{30}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}_{30}}\\
	\vdots\\
	\frac{\boldsymbol{x}_2\cdot \boldsymbol{c}_2}{\boldsymbol{r}_2}+\cdots +\frac{\boldsymbol{x}_{30}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}_{30}}\\
\end{array} \right] 
$$

转化成$A\cdot X = b$形式：

$$
\left[ \begin{matrix}
	\frac{\boldsymbol{c}_2}{\boldsymbol{r}}-1&		\cdots&		\frac{\boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots&		\ddots&		\vdots\\
	\frac{\boldsymbol{c}_2}{\boldsymbol{r}}&		\cdots&		\frac{\boldsymbol{c}_{30}}{\boldsymbol{r}}-1\\
\end{matrix} \right] \cdot \left[ \begin{array}{l}
	\boldsymbol{x}_2\\
	\vdots\\
	\boldsymbol{x}_{30}\\
\end{array} \right] =-\left[ \begin{array}{c}
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_2}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots\\
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_{30}}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
\end{array} \right] 
$$


其中 


$$
\boldsymbol{A}=\left[ \begin{matrix}
	\frac{\boldsymbol{c}_2}{\boldsymbol{r}}-1&		\cdots&		\frac{\boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots&		\ddots&		\vdots\\
	\frac{\boldsymbol{c}_2}{\boldsymbol{r}}&		\cdots&		\frac{\boldsymbol{c}_{30}}{\boldsymbol{r}}-1\\
\end{matrix} \right] 

，
\boldsymbol{b}=-\left[ \begin{array}{c}
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_2}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
	\vdots\\
	\frac{\boldsymbol{dst}\cdot \boldsymbol{c}_{30}}{\boldsymbol{v}}+\boldsymbol{f}-\frac{\boldsymbol{f}\cdot \boldsymbol{c}_2}{\boldsymbol{r}}-\cdots -\frac{\boldsymbol{f}\cdot \boldsymbol{c}_{30}}{\boldsymbol{r}}\\
\end{array} \right] 
$$

### 参数设置
1. 速度$v=100m/s$
2. 充电速度$r = 2000mA/s$
3. 最低工作值$f=4mA$

### 数值解结果
| nodes | battery capacity |
|:-----:|------------------|
|   0   | 2298.415         |
|   1   | 3241.665         |
| 2     | 1944.696         |
| 3     | 2337.717         |
| 4     | 1590.977         |
| 5     | 1944.696         |
| 6     | 2691.436         |
| 7     | 1983.998         |
| 8     | 1944.696         |
| 9     | 2337.717         |
| 10    | 1944.696         |
| 11    | 3084.457         |
| 12    | 2730.738         |
| 13    | 1944.696         |
| 14    | 1669.581         |
| 15    | 1944.696         |
| 16    | 2337.717         |
| 17    | 3123.759         |
| 18    | 2337.717         |
| 19    | 1944.696         |
| 20    | 1551.675         |
| 21    | 2337.717         |
| 22    | 3123.759         |
| 23    | 1551.675         |
| 24    | 2337.717         |
| 25    | 1866.092         |
| 26    | 1590.977         |
| 27    | 2691.436         |
| 28    | 2298.415         |


## 第二问：符号解法（symbolic）

代码已经实现，但是矩阵渲染太大导致计算机崩溃，故此可以得出利用符号解求解该问题并没有意义。