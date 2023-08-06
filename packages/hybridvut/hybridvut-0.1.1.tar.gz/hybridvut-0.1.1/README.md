# hybridvut

This package provides functionalities to deal with hybrid IO-LCA based on the Make and Use framework.

Key features are:
* hybridization of a foreground and a background system
* unit handling using [iam_units](https://github.com/IAMconsortium/units) ([pint](https://pint.readthedocs.io/en/stable/) units)
* functions for data handling (e.g. region aggregation, RAS)
* basic IO calculations (e.g. transaction and multiplier matrices)
* preprocessing to bring raw data into the right format (i.e. message-ix data)

Additional hybridization procedures might be implemented in future work. Furthermore, functions can be also applied just to a single system.


## Basic structure

The general idea is to distinguish between a foreground and a background system.
The forground system and the background system are represented by a make table (V<sub>for</sub> and V<sub>back</sub>, respectively) and a use table (U<sub>for</sub>  and U<sub>back</sub> , respectively).

The aim is to combine both systems so that no double-counting occurs. Special emphasize is thus needed for the use table U.

To connect both systems properly, co-called cut-off matrices C<sub>u</sub> and C<sub>d</sub> are introduced. C<sub>u</sub> connects the upstream processes of the foreground system to the industries of the background system. C<sub>d</sub> connects the downstream industries to the processes of the foreground sytem.
V<sub>for</sub>, V<sub>back</sub>, U<sub>for</sub> and U<sub>back</sub> are known.

The hybridized total system represented by V and U includes all necessary adoptions of the submatrices and avoids double-counting.    

|       -          | Make Table V        |  ----------->        | Use Table U         | ---------->          |
| ---------------- | ------------------- | -------------------- | ------------------- | -------------------- |
|     *indices*    | *c<sub>f</sub>*     | *c<sub>b</sub>*      | *i<sub>f</sub>*     | *i<sub>b</sub>*      |
| *c<sub>f</sub>*  |                     |                      | **U<sub>for</sub>** |    C<sub>d</sub>     |
| *c<sub>b</sub>*  |                     |                      | C<sub>u</sub>       | **U<sub>back</sub>** |
| *i<sub>f</sub>*  | **V<sub>for</sub>** | 0                    |                     |                      |
| *i<sub>b</sub>*  | 0                   | **V<sub>back</sub>** |                     |                      |

Furthermore, additional factors can be taken into account which are represented by the intervention matrix F.

To re-allocate the interventions from the industries of the background system to the foreground system, a sub-matrix F<sub>u</sub> is introduced.

NOTE: An additional sub-matrix is thinkable to re-allocate interventions the other way around, but is not yet implemented. The intervention tables might be in principle  also defined per commodity.

|       -          | Intervention Table F | ------------------>  | Intervention Table F | ------------------>      |
| ---------------- | -------------------- | -------------------- | -------------------- | ------------------------ |
|  *indices*       |  *c<sub>f</sub>*     | *c<sub>b</sub>*      | *i<sub>f</sub>*      | *i<sub>b</sub>*          |
| *k<sub>f</sub>*  |          0           |          0           | **F<sub>for</sub>**  | 0                        |
| *k<sub>b</sub>*  |          0           |          0           |  F<sub>u</sub>       | **F<sub>back</sub>**     |


## Data format

The hybridvut package uses [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) to deal with the required matrices. The format of these DataFrames needs to fulfill certain requirements in regard to its [pandas.MultiIndex](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html).

**Make matrix V**:

|     -      | **region**    | ...             | ...             | ... |
| ---------- | ------------- | --------------- | --------------- | --- |
|            | **commodity** | ...             | ...             | ... |
|            | **unit**      | ...             | ...             | ... |
| **region** | **industry**  |                 |                 |     |
| ...        | ...           | v<sub>1,1</sub> | v<sub>1,2</sub> | ... |
| ...        | ...           | v<sub>2,1</sub> | v<sub>2,2</sub> | ... |
| ...        | ...           | ...             | ...             | ... |


**Use matrix U**:

|     -      |    -           | **region**     | ...             | ...             | ... |
| ---------- | -------------- | -------------- | --------------- | --------------- | --- |
|            |                | **industry**   | ...             | ...             | ... |
| **region** | **commodity**  | **unit**       |                 |                 |     |
| ...        | ...            | ...            | u<sub>1,1</sub> | u<sub>1,2</sub> | ... |
| ...        | ...            | ...            | u<sub>2,1</sub> | u<sub>2,2</sub> | ... |
| ...        | ...            | ...            | ...             | ...             | ... |


**Intervention matrix F**:

|     -            | **region**   | ...             | ...             | ... |
| ---------------- | ------------ | --------------- | --------------- | --- |
|                  | **industry** | ...             | ...             | ... |
| **intervention** | **unit**     |                 |                 |     |
| ...              | ...          | f<sub>1,1</sub> | f<sub>1,2</sub> | ... |
| ...              | ...          | f<sub>2,1</sub> | f<sub>2,2</sub> | ... |
| ...              | ...          | ...             | ...             | ... |


**Characterization matrix Q**:

|     -      | **intervention** | ...             | ...             | ... |
| ---------- | ---------------- | --------------- | --------------- | --- |
|            | **unit**         | ...             | ...             | ... |
| **impact** | **unit**         |                 |                 |     |
| ...        | ...              | q<sub>1,1</sub> | q<sub>1,2</sub> | ... |
| ...        | ...              | q<sub>2,1</sub> | q<sub>2,2</sub> | ... |
| ...        | ...              | ...             | ...             | ... |

## Hybridization procedure

This section describes the current core procedure for hybridization.

```python
import hybridvut as hyb

foreground = hyb.VUT(V=V_for, U=U_for, F=F_for, Q=None)
background = hyb.VUT(V=V_back, U=U_back, F=F_back, Q=Q_back)

HT = hyb.HybridTables(forground=foreground, background=background)
HT.hybridize(H, H1, HF)

# Hybridized total system
HT.total.V
HT.total.U
HT.total.F
HT.total.Q
```

1. Define concordance matrices H, H1 and HF (for industries, commodities and interventions, respectively)
2. Adjust V<sub>back</sub>, U<sub>back</sub>; and calculate q and x based on V
3. Define weighting factor matrices T and T1
4. Calculate upstream cut-off matrix C<sub>u</sub> and adjust U<sub>back</sub> (second time)
5. Calculate downstream cut-off matrix C<sub>d</sub> and  adjust U<sub>back</sub> (third time)
6. Correct C<sub>d</sub>, C<sub>u</sub> and U<sub>for</sub> 
7. Adjust intervention sub-tables of F 
8. Combine all submatrices into V, U and F
9. Adjust characterization matrix Q

### 1) Define concordance matrices H ($`H_{ind}`$), H1 ($`H_{com}`$) and HF ($`H_{int}`$)

$`H_{ind}`$ relates process of foreground system to industry of background system (includes 1 if relation, otherwise 0).

$`H_{com}`$ relates commodity of foreground system to commodity of background system (includes 1 if relation, otherwise 0).

$`H_{int}`$ relates an intervention of the foreground system to an intervention of the background system (includes 1 if relation, otherwise 0).

Note: in multi-regional models the relation is country-wise (e.g., a commodity of a country can only related to a commodity of one country). However, more than one industry of the background can be associated to the industry of the forground system (the same is true for the commodity relation). Thereby, the sum of all associated industries (commodities) must equal 1. 

**Concordance matrix H for industries**:

|    -       | **region**   | ...               | ...               | ... |
| ---------- | ------------ | ----------------- | ----------------- | --- |
|            | **industry** | ...               | ...               | ... |
| **region** | **industry** |                   |                   |     |
| ...        | ...          | h<sub>1b,1f</sub> | h<sub>1b,2f</sub> | ... |
| ...        | ...          | h<sub>2b,1f</sub> | h<sub>2b,2f</sub> | ... |
| ...        | ...          | ...               | ...               | ... |


**Concordance matrix H1 for commodities**:

|      -     |    -          | **region**    | ...                | ...                | ... |
| ---------- | ------------- | ------------- | ------------------ | ------------------ | --- |
|            |               | **commodity** | ...                | ...                | ... |
|            |               | **unit**      | ...                | ...                | ... |
| **region** | **commodity** | **unit**      |                    |                    |     |
| ...        | ...           | ...           | h1<sub>1f,1b</sub> | h1<sub>1f,2b</sub> | ... |
| ...        | ...           | ...           | h1<sub>2f,1b</sub> | h1<sub>2f,2b</sub> | ... |
| ...        | ...           | ...           | ...                | ...                | ... |


**Concordance matrix HF for interventions**:

|       -          | **intervention**   | ...                | ...                | ... |
| ---------------- | ------------------ | ------------------ | ------------------ | --- |
|                  | **unit**           | ...                | ...                | ... |
| **intervention** | **unit**           |                    |                    |     |
| ...              | ...                | hf<sub>1b,1f</sub> | hf<sub>1b,2f</sub> | ... |
| ...              | ...                | hf<sub>2b,1f</sub> | hf<sub>2b,2f</sub> | ... |
| ...              | ...                | ...                | ...                | ... |


### 2  Adjust $`V_{back}`$, $`U_{back}`$; and calculate $`q`$ and $`g`$ based on $`V`$

```math
\mathbf{U}_{back}^{adj} = \mathbf{U}_{back} - \mathbf{H}_{com}^{T} \cdot \mathbf{U}_{for} \cdot \mathbf{H}_{ind}^{T} \\
\mathbf{V}_{back}^{adj} = \mathbf{V}_{back} - \mathbf{H}_{ind} \cdot \mathbf{V}_{for} \cdot \mathbf{H}_{com} \\
\mathbf{g}_{for} = \mathbf{V}_{for} \cdot \mathbf{i} \\
\mathbf{q}_{for} = \mathbf{V}_{for}^{T} \cdot \mathbf{i} \\
\mathbf{g}_{back}^{adj} = \mathbf{V}_{back}^{adj} \cdot \mathbf{i} \\
\mathbf{q}_{back}^{adj} = \mathbf{V}_{back}^{adj T} \cdot \mathbf{i} 
```

, where $`ì`$ is the summation vector of ones with prpoper lenght.

### 3) Calculate weighting factor matrices T ($`T_{u}`$) and T1 ($`T_{d}`$)
Matrix $`T_{u}`$ defines how much of the upstream input can be related to the foreground processes (and thus shifted from the background industries). Here, the assumption is made that this is determined automatically by the ratio of industry output x (of the new process and its reference industry).

```math
\mathbf{T}_{u} = \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} \right]  \varnothing  \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} + \mathbf{J}_{c,i} \cdot \mathbf{\hat{x}_{back}^{adj}} \cdot \mathbf{H}_{ind}  \right]
```


Matrix$`T_{d}`$ defines how much of the downstream input can be related to the foreground processes (and thus shifted from the background industries). Here, the assumption is made that this is determined by the ratio of commodity output q (of the new commodity and its reference commodity).

```math
\mathbf{T}_{d} = \left[  \mathbf{\hat{q}_{for}}  \cdot \mathbf{H}_{com} \cdot  \mathbf{J}_{c,i}  \right]  \varnothing  \left[ \mathbf{\hat{q}_{for}}  \cdot \mathbf{H}_{com} \cdot  \mathbf{J}_{c,i} + \mathbf{H}_{com} \cdot \mathbf{\hat{q}_{back}^{adj}}  \cdot \mathbf{J}_{c,i} \right]
```


### 4) Calculate upstream cut-off matrix $`C_{u}`$ and adjust $`U_{back}`$ (second time)

```math
\mathbf{C}_{u} = \mathbf{T}_{u} \odot \mathbf{U}_{back}^{adj} \cdot \mathbf{H}_{ind} \\
\mathbf{U}_{back}^{adj1} = \mathbf{U}_{back}^{adj} - \mathbf{C}_{u} \cdot \mathbf{H}_{ind}^{T} 
```

### 5) Calculate downstream cut-off matrix $`C_{d}`$ and  adjust $`U_{back}`$ (third time)

```math
\mathbf{C}_{d} = \mathbf{T}_{d} \odot \mathbf{H}_{com} \cdot \mathbf{U}_{back}^{adj1} \\
\mathbf{U}_{back}^{adj2} = \mathbf{U}_{back}^{adj1} - \mathbf{H}_{com}^{T} \cdot \mathbf{C}_{d} 
```

### 6) Correct $`C_{u}`$, $`C_{d}`$ and $`U_{for}`$

The correction term $`\mathbf{O}_{u}`$ removes commodities those are actually covered as commodities in the foreground system.
The correction term $`\mathbf{O}_{d}`$ removes commodities those are actually used by technology of the foreground system.

```math
\mathbf{C}_{u}^{adj} = \mathbf{C}_{u} - \underbrace{ \mathbf{C}_{u} \odot \mathbf{H}_{com}^{T} \cdot \mathbf{T}_{u} \cdot \mathbf{H}_{ind} }_{\text{correction term $\mathbf{O}_{u}$}}\\
\mathbf{C}_{d}^{adj} = \mathbf{C}_{d} - \underbrace{ \mathbf{C}_{d} \odot \mathbf{H}_{com} \cdot \mathbf{T}_{d} \cdot \mathbf{H}_{ind}^{T}}_{\text{correction term $\mathbf{O}_{d}$}} \\
\mathbf{U}_{for}^{adj} = \mathbf{U}_{for} + \mathbf{H}_{com} \cdot \mathbf{O}_{u} + \mathbf{O}_{d} \cdot \mathbf{H}_{ind}
```



### 7) Adjust intervention sub-tables of $`F`$
The re-allocation procedure is similar to the first steps of re-allocation the commodities from the background to the foreground system. The implicit assumption is (currently) that the background system already includes the intire interventions; and no additional interventions are added by the foreground system. The task hence is to remove the interventions of the associated processes from the background system to the foreground system, which are not yet taken into account in the foreground system.

```math
\mathbf{F}_{back}^{adj} = \mathbf{F}_{back} - \mathbf{H}_{inter} \cdot \mathbf{F}_{for} \cdot \mathbf{H}_{ind}^{T} \\
\mathbf{T}_{inter} = \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} \right]  \varnothing  \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} + \mathbf{J}_{c,i} \cdot \mathbf{\hat{g}_{back}^{adj}} \cdot \mathbf{H}_{ind}  \right] \\
\mathbf{F}_{u} = \mathbf{T}_{inter} \odot \mathbf{F}_{back}^{adj} \cdot \mathbf{H}_{ind} \\ 
\mathbf{F}_{back}^{adj1} = \mathbf{F}_{back}^{adj} - \mathbf{F}_{u} \cdot \mathbf{H}_{ind}^{T}
```


### 8) Combine all submatrices into $`V`$, $`U`$ and $`F`$

|       -         | Make Table V        |  ----------->                      | Use Table U                        |  ---------->                         |
| --------------- | ------------------- | ---------------------------------- | ---------------------------------- | ------------------------------------ |
|     *indices*   | *c<sub>f</sub>*     | *c<sub>b</sub>*                    | *i<sub>f</sub>*                    | *i<sub>b</sub>*                      |
| *c<sub>f</sub>* |                     |                                    | **U<sub>for</sub><sup>adj</sup>**  | **C<sub>d</sub><sup>adj</sup>**      |
| *c<sub>b</sub>* |                     |                                    | **C<sub>u</sub><sup>adj</sup>**    | **U<sub>back</sub><sup>adj2</sup>**  |
| *i<sub>f</sub>* | **V<sub>for</sub>** | 0                                  |                                    |                                      |
| *i<sub>b</sub>* | 0                   | **V<sub>back</sub><sup>adj</sup>** |                                    |                                      |



|       -          | Intervention Table F | ---------------------> | Intervention Table F | ------------------->                |
| ---------------- | -------------------- | ---------------------- | -------------------- | ----------------------------------- |
|  *indices*       |   *c<sub>f</sub>*    |  *c<sub>b</sub>*       | *i<sub>f</sub>*      | *i<sub>b</sub>*                     |
| *k<sub>f</sub>*  |              0       |      0                 | **F<sub>for</sub>**  | 0                                   |
| *k<sub>b</sub>*  |          0           |         0              |  **F<sub>u</sub>**   | **F<sub>back</sub><sup>adj1</sup>** |


### 9) Adjust characterization matrix $`Q`$
To deal with the characterization factors of (environmental) interventions, currently, two alternatives are implemented:
* Characterisation factors are provided for the background system; or
* Characterization factors are provided for the foreground system

If **Q<sub>back</sub>** is given:

```math
\mathbf{Q}_{for} = \mathbf{Q}_{back} \cdot \mathbf{H}_{int}
```


If **Q<sub>for</sub>** is given:

```math
\mathbf{Q}_{back} = \mathbf{Q}_{for} \cdot \mathbf{H}_{int}^{T}
```


|       -               | Characterization Table Q | ---------------------> |
| --------------------- | ------------------------ | ---------------------- |
|  *indices*            |   *k<sub>f</sub>*        |  *k<sub>b</sub>*       |
| *o<sub>f or b</sub>*  | **Q<sub>for</sub>**      |  **Q<sub>back</sub>**  |

 
### Further notes
The hybridization procedure for the messageix-exiobase example includes three modifications of these steps (necessary due to the nature of the messageix model):
1. Aggregating sectors (i.e., technologies those have "final" products as input flows) are set to zero. The use of these products is covered by the background system.
2. To ensure that value added is the same after hybridizarion, we use it from the background system ($`F_{back}`$), allocate it among the industries (i.e. foreground technologies) and resacle the make and use tables to fulfill the original Exiobase ratios of values added ($`v_{back}_{i}`$) per intermediate input ($`\sum_{c} U_{back}_{c,i}`$) of the corresponding industry i.
3. Before allocating GHG emissions from background to foreground industries (step 7), the total GHG emissions (CO2, CH4, N20), are usd to scale the corresponding emissions in Exiobase. GHG emissions of the foreground system are then set to zero ($`F_{for}`$).
