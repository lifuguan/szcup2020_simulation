<!--
 * @Author: your name
 * @Date: 2020-07-23 10:35:16
 * @LastEditTime: 2020-07-23 11:11:19
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \szcup2020_simulation\README.md
--> 


深圳杯2020——数学建模模拟赛——C题
====

## 依赖库
- Google or-tools
- xlrd

## 计算公式
- 经度（东西方向）1M实际度：31544206M*cos(纬度)/360°=
  
  $31544206\cdot\cos(latitude=36)/360 = 708883.29m/longtitude$

- 纬度（南北方向）1M实际度：40030173M360°=

  $40030173/360 = 111194.92m/latitude$