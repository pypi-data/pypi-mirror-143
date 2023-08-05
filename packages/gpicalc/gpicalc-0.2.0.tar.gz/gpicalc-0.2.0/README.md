# GPI Calculator

## Welcome to GPI Calculator
A Package for Calculating Global Performance Indicator (GPI)<br/>
Use the GPI Calculator to compute a comprehensive performance metric for your models.

## Introduction
The GPI was introduced by Despotovic, et al. (2015) in their publication "Review and statistical analysis of different global solar radiation sunshine models". The motivation of creating the GPI was to combine multiple performance evaluation metrics into a single numerical representation for multi-dimensional and comprehensive comparison of different artificial intelligence/empirical models. The GPI metric has been cited and used in various articles such as:
* Chia, M.Y., Huang, Y.F. and Koo, C.H., 2021. Improving reference evapotranspiration estimation using novel inter-model ensemble approaches. Computers and Electronics in Agriculture, 187, p.106227.
* Chia, M.Y., Huang, Y.F. and Koo, C.H., 2022. Resolving data-hungry nature of machine learning reference evapotranspiration estimating models using inter-model ensembles with various data management schemes. Agricultural Water Management, 261, p.107343.

## Installation
```bash
pip install gpicalc
```

## Example
We can import the test.xlsx supplied in the repository using the following lines:
```bash
import pandas as pd

data = pd.read_excel('test.xlsx', index_col=0)
```

This will give you a DataFrame named "data" that has 3 columns (MAE, RMSE and R2) and 30 rows (30 different models).

Next, import the "GPICalculator" class from the [gpi package](https://github.com/planta94/gpi) to create a GPICalculator object.
```bash
from gpicalc import GPICalculator

calculator = GPICalculator()
```

To obtain the GPI score, use the GPICalculator.score() method by including "data" and a list of coefficient as the parameters.
```bash
coefficient = [1, 1, -1] # Use positive coefficient for metrics to be minimised (MAE, RMSE), and negative coefficient for metrics to be maximized (R2)
gpi_score = calculator.score(data, coefficient) # GPI is positive-oriented, the higher the better
```
## Support
For any suggestions or feedbacks, I will be available at this repository or chiamy94@gmail.com.
